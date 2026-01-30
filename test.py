"""
Generate and run tests using Groq test generator
"""
import argparse
import sys
import subprocess
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

# Server URL for reporting results
SERVER_URL = "http://localhost:8000/tests/result"

def report_to_server(file_path, status, error=None):
    """Send test result to CogniServer"""
    try:
        # Use absolute path for consistency
        abs_path = str(Path(file_path).resolve())
        data = {
            "file_path": abs_path, 
            "status": status,
            "error": error
        }
        
        req = urllib.request.Request(
            SERVER_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            pass # Success
            
    except Exception as e:
        # Don't fail the test runner if reporting fails
        print(f"[Warning] Could not report to server: {e}")

def run_pytest(test_file_path):
    """Run pytest on the generated test file and return stats"""
    print(f"\nRunning pytest on {test_file_path}...")
    print("=" * 60)
    
    # Fix PYTHONPATH: Generated tests are in PROJECT_ROOT/generated_tests/
    # Source modules are in PROJECT_ROOT/test_repo/
    # We need PROJECT_ROOT/test_repo in PYTHONPATH
    
    test_file_dir = Path(test_file_path).parent  # .../generated_tests
    project_root = test_file_dir.parent  # .../cognicode
    test_repo_dir = str(project_root / "test_repo")  # .../cognicode/test_repo
    
    current_env = os.environ.copy()
    python_path = current_env.get("PYTHONPATH", "")
    current_env["PYTHONPATH"] = f"{test_repo_dir}{os.pathsep}{python_path}"
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_file_path, 
            '-v',           # Verbose output
            '--tb=short',   # Short traceback format
            '--no-header'   # No pytest header
        ], capture_output=True, text=True, timeout=30, env=current_env)
        
        # Print pytest output
        output_txt = ""
        if result.stdout:
            print(result.stdout)
            output_txt += result.stdout
        if result.stderr:
            print("STDERR:", result.stderr)
            output_txt += result.stderr
        
        # Parse output for counts using regex
        import re
        passed_count = 0
        failed_count = 0
        
        # Look for "X passed"
        m_passed = re.search(r'(\d+) passed', output_txt)
        if m_passed:
            passed_count = int(m_passed.group(1))
            
        # Look for "X failed"
        m_failed = re.search(r'(\d+) failed', output_txt)
        if m_failed:
            failed_count = int(m_failed.group(1))
            
        # Fallback: if exit code 0 and no regex match, assume all passed?
        # Usually pytest prints summary line. If not found, maybe something else wrong.
        # But let's trust regex or exit code.
        
        if result.returncode == 0 and passed_count == 0:
            # Maybe it said "collected X items" and nothing failed? 
            # Or regex failed. But if ret code 0, usually implies success.
            # Let's verify if we missed something.
            # For robustness, we return what we found.
            pass

        error_msg = None
        if result.returncode != 0:
             print(f"Tests failed (exit code: {result.returncode})")
             error_msg = result.stderr if result.stderr else "Tests failed"
             if not result.stderr and result.stdout:
                 lines = result.stdout.splitlines()
                 if lines: error_msg = lines[-1]
        else:
             print("All tests passed!")

        return passed_count, failed_count, error_msg
            
    except subprocess.TimeoutExpired:
        print("Tests timed out (30s limit)")
        return 0, 0, "Timeout"
    except FileNotFoundError:
        print("pytest not found. Install with: pip install pytest")
        return 0, 0, "pytest not found"
    except Exception as e:
        print(f"Error running pytest: {e}")
        return 0, 0, str(e)

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
    
    # Track total stats for file
    total_passed = 0
    total_run = 0
    file_errors = []

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
                file_errors.append(f"{func_name}: Generation failed")
                continue
            
            print(f"Generated {result['test_count']} test cases")
            
            if args.no_run:
                summary_results.append({'function': func_name, 'status': 'SKIPPED', 'details': 'No-run mode'})
                continue
            
            # Step 2: Run the generated tests
            print(f"Step 2: Running generated tests...")
            
            p_count, f_count, error_msg = run_pytest(result['output_file'])
            
            total_passed += p_count
            total_run += (p_count + f_count)
            
            # Status per function
            if f_count > 0 or (p_count == 0 and f_count == 0 and error_msg):
                func_status = 'FAILED'
                global_exit_code = 1
                if error_msg: file_errors.append(f"{func_name}: {error_msg}")
            else:
                func_status = 'PASSED'
                
            summary_results.append({
                'function': func_name, 
                'status': func_status, 
                'details': f"{p_count} passed, {f_count} failed"
            })

        # Calculate Final File Status based on Threshold
        if total_run > 0:
            pass_rate = (total_passed / total_run) * 100
        else:
            pass_rate = 0.0
            
        # User defined threshold: 70%
        THRESHOLD = 70.0
        
        if pass_rate >= THRESHOLD:
            file_status = "PASSED"
            status_symbol = "[PASS]"
        else:
            file_status = "FAILED"
            status_symbol = "[FAIL]"
            
        print(f"\n[Stats] Pass Rate: {pass_rate:.1f}% ({total_passed}/{total_run}) (Threshold: {THRESHOLD}%) -> Status: {file_status}")

        # Final Summary
        print("\n" + "=" * 60)
        print("BATCH TESTING SUMMARY:")
        print(f"{'FUNCTION':<30} | {'STATUS':<10} | {'DETAILS'}")
        print("-" * 60)
        for item in summary_results:
            print(f"{item['function']:<30} | {item['status']:<10} | {item['details']}")
        print("-" * 60)

        # Report to server
        if not args.no_run:
            print(f"Reporting result to server for {args.file_path}...")
            report_to_server(
                args.file_path, 
                file_status, 
                error="\n".join(file_errors) if file_errors and file_status == "FAILED" else None
            )
            print(f"{status_symbol} {os.path.basename(args.file_path)}: {file_status}")

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