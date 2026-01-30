import os
import argparse
import pickle
from search_core.indexing import index_directory, build_faiss_index, EXT_LANG_MAP
from search_core.retrieval import retrieve, format_result

# --- Setup Paths ---
# We use os.path.join and os.getcwd() to make the paths relative to the project root.
# This ensures it works no matter where the script is run from.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# The directory to index is defined by the .env file, but for a local project, 
# we'll assume the codebase is right next to the script.
# We'll default to the current working directory or a specified project name.
DEFAULT_CODE_PATH = os.path.join(ROOT_DIR, 'my_api_server')
INDEX_FILE = os.path.join(ROOT_DIR, 'index_data.pkl')

def save_index(index, metas, filepath):
    """Saves the FAISS index and metadata to a file using pickle."""
    print(f"Saving index to {filepath}...")
    with open(filepath, 'wb') as f:
        pickle.dump({'index': index, 'metas': metas}, f)
    print("Index saved successfully.")

def load_index(filepath):
    """Loads the FAISS index and metadata from a file."""
    if not os.path.exists(filepath):
        print(f"Index file not found at {filepath}. Please run with the --build flag first.")
        return None, None
    print(f"Loading index from {filepath}...")
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    print("Index loaded successfully.")
    return data['index'], data['metas']

def main():
    parser = argparse.ArgumentParser(description="Semantic Code Search Engine.")
    parser.add_argument("query", nargs='?', default=None, help="The natural language query to search for (e.g., 'function for API key authentication').")
    parser.add_argument("--build", action="store_true", help="Build the search index from the codebase and save it to disk.")
    parser.add_argument("--path", default=DEFAULT_CODE_PATH, help="Root path of the codebase to index.")
    parser.add_argument("--top_k", type=int, default=3, help="Number of top results to return.")
    
    args = parser.parse_args()

    # --- 1. Index Building Mode ---
    if args.build:
        # Only index Python files in the my_api_server example
        extensions_to_index = ['.py'] 
        print(f"Indexing code in: {args.path}")
        
        # Run the full indexing pipeline
        all_chunks = index_directory(args.path, extensions=extensions_to_index)
        print(f"Extracted {len(all_chunks)} code chunks.")
        
        if not all_chunks:
            print("No searchable code found. Exiting.")
            return

        faiss_index, metas, _ = build_faiss_index(all_chunks)
        
        # Save the index and metadata
        save_index(faiss_index, metas, INDEX_FILE)
        print("Build complete. Ready to search.")
        return

    # --- 2. Search Mode ---
    if args.query:
        # Load the index before searching
        faiss_index, metas = load_index(INDEX_FILE)
        
        if faiss_index is None:
            return
            
        print(f"\nSearching for: '{args.query}'...")
        
        # Perform the retrieval
        results = retrieve(args.query, faiss_index, metas, top_k=args.top_k)
        
        # Format and display results
        print("\n" + "="*80)
        print("          ✨ SEMANTIC CODE SEARCH RESULTS ✨")
        print("="*80)
        
        # Note: format_result re-reads the file to display the snippet
        for i, result in enumerate(results):
            # Pass the base path so format_result can calculate the relative path
            formatted_output = format_result(result, all_chunks=[], base_path=args.path)
            print(f"RESULT #{i + 1}:")
            print(formatted_output)

    else:
        # If neither --build nor a query is provided
        parser.print_help()


if __name__ == "__main__":
    main()
