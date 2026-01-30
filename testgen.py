#!/usr/bin/env python3
"""
Automatic Test Case Generator CLI
A command-line utility for generating pytest test cases using Gemini LLM

Usage:
    python pytest.py generate <file_path> <function_name> [options]
    python pytest.py generate-all <file_path> [options]
    python pytest.py list <file_path>
    python pytest.py info <file_path> <function_name>
"""

import click
import os
import sys
from pathlib import Path
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_generator import TestGenerator
from config import Config

class Colors:
    """Color constants for terminal output"""
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    HIGHLIGHT = Fore.MAGENTA
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def print_banner():
    """Print the application banner"""
    banner = f"""
{Colors.HIGHLIGHT}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║              🤖 AUTOMATIC TEST CASE GENERATOR 🤖              ║
║                    Powered by Gemini LLM                    ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.SUCCESS}✅ {message}{Colors.RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.ERROR}❌ {message}{Colors.RESET}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.RESET}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.INFO}ℹ️  {message}{Colors.RESET}")

def validate_file_path(file_path: str) -> bool:
    """Validate that the file path exists and is a Python file"""
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return False
    
    if not file_path.endswith('.py'):
        print_error("File must be a Python file (.py)")
        return False
    
    return True

def check_configuration():
    """Check if the configuration is valid"""
    try:
        Config.validate()
        return True
    except ValueError as e:
        print_error(f"Configuration Error: {e}")
        print_info("Please check your .env file or environment variables")
        print_info("Copy .env.example to .env and fill in your Gemini API key")
        return False

@click.group()
@click.version_option(version="1.0.0", prog_name="pytest-generator")
def cli():
    """Automatic Test Case Generator - Generate pytest test cases using Gemini LLM"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('function_name', type=str)
@click.option('--output', '-o', type=str, help='Output file path for generated tests')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--no-banner', is_flag=True, help='Disable banner display')
def generate(file_path: str, function_name: str, output: str, verbose: bool, no_banner: bool):
    """Generate test cases for a specific function"""
    
    if not no_banner:
        print_banner()
    
    # Validate configuration
    if not check_configuration():
        sys.exit(1)
    
    # Validate file path
    if not validate_file_path(file_path):
        sys.exit(1)
    
    try:
        # Initialize test generator
        if verbose:
            print_info(f"Initializing test generator...")
        
        generator = TestGenerator(verbose=verbose)
        
        # Generate tests
        print_info(f"Generating tests for function '{function_name}' in {file_path}")
        
        success, message = generator.generate_tests_for_function(
            file_path, function_name, output
        )
        
        if success:
            print_success(message)
            
            # Show additional info if verbose
            if verbose:
                success_info, func_info = generator.get_function_info(file_path, function_name)
                if success_info:
                    print_info(f"Function complexity: {func_info.get('complexity', 'Unknown')}")
                    print_info(f"Parameters: {len(func_info.get('parameters', []))}")
                    print_info(f"Has docstring: {'Yes' if func_info.get('docstring') else 'No'}")
        else:
            print_error(message)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_warning("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

@cli.command('generate-all')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output-dir', '-d', type=str, help='Output directory for generated tests')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--no-banner', is_flag=True, help='Disable banner display')
def generate_all(file_path: str, output_dir: str, verbose: bool, no_banner: bool):
    """Generate test cases for all functions in a file"""
    
    if not no_banner:
        print_banner()
    
    # Validate configuration
    if not check_configuration():
        sys.exit(1)
    
    # Validate file path
    if not validate_file_path(file_path):
        sys.exit(1)
    
    try:
        # Initialize test generator
        if verbose:
            print_info("Initializing test generator...")
        
        generator = TestGenerator(verbose=verbose)
        
        # List functions first
        success_list, functions = generator.list_functions_in_file(file_path)
        if not success_list:
            print_error(f"Error: {functions[0] if functions else 'Unknown error'}")
            sys.exit(1)
        
        if not functions:
            print_warning("No functions found in the file")
            sys.exit(0)
        
        print_info(f"Found {len(functions)} functions: {', '.join(functions)}")
        
        # Confirm with user
        if not click.confirm(f"Generate tests for all {len(functions)} functions?"):
            print_info("Operation cancelled")
            sys.exit(0)
        
        # Generate tests for all functions
        print_info(f"Generating tests for all functions in {file_path}")
        
        success, message = generator.generate_tests_for_all_functions(
            file_path, output_dir
        )
        
        if success:
            print_success(message)
        else:
            print_error(message)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_warning("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def list(file_path: str, verbose: bool):
    """List all functions in a Python file"""
    
    # Validate file path
    if not validate_file_path(file_path):
        sys.exit(1)
    
    try:
        generator = TestGenerator(verbose=verbose)
        success, functions = generator.list_functions_in_file(file_path)
        
        if not success:
            print_error(f"Error: {functions[0] if functions else 'Unknown error'}")
            sys.exit(1)
        
        if not functions:
            print_warning("No functions found in the file")
        else:
            print_info(f"Functions found in {os.path.basename(file_path)}:")
            for i, func in enumerate(functions, 1):
                print(f"  {Colors.HIGHLIGHT}{i:2d}.{Colors.RESET} {func}")
            
            print_info(f"Total: {len(functions)} function{'s' if len(functions) != 1 else ''}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('function_name', type=str)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def info(file_path: str, function_name: str, verbose: bool):
    """Get detailed information about a specific function"""
    
    # Validate file path
    if not validate_file_path(file_path):
        sys.exit(1)
    
    try:
        generator = TestGenerator(verbose=verbose)
        success, func_info = generator.get_function_info(file_path, function_name)
        
        if not success:
            print_error(func_info.get('error', 'Unknown error'))
            sys.exit(1)
        
        # Display function information
        print_info(f"Function Information: {function_name}")
        print("="*60)
        
        print(f"{Colors.BOLD}Signature:{Colors.RESET}")
        print(f"  {func_info.get('signature', 'N/A')}")
        
        print(f"\n{Colors.BOLD}Parameters:{Colors.RESET}")
        params = func_info.get('parameters', [])
        if params:
            for param in params:
                default_info = f" = {param['default_value']}" if param['has_default'] else ""
                print(f"  • {param['name']}: {param['type']}{default_info} ({param['kind']})")
        else:
            print("  No parameters")
        
        print(f"\n{Colors.BOLD}Return Type:{Colors.RESET} {func_info.get('return_type', 'Any')}")
        
        print(f"\n{Colors.BOLD}Complexity:{Colors.RESET} {func_info.get('complexity', 'Unknown')}")
        
        print(f"\n{Colors.BOLD}Line Number:{Colors.RESET} {func_info.get('line_number', 'Unknown')}")
        
        print(f"\n{Colors.BOLD}Async Function:{Colors.RESET} {'Yes' if func_info.get('is_async') else 'No'}")
        
        decorators = func_info.get('decorators', [])
        if decorators:
            print(f"\n{Colors.BOLD}Decorators:{Colors.RESET}")
            for decorator in decorators:
                print(f"  @{decorator}")
        
        docstring = func_info.get('docstring')
        if docstring:
            print(f"\n{Colors.BOLD}Docstring:{Colors.RESET}")
            print(f"  {docstring}")
        else:
            print(f"\n{Colors.BOLD}Docstring:{Colors.RESET} None")
        
        if verbose:
            print(f"\n{Colors.BOLD}Function Code:{Colors.RESET}")
            print("-" * 40)
            print(func_info.get('code', 'N/A'))
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)

@cli.command()
def config():
    """Show current configuration"""
    print_info("Current Configuration:")
    print("="*40)
    
    try:
        Config.validate()
        print(f"{Colors.SUCCESS}✅ Gemini API Key: {'*' * 20} (configured){Colors.RESET}")
    except ValueError:
        print(f"{Colors.ERROR}❌ Gemini API Key: Not configured{Colors.RESET}")
    
    print(f"📊 Max Test Cases: {Config.MAX_TEST_CASES}")
    print(f"🔍 Include Edge Cases: {Config.INCLUDE_EDGE_CASES}")
    print(f"⚠️  Include Error Cases: {Config.INCLUDE_ERROR_CASES}")
    print(f"📁 Output Directory: {Config.OUTPUT_DIR}")
    print(f"🔊 Verbose Mode: {Config.VERBOSE}")
    print(f"🤖 Gemini Model: {Config.GEMINI_MODEL}")

@cli.command()
def setup():
    """Interactive setup wizard"""
    print_banner()
    print_info("Welcome to the Test Generator Setup Wizard!")
    print()
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print_warning(".env file already exists")
        if not click.confirm("Do you want to overwrite it?"):
            print_info("Setup cancelled")
            return
    
    # Get API key
    api_key = click.prompt("Enter your Gemini API Key", type=str, hide_input=True)
    
    # Get other configurations
    model = click.prompt("Gemini model", default="gemini-pro", type=str)
    max_tests = click.prompt("Maximum test cases per function", default=10, type=int)
    include_edge = click.confirm("Include edge cases?", default=True)
    include_error = click.confirm("Include error cases?", default=True)
    output_dir = click.prompt("Output directory", default="generated_tests", type=str)
    
    # Create .env file
    env_content = f"""# Gemini API Configuration
GEMINI_API_KEY={api_key}
GEMINI_MODEL={model}

# Test Generation Settings
MAX_TEST_CASES={max_tests}
INCLUDE_EDGE_CASES={str(include_edge).lower()}
INCLUDE_ERROR_CASES={str(include_error).lower()}

# Output Settings
OUTPUT_DIR={output_dir}
VERBOSE=false
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print_success("Configuration saved to .env file!")
    print_info("You can now use the test generator.")

if __name__ == '__main__':
    cli()