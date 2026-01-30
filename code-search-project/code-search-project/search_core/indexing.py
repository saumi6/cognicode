import os
import glob
import numpy as np
import faiss
from tree_sitter_languages import get_parser
from .model_utils import embed_text

# Global Tree-sitter parser cache
LANGUAGE_PARSERS = {}
EXT_LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c"
}

def get_parser_for_language(lang_name: str):
    """Fetches or initializes the tree-sitter parser for a given language."""
    if lang_name in LANGUAGE_PARSERS:
        return LANGUAGE_PARSERS[lang_name]
    try:
        parser = get_parser(lang_name)
    except Exception:
        parser = None
    LANGUAGE_PARSERS[lang_name] = parser
    return parser

def find_nodes(node, types_set):
    """Performs a depth-first search to find nodes of specific types."""
    res = []
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in types_set:
            res.append(n)
        # Push children in reverse order to process them left-to-right
        stack.extend(reversed(n.children))
    return res

def extract_chunks_from_code(code: str, language: str, filename: str):
    """
    Extracts function/method-level code chunks using tree-sitter.
    If no functions are found, the whole file is returned as a single chunk.
    """
    parser = get_parser_for_language(language)
    if parser is None:
        return [{"text": code, "meta": {"filename": filename, "language": language, "type": "file", "name": os.path.basename(filename)}}]
        
    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node
    
    # Types that define functions/methods across languages
    types_set = set(["function_definition", "function_declaration", "method_declaration", "method_definition", "function", "method"])
    func_nodes = find_nodes(root, types_set)
    code_bytes = code.encode("utf8")
    chunks = []
    
    if not func_nodes:
        # If no explicit functions, return the whole file
        chunks.append({"text": code, "meta": {"filename": filename, "language": language, "type": "file", "name": os.path.basename(filename)}})
        return chunks
        
    id_types = set(["identifier", "name", "function_name"])
    for fn in func_nodes:
        snippet = code_bytes[fn.start_byte:fn.end_byte].decode("utf8")
        name = None
        
        # Try to extract a meaningful name for the function/method
        name_nodes = find_nodes(fn, id_types)
        if name_nodes:
            try:
                # Use the first identifier node found as the name
                name = code_bytes[name_nodes[0].start_byte:name_nodes[0].end_byte].decode("utf8")
            except Exception:
                pass

        chunks.append({"text": snippet, "meta": {"filename": filename, "language": language, "type": "function", "name": name}})
    return chunks

def index_directory(root_dir: str, extensions: list):
    """Scans a directory for code files and extracts all chunks."""
    filepaths = []
    for ext in extensions:
        filepaths.extend(glob.glob(os.path.join(root_dir, f"**/*{ext}"), recursive=True))
        
    all_chunks = []
    for fp in filepaths:
        try:
            with open(fp, "r", encoding="utf8") as f:
                code = f.read()
        except Exception:
            continue
            
        lang = EXT_LANG_MAP.get(os.path.splitext(fp)[1].lower(), "text")
        chunks = extract_chunks_from_code(code, lang, fp)
        
        for c in chunks:
            c["meta"]["filepath"] = os.path.abspath(fp)
        all_chunks.extend(chunks)
        
    return all_chunks

def build_faiss_index(chunks):
    """Generates embeddings and builds the FAISS index."""
    texts = [c["text"] for c in chunks]
    embs = embed_text(texts, batch_size=32)  # Increased batch size for speed
    dim = embs.shape[1]
    
    # Normalize embeddings to unit vectors for similarity search (Inner Product)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    embs = embs / np.clip(norms, 1e-9, None)
    
    index = faiss.IndexFlatIP(dim)
    index.add(embs)
    metas = [c["meta"] for c in chunks]
    
    return index, metas, embs
