import os
import re
import numpy as np
from .model_utils import embed_text

def retrieve(query: str, index, metas, top_k=5, boost=0.2):
    """
    Performs vector search, applies keyword boosting, and returns sorted results.
    """
    # 1. Embed the query
    q_emb = embed_text([query])
    
    # 2. Normalize the query vector
    q_emb = q_emb / np.clip(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-9, None)
    
    # 3. Search the FAISS index
    D, I = index.search(q_emb, top_k * 2)  # Fetch double the results for better reranking
    
    results = []
    query_terms = set(re.findall(r"\w+", query.lower()))
    
    # 4. Rerank/Boost Results
    for score, idx in zip(D[0], I[0]):
        meta = metas[idx].copy()
        
        # Simple keyword boosting logic: boost the score if query terms appear
        # in the function/file name.
        name = str(meta.get("name", "")).lower()
        fname = os.path.basename(meta.get("filename", "")).lower()
        
        for term in query_terms:
            if term and (term in name or term in fname):
                score += boost
                
        results.append({"score": float(score), "meta": meta})
        
    # 5. Sort and return the top K results
    results = sorted(results, key=lambda x: -x["score"])
    return results[:top_k]

def format_result(result, all_chunks, base_path):
    """Formats a single search result into a detailed, readable string."""
    score = result['score']
    meta = result['meta']
    
    filepath = meta['filepath']
    relative_path = os.path.relpath(filepath, base_path) if base_path else filepath
    name = meta.get('name', 'N/A')
    
    # Find the original code snippet (This requires accessing the original file)
    snippet = "Error: Snippet not found."
    try:
        # NOTE: To get the snippet in a terminal environment, we must re-read the file
        # and extract the code using the function name.
        with open(filepath, 'r', encoding='utf-8') as f:
            full_code = f.read()
        
        # Re-parse the file to find the snippet (less efficient but necessary here)
        from .indexing import extract_chunks_from_code
        
        # Find the specific chunk text
        file_lang = meta['language']
        chunks = extract_chunks_from_code(full_code, file_lang, filepath)
        
        # Search for the matching chunk text by name (or use the whole file if type='file')
        for chunk in chunks:
            if chunk['meta'].get('name') == name and chunk['meta'].get('type') == 'function':
                 snippet = chunk['text']
                 break
            elif meta['type'] == 'file':
                 snippet = full_code
                 break

    except Exception as e:
        snippet = f"Error reading file or extracting snippet: {e}"

    
    output = f"┌──────────────────────────────────────────────────────────\n"
    output += f"│ Score: {score:.4f} \n"
    output += f"│ Type:  {meta['type'].upper()} ({meta['language'].capitalize()})\n"
    output += f"│ Name:  {name}\n"
    output += f"│ Path:  ./{relative_path}\n"
    output += f"├──────────────────────────────────────────────────────────\n"
    
    # Indent the snippet nicely
    indented_snippet = "\n".join(["│   " + line for line in snippet.splitlines()])
    output += indented_snippet + "\n"
    output += f"└──────────────────────────────────────────────────────────\n"
    return output
