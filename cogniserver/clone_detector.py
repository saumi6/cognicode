import os
import ast
import numpy as np
import faiss
from typing import List

# Upgraded to the modern google.genai SDK (google-generativeai is deprecated)
from google import genai as google_genai
from google.genai import types as genai_types

EMBEDDING_MODEL = 'models/gemini-embedding-001'

def _load_api_key() -> str | None:
    """Load GEMINI_API_KEY from env or .env file directly."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(root_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                        api_key = line.split("=", 1)[1].strip()
                        os.environ["GEMINI_API_KEY"] = api_key
                        break
    return api_key


def extract_functions(file_map: dict) -> List[dict]:
    """Parse Python files and extract function bodies as strings."""
    functions = []
    for module_name, abs_path in file_map.items():
        if not os.path.exists(abs_path):
            continue
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            lines = source.split("\n")
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, "end_lineno") and node.end_lineno is not None:
                        func_body = "\n".join(lines[node.lineno - 1 : node.end_lineno])
                    else:
                        func_body = f"def {node.name}(): ...\n"
                    # Skip trivially short functions
                    if len(func_body.strip()) < 50:
                        continue
                    functions.append(
                        {"file": module_name, "func_name": node.name, "code": func_body}
                    )
        except Exception:
            pass
    return functions


def scan_for_clones(file_map: dict) -> List[dict] | dict:
    """
    Core Semantic Clone Engine.
    Parses ASTs, embeds via Gemini text-embedding-004, uses FAISS L2 search.
    Returns a list of clone pairs or an error dict.
    """
    api_key = _load_api_key()
    if not api_key:
        return {"error": "GEMINI_API_KEY not configured. Please set it in your .env file."}

    client = google_genai.Client(api_key=api_key)

    functions = extract_functions(file_map)
    if not functions:
        return []

    print(f"[CLONE] Extracting embeddings for {len(functions)} functions...")
    contents = [f["code"] for f in functions]

    # Batch into chunks of 10 to avoid 429 rate-limit errors on the free tier
    import time
    BATCH_SIZE = 10
    embeddings = []
    try:
        for i in range(0, len(contents), BATCH_SIZE):
            batch = contents[i : i + BATCH_SIZE]
            print(f"[CLONE]   Embedding batch {i // BATCH_SIZE + 1} ({len(batch)} items)...")
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=genai_types.EmbedContentConfig(task_type="retrieval_document"),
            )
            embeddings.extend([e.values for e in response.embeddings])
            # Small delay between batches to respect rate limits
            if i + BATCH_SIZE < len(contents):
                time.sleep(1.5)
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {"error": f"Embedding API failed: {str(e)}"}

    mat = np.array(embeddings, dtype="float32")
    n_funcs, d_dims = mat.shape
    print(f"[CLONE] Building FAISS index (n={n_funcs}, d={d_dims})...")

    index = faiss.IndexFlatL2(d_dims)
    index.add(mat)

    # k=2: nearest[0] is always self (dist≈0), nearest[1] is the closest other function
    distances, indices = index.search(mat, 2)

    # L2 distance threshold — text-embedding-004 produces ~unit vectors so L2 ≈ 2*(1-cos)
    # distance < 0.25 ≈ cosine similarity > 0.875 — very strong semantic match
    THRESHOLD = 0.25
    clones_found = []
    seen_pairs: set = set()

    for i in range(n_funcs):
        j = int(indices[i][1])
        dist = float(distances[i][1])

        if dist < THRESHOLD and j != -1:
            pair = tuple(sorted([i, j]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            f1, f2 = functions[i], functions[j]
            # Skip if same file + same function name (duplicate AST walk artifact)
            if f1["file"] == f2["file"] and f1["func_name"] == f2["func_name"]:
                continue

            similarity_pct = round(max(0.0, (1.0 - dist / 2.0)) * 100, 1)
            clones_found.append(
                {
                    "score": similarity_pct,
                    "func1": {"name": f1["func_name"], "file": f1["file"]},
                    "func2": {"name": f2["func_name"], "file": f2["file"]},
                }
            )

    print(f"[CLONE] Scan complete. Found {len(clones_found)} semantic clone(s).")
    return clones_found

# ===== SEMANTIC KNOWLEDGE BASE (FEATURE 11) =====
_search_cache = {"mat": None, "functions": None}

def search_code(query: str, file_map: dict) -> List[dict] | dict:
    """
    Embeds a natural language query with Gemini and searches the FAISS codebase index
    to return top-matching code snippets. Uses internal caching to avoid re-embedding.
    """
    api_key = _load_api_key()
    if not api_key:
        return {"error": "GEMINI_API_KEY not configured."}

    client = google_genai.Client(api_key=api_key)

    # 1. Embed or load the codebase
    if _search_cache["mat"] is None or _search_cache["functions"] is None:
        functions = extract_functions(file_map)
        if not functions:
            return []
        
        contents = [f["code"] for f in functions]
        embeddings = []
        import time
        for i in range(0, len(contents), 10):
            batch = contents[i:i+10]
            resp = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=genai_types.EmbedContentConfig(task_type="retrieval_document")
            )
            embeddings.extend([e.values for e in resp.embeddings])
            if i + 10 < len(contents): time.sleep(1)

        _search_cache["mat"] = np.array(embeddings, dtype="float32")
        _search_cache["functions"] = functions

    # 2. Embed the natural language search query
    try:
        q_resp = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[query],
            config=genai_types.EmbedContentConfig(task_type="retrieval_query")
        )
        q_mat = np.array([q_resp.embeddings[0].values], dtype="float32")
    except Exception as e:
        return {"error": f"Failed to embed search query: {e}"}

    # 3. FAISS Search
    mat = _search_cache["mat"]
    n_funcs, d_dims = mat.shape
    index = faiss.IndexFlatL2(d_dims)
    index.add(mat)

    k = min(5, n_funcs)
    distances, indices = index.search(q_mat, k)

    results = []
    for i in range(k):
        idx = int(indices[0][i])
        dist = float(distances[0][i])
        if idx != -1:
            f = _search_cache["functions"][idx]
            match_pct = round(max(0.0, (1.0 - dist / 2.0)) * 100, 1)
            results.append({
                "score": match_pct,
                "func_name": f["func_name"],
                "file": f["file"],
                "code": f["code"]
            })

    return results
