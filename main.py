import argparse
import sys
import os
from file_parser import get_function_source
from gemini_client import generate_tests

def main():
    """
    The main function for the command-line utility.
    It parses arguments, extracts the target function's source code,
    and calls the Gemini API to generate tests.
    """
    parser = argparse.ArgumentParser(
        description="Generate pytest test cases for a specific Python function using Gemini.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file_path", help="The path to the Python file containing the function.")
    parser.add_argument("function_name", help="The name of the function to test.")
    
    args = parser.parse_args()

    try:
        print(f"🔍 Analyzing '{args.function_name}' in '{args.file_path}'...")
        # Extract the source code of the target function
        source_code = get_function_source(args.file_path, args.function_name)
        
        # Get the module name from the file path to use in the import statement
        module_name = os.path.splitext(os.path.basename(args.file_path))[0]
        
        print(f"🤖 Calling Gemini to generate test cases for '{args.function_name}'...")
        # Generate the test cases using the Gemini client
        generated_tests = generate_tests(source_code, args.function_name, module_name)
        
        print("\n" + "="*20 + " Generated Tests " + "="*20)
        print(generated_tests)
        print("="*57 + "\n")

    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'", file=sys.stderr)
        sys.exit(1)
    except AttributeError:
        print(f"Error: Function '{args.function_name}' not found or is not a callable function in '{args.file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
