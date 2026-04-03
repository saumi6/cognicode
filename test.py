"""
Generate and run tests using Groq test generator
"""
import argparse
import sys
import subprocess
import os
import json
import re
import urllib.request
import urllib.error
from pathlib import Path

# Force UTF-8 encoding for standard output to avoid Windows console charmap errors
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Server URL for reporting results
SERVER_URL = "http://127.0.0.1:8000/tests/result"

def report_to_server(file_path, status, error=None, coverage_percent=None):
    """Send test result to CogniServer"""
    try:
        # Use absolute path for consistency
        abs_path = str(Path(file_path).resolve())
        data = {
            "file_path": abs_path, 
            "status": status,
            "error": error,
            "coverage_percent": coverage_percent,
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

def _parse_coverage_total(output: str) -> float:
    """
    Parse the pytest-cov terminal output for the TOTAL line.
    Example line:  TOTAL      100     15     85%
    Returns the coverage percentage as a float (e.g. 85.0),
    or 0.0 if no TOTAL line is found.
    """
    m = re.search(r'^TOTAL\s+\d+\s+\d+\s+(\d+)%', output, re.MULTILINE)
    if m:
        return float(m.group(1))
    return 0.0


def run_pytest(test_file_path, source_file_path=None):
    """Run pytest on the generated test file and return (passed, failed, error, coverage_percent)"""
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
        # Build pytest command
        pytest_cmd = [
            sys.executable, '-m', 'pytest', 
            test_file_path, 
            '-v',           # Verbose output
            '--tb=short',   # Short traceback format
            '--no-header'   # No pytest header
        ]

        # ── pytest-cov integration ────────────────────────────────
        # If we know which source file is being tested, add --cov
        # scoped to that module so we get a per-file coverage report.
        if source_file_path:
            # Ensure it's a relative path before converting to a module name
            # e.g. C:\...\test_repo\address.py -> test_repo/address.py -> test_repo.address
            try:
                p = Path(source_file_path)
                if p.is_absolute():
                    p = p.relative_to(Path.cwd())
                
                module_path = str(p).replace('.py', '').replace('/', '.').replace('\\', '.')
                module_path = module_path.strip('.')
                
                pytest_cmd += [
                    f'--cov={module_path}',
                    '--cov-report=term',    # terminal table output
                ]
            except Exception as e:
                print(f"[Warning] Failed to configure coverage module path: {e}")

        # Run pytest
        result = subprocess.run(
            pytest_cmd,
            capture_output=True, text=True, timeout=60, env=current_env
        )
        
        # Print pytest output
        output_txt = ""
        if result.stdout:
            print(result.stdout)
            output_txt += result.stdout
        if result.stderr:
            print("STDERR:", result.stderr)
            output_txt += result.stderr
        
        # Parse output for counts using regex
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

        # ── Parse coverage from pytest-cov output ─────────────────
        coverage_percent = _parse_coverage_total(output_txt)
        if coverage_percent > 0:
            print(f"[Coverage] {coverage_percent:.0f}%")

        return passed_count, failed_count, error_msg, coverage_percent
            
    except subprocess.TimeoutExpired:
        print("Tests timed out (60s limit)")
        return 0, 0, "Timeout", 0.0
    except FileNotFoundError:
        print("pytest not found. Install with: pip install pytest")
        return 0, 0, "pytest not found", 0.0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return 0, 0, str(e), 0.0

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
    last_coverage_percent = 0.0  # Will hold the latest coverage value

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
            
            p_count, f_count, error_msg, cov_pct = run_pytest(
                result['output_file'],
                source_file_path=args.file_path
            )
            
            total_passed += p_count
            total_run += (p_count + f_count)
            if cov_pct > 0:
                last_coverage_percent = cov_pct
            
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

        # ── AI Diagnosis on failure ──────────────────────────────
        error_payload = None
        if file_status == "FAILED" and file_errors:
            raw_traceback = "\n".join(file_errors)

            # Run the Groq failure analysis (never block the runner)
            ai_diagnosis = ""
            try:
                ai_diagnosis = gen.analyze_test_failure(args.file_path, raw_traceback)
            except Exception:
                ai_diagnosis = "AI Analysis Unavailable."

            # ANSI color codes for terminal output
            CYAN   = "\033[96m"
            YELLOW = "\033[93m"
            RESET  = "\033[0m"
            BOLD   = "\033[1m"

            diagnosis_block = (
                f"\n{CYAN}{BOLD}{'=' * 48}\n"
                f"           ⚡ AI DIAGNOSIS ⚡\n"
                f"{'=' * 48}{RESET}\n"
                f"{YELLOW}{ai_diagnosis}{RESET}\n"
                f"{CYAN}{'=' * 48}{RESET}\n"
            )

            # Print to terminal so the developer sees it immediately
            print(diagnosis_block)

            # Build the server payload (plain text, no ANSI codes)
            error_payload = (
                "================ AI DIAGNOSIS ================\n"
                f"{ai_diagnosis}\n"
                "===============================================\n\n"
                "[Raw Pytest Traceback Follows...]\n"
                f"{raw_traceback}"
            )

        # Report to server
        if not args.no_run:
            print(f"Reporting result to server for {args.file_path}...")
            print(f"[Coverage] Sending coverage_percent={last_coverage_percent}")
            report_to_server(
                args.file_path, 
                file_status, 
                error=error_payload,
                coverage_percent=last_coverage_percent
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