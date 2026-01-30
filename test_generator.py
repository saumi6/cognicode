import os
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import traceback

from gemini_client import GeminiClient
from utils import FunctionAnalyzer
from config import Config

class TestGenerator:
    def __init__(self, verbose: bool = False):
        self.client = GeminiClient()
        self.verbose = verbose
        
    def generate_tests(self, file_path: str, function_name: str) -> Dict[str, Any]:
        """Generate test cases for a specific function."""
        try:
            # Create analyzer for this specific file
            analyzer = FunctionAnalyzer(file_path)
            
            # Analyze the function
            func_info = analyzer.analyze_function(function_name)
            if not func_info:
                return {
                    'success': False,
                    'error': f"Function '{function_name}' not found in {file_path}",
                    'output_file': None,
                    'test_count': 0
                }
            
            if self.verbose:
                print(f"📊 Function analysis complete: {func_info['name']}")
                print(f"   Signature: {func_info['signature']}")
                print(f"   Parameters: {len(func_info['parameters'])}")
            
            # Generate test cases using LLM
            test_code = self._generate_test_code(func_info, file_path)
            if not test_code:
                return {
                    'success': False,
                    'error': "Failed to generate test code - LLM returned empty response",
                    'output_file': None,
                    'test_count': 0
                }
            
            if self.verbose:
                print(f"✅ Generated {len(test_code)} characters of test code")
            
            # Clean up the generated code
            test_code = self._clean_generated_code(test_code, function_name)
            
            # Create output file
            output_file = self._create_output_file(file_path, function_name, test_code, func_info)
            
            # Count test cases (rough estimate)
            test_count = len(re.findall(r'def test_', test_code))
            
            return {
                'success': True,
                'error': None,
                'output_file': output_file,
                'test_count': test_count
            }
            
        except Exception as e:
            error_msg = f"Error in generate_tests: {str(e)}"
            if self.verbose:
                error_msg += f"\nFull traceback:\n{traceback.format_exc()}"
            return {
                'success': False,
                'error': error_msg,
                'output_file': None,
                'test_count': 0
            }


    def _generate_test_code(self, func_info: Dict, file_path: str) -> str:
        """Generate test code using Gemini LLM."""
        
        try:
            func_name = func_info['name']
            
            prompt = f"""GENERATE COMPLETE PYTEST CODE FOR {func_name} FUNCTION.

    CRITICAL RULES:
    1. EVERY function must have COMPLETE implementation with actual working code
    2. NO empty function bodies allowed
    3. NO placeholder comments
    4. MUST use correct indentation (4 spaces)
    5. MUST include actual assert statements and pytest.raises blocks
    6. Do NOT import any modules, all the necessary modules will be imported retroactively, you just have to give test cases

    GENERATE THIS EXACT CODE STRUCTURE:

    ```python
    @pytest.mark.parametrize("n, expected", [
        (0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (8, 21), (10, 55)
    ])
    def test_{func_name}_normal_cases(n, expected):
        \"\"\"Test {func_name} with valid inputs\"\"\"
        result = {func_name}(n)
        assert result == expected

    def test_{func_name}_edge_cases():
        \"\"\"Test {func_name} with edge cases\"\"\"
        assert {func_name}(0) == 0
        assert {func_name}(1) == 1
        assert {func_name}(2) == 1

    def test_{func_name}_error_cases():
        \"\"\"Test {func_name} with invalid inputs\"\"\"
        with pytest.raises(ValueError):
            {func_name}(-1)
        with pytest.raises(ValueError):
            {func_name}(-5)
        with pytest.raises(ValueError):
            {func_name}(-100)
    ```

    COPY THE EXACT FORMAT ABOVE. Replace {func_name} with the actual function name. 
    Make sure EVERY function has complete working code inside.

    Generate ONLY the test functions with complete implementations:"""

            response = self.client.generate_content(prompt)
            
            if self.verbose and response:
                print(f"✅ Received response: {len(response)} characters")
                print(f"   Preview: {response[:300]}...")
            
            if not response:
                return None
            
            # Extract code from response
            code_match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            return response.strip()
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Error in _generate_test_code: {e}")
            return None
        
    def _clean_generated_code(self, code: str, target_function_name: str) -> str:
        """Clean up the generated code by removing unwanted elements."""
        lines = code.split('\n')
        cleaned_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            original_line = lines[i]
            
            # Skip empty lines at the beginning
            if not line and not cleaned_lines:
                i += 1
                continue
            
            # Remove separator lines and headers
            if ('=' in line and len(line) > 10) or line.upper().startswith('# GENERATED'):
                i += 1
                continue
            
            # Skip duplicate imports (basic check)
            if line.startswith(('import pytest', 'from unittest.mock')) and any('import pytest' in cl or 'from unittest.mock' in cl for cl in cleaned_lines):
                i += 1
                continue
            
            # Check for duplicate function definition
            if line.startswith('def ') and target_function_name in line and not line.startswith('def test_'):
                # This is likely the duplicate function definition - skip the entire function
                i = self._skip_function_block(lines, i)
                continue
            
            # Fix import statements (replace generic module names)
            if 'from my_module import' in line or 'from your_module import' in line:
                # Skip this line - we'll handle imports in the header
                i += 1
                continue
            
            # Skip comments about importing from modules
            if line.startswith('#') and ('from your_module' in line or 'from my_module' in line):
                i += 1
                continue
            
            cleaned_lines.append(original_line)
            i += 1
        
        # Join the lines back and clean up
        cleaned_code = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive empty lines
        cleaned_code = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_code)
        
        return cleaned_code.strip()
    
    def _skip_function_block(self, lines: List[str], start_idx: int) -> int:
        """Skip an entire function block and return the next line index."""
        i = start_idx + 1
        base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
        
        while i < len(lines):
            line = lines[i]
            if line.strip():  # Non-empty line
                current_indent = len(line) - len(line.lstrip())
                # If we've returned to the base indentation level or less, we're done
                if current_indent <= base_indent:
                    break
            i += 1
        
        return i
    
    def _create_output_file(self, file_path: str, function_name: str, test_code: str, func_info: Dict) -> str:
        """Create the output test file."""
        # Ensure output directory exists
        output_dir = Path(Config.OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)
        
        # Create output filename
        source_name = Path(file_path).stem
        output_filename = f"test_{source_name}_{function_name}.py"
        output_file = output_dir / output_filename
        
        # Get the absolute path to the source file directory
        source_dir = os.path.abspath(os.path.dirname(file_path))
        
        # Create the complete test file content with clean header
        header = f'''"""
Auto-generated test cases for function: {function_name}
Generated on: {self._get_timestamp()}
Source file: {Path(file_path).name}
Function signature: {func_info['signature']}
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add the directory containing the source file to Python path
sys.path.insert(0, r"{source_dir}")

# Import the function to be tested
from {source_name} import {function_name}

'''
        
        # Combine header with generated test code
        complete_content = header + test_code
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        
        return str(output_file)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for file headers."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_functions_from_file(self, file_path: str) -> List[Dict]:
        """Get all functions from a Python file."""
        analyzer = FunctionAnalyzer(file_path)
        return analyzer.get_all_functions()
    
    def analyze_function(self, file_path: str, function_name: str) -> Optional[Dict]:
        """Analyze a specific function."""
        analyzer = FunctionAnalyzer(file_path)
        return analyzer.analyze_function(function_name)

    def generate_tests_for_function(self, file_path: str, function_name: str, output_file: str = None) -> Tuple[bool, str]:
        """Generate tests for a specific function - wrapper for CLI compatibility."""
        result = self.generate_tests(file_path, function_name)
        
        if result['success']:
            return True, f"Tests generated successfully! Output: {result['output_file']} ({result['test_count']} test cases)"
        else:
            return False, result['error']
    
    def generate_tests_for_all_functions(self, file_path: str, output_dir: str = None) -> Tuple[bool, str]:
        """Generate tests for all functions in a file."""
        functions = self.get_functions_from_file(file_path)
        
        if not functions:
            return False, "No functions found in the file"
        
        results = []
        for func_info in functions:
            result = self.generate_tests(file_path, func_info['name'])
            results.append(result)
        
        successful = sum(1 for r in results if r['success'])
        total_tests = sum(r.get('test_count', 0) for r in results if r['success'])
        
        if successful == 0:
            return False, "Failed to generate tests for any function"
        elif successful == len(results):
            return True, f"Successfully generated tests for all {successful} functions ({total_tests} total test cases)"
        else:
            return True, f"Generated tests for {successful}/{len(results)} functions ({total_tests} total test cases)"
    
    def list_functions_in_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """List all functions in a file - returns success flag and list of function names."""
        try:
            functions = self.get_functions_from_file(file_path)
            function_names = [f['name'] for f in functions]
            return True, function_names
        except Exception as e:
            return False, [str(e)]
    
    def get_function_info(self, file_path: str, function_name: str) -> Tuple[bool, Dict]:
        """Get detailed function information."""
        try:
            func_info = self.analyze_function(file_path, function_name)
            if func_info:
                return True, func_info
            else:
                return False, {'error': f"Function '{function_name}' not found"}
        except Exception as e:
            return False, {'error': str(e)}