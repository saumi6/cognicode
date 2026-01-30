"""
Generate and run tests using Groq test generator
"""
import argparse
import sys
import subprocess
from pathlib import Path

def run_pytest(test_file_path):
    """Run pytest on the generated test file"""
    print(f"\nRunning pytest on {test_file_path}...")
    print("=" * 60)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_file_path, 
            '-v',           # Verbose output
            '--tb=short',   # Short traceback format
            '--no-header'   # No pytest header
        ], capture_output=True, text=True, timeout=30)
        
        # Print pytest output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Check results
        if result.returncode == 0:
            print("All tests passed!")
            return True
        else:
            print(f"Tests failed (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print("Tests timed out (30s limit)")
        return False
    except FileNotFoundError:
        print("pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False

def main():
    """Main function with command-line argument parsing"""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate pytest test cases using Groq and run them",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file_path", 
        help="Path to the Python file containing the function"
    )
    parser.add_argument(
        "function_name", 
        nargs='?', # Optional argument
        help="Name of the function to test (optional, defaults to all functions)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-run", 
        action="store_true", 
        help="Generate tests but don't run them"
    )
    
    args = parser.parse_args()

    # Validate file path
    if not Path(args.file_path).exists():
        print(f"Error: File '{args.file_path}' not found")
        sys.exit(1)
    
    print(f"Source File: {args.file_path}")
    print(f"Verbose: {args.verbose}")
    print("-" * 60)
    
    try:
        # Determine which functions to test
        functions_to_test = []
        if args.function_name:
            functions_to_test.append(args.function_name)
        else:
            print("No function specified. Scanning file for all functions...")
            from utils import FunctionAnalyzer
            analyzer = FunctionAnalyzer(args.file_path)
            functions_to_test = analyzer.get_all_functions()
            print(f"Found {len(functions_to_test)} functions: {', '.join(functions_to_test)}")

        if not functions_to_test:
            print("No functions found to test.")
            sys.exit(0)

        # Import generator
        from test_generator_groq import TestGeneratorGroq
        gen = TestGeneratorGroq(verbose=args.verbose)
        
        # Track results
        summary_results = []
        global_exit_code = 0

        for func_name in functions_to_test:
            print(f"\n" + "="*30)
            print(f" Processing Function: {func_name} ")
            print("="*30)
            
            # Step 1: Generate tests
            print(f"Step 1: Generating tests for '{func_name}'...")
            
            result = gen.generate_tests(args.file_path, func_name)
            
            if not result['success']:
                print(f"Test generation failed for {func_name}: {result['error']}")
                summary_results.append({'function': func_name, 'status': 'GEN_FAIL', 'details': result['error']})
                global_exit_code = 1
                continue
            
            print(f"Generated {result['test_count']} test cases")
            
            if args.no_run:
                summary_results.append({'function': func_name, 'status': 'SKIPPED', 'details': 'No-run mode'})
                continue
            
            # Step 2: Run the generated tests
            print(f"Step 2: Running generated tests...")
            test_passed = run_pytest(result['output_file'])
            
            status = 'PASSED' if test_passed else 'FAILED'
            summary_results.append({'function': func_name, 'status': status, 'details': f"{result['test_count']} tests"})
            
            if not test_passed:
                global_exit_code = 1

        # Final Summary
        print("\n" + "=" * 60)
        print("BATCH TESTING SUMMARY:")
        print(f"{'FUNCTION':<30} | {'STATUS':<10} | {'DETAILS'}")
        print("-" * 60)
        for item in summary_results:
            print(f"{item['function']:<30} | {item['status']:<10} | {item['details']}")
        print("-" * 60)

        sys.exit(global_exit_code)
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure test_generator_groq.py and utils.py are in the same directory")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()