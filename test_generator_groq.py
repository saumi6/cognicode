"""
Test Generator using Groq LLM - Alternative to Gemini
"""
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from groq_client import GroqClient
from utils import FunctionAnalyzer
from config_groq import Config

class TestGeneratorGroq:
    def __init__(self, verbose: bool = False):
        self.client = GroqClient()
        self.verbose = verbose
        
    def generate_tests(self, file_path: str, function_name: str) -> Dict[str, Any]:
        """Generate test cases for a specific function using Groq."""
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
            
            # Generate test cases using Groq
            test_code = self._generate_test_code_groq(func_info, file_path)
            if not test_code:
                return {
                    'success': False,
                    'error': "Failed to generate test code - Groq returned empty response",
                    'output_file': None,
                    'test_count': 0
                }
            
            if self.verbose:
                print(f"✅ Generated {len(test_code)} characters of test code")
            
            # Clean up the generated code
            test_code = self._clean_generated_code(test_code, function_name)
            
            # Create output file
            output_file = self._create_output_file(file_path, function_name, test_code, func_info)
            
            # Count test cases
            test_count = len(re.findall(r'def test_', test_code))
            
            return {
                'success': True,
                'error': None,
                'output_file': output_file,
                'test_count': test_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error: {str(e)}",
                'output_file': None,
                'test_count': 0
            }
    
    def _generate_test_code_groq(self, func_info: Dict, file_path: str) -> str:
        """Generate test code using Groq with a focused prompt."""
        
        func_name = func_info['name']
        signature = func_info['signature']
        params = func_info.get('parameters', [])
        docstring = func_info.get('docstring', '')
        
        # Determine the source file stem for prompt context
        source_file_stem = Path(file_path).stem
        
        # Create a very specific prompt for Groq
        class_context = func_info.get('class_context')
        context_str = ""
        param_hint = ""
        
        if class_context:
            context_str = f"""
CONTEXT: This function is a method of class '{class_context['class_name']}'.
Here is the class definition:
```python
{class_context['class_code']}
```
IMPORTANT: You MUST instantiate the class '{class_context['class_name']}' in your tests before calling '{func_name}'.
If the class requires dependencies (like other classes), mock them using `unittest.mock.Mock` or `MagicMock`.
"""
            param_hint = "- Ensure to initialize the class with required arguments (or mocks) in every test case."
        
        prompt = f"""Generate complete pytest test functions for this Python function:

FUNCTION: {signature}
DOCSTRING: {docstring}
{context_str}

Generate exactly 3 complete test functions with full implementations:

1. test_{func_name}_normal_cases() - with @pytest.mark.parametrize and multiple test cases
2. test_{func_name}_edge_cases() - with boundary conditions and edge cases
3. test_{func_name}_error_cases() - with pytest.raises for invalid inputs

Requirements:
- Each function must have complete implementation with assertions
- Use realistic test values based on the function purpose
- Include proper docstrings
- Use pytest.mark.parametrize where appropriate
- Handle exceptions with pytest.raises (example: `with pytest.raises(ValueError):`). DO NOT pass a `msg=` argument to pytest.raises, as it is not supported in newer versions.
- For floating point comparisons, usage `pytest.approx` or `math.isclose`. Do NOT inspect precision errors manually.
- Do NOT import any modules, do not assume any module the user has made, you can import standard modules available in pyhthon only if absolutely necessary, all the necessary modules will be imported retroactively, you just have to give test cases
- **CRITICAL: When using `monkeypatch.setattr`, YOU MUST USE THE FULL ABSOLUTE IMPORT PATH to the function being patched.**
  - WRONG: `monkeypatch.setattr("round_currency", lambda x: x)`
  - WRONG: `monkeypatch.setattr("product.round_currency", lambda x: x)`
  - CORRECT: `monkeypatch.setattr("test_repo.{source_file_stem}.round_currency", lambda x: x)` (where `{source_file_stem}` is the file name without extension)
{param_hint}


Example format:
```python
@pytest.mark.parametrize("input_val, expected", [
    (1, 1), (2, 2), (5, 5)
])
def test_{func_name}_normal_cases(input_val, expected):
    \"\"\"Test normal cases\"\"\"
    result = {func_name}(input_val)
    assert result == expected
```

Generate complete, executable test functions:"""

        try:
            if self.verbose:
                print("🤖 Sending request to Groq...")
            
            response = self.client.generate_content(prompt)
            
            if self.verbose and response:
                print(f"✅ Received response from Groq: {len(response)} characters")
            
            return response
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Error with Groq: {e}")
            return None
    
    def _clean_generated_code(self, code: str, target_function_name: str) -> str:
        """Clean up the generated code."""
        # Remove code block markers
        code = re.sub(r'```python\s*', '', code)
        code = re.sub(r'```\s*$', '', code)
        
        # Remove duplicate imports and comments
        # Also sanitize for weird unicode characters (like non-breaking hyphens)
        code = code.encode('ascii', 'ignore').decode('ascii')
        
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Skip empty lines at start
            if not stripped and not cleaned_lines:
                continue
            # Skip duplicate imports
            if stripped.startswith('import pytest') and any('import pytest' in cl for cl in cleaned_lines):
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _create_output_file(self, file_path: str, function_name: str, test_code: str, func_info: Dict) -> str:
        """Create the output test file."""
        # Same implementation as original but with Groq attribution
        output_dir = Path(Config.OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)
        
        source_name = Path(file_path).stem
        output_filename = f"test_{source_name}_{function_name}_groq.py"
        output_file = output_dir / output_filename
        
        source_dir = os.path.abspath(os.path.dirname(file_path))
        
# Find the package root
        current_dir = Path(source_dir).resolve()
        package_parts = []
        
        print(f"DEBUG: Searching for package root starting at {current_dir}")
        
        # Walk up looking for __init__.py
        while (current_dir / "__init__.py").exists():
            print(f"DEBUG: Found __init__.py in {current_dir}")
            package_parts.insert(0, current_dir.name)
            current_dir = current_dir.parent
            
        print(f"DEBUG: Package parts found: {package_parts}")

        # Check if it's a class method to adjust import
        class_context = func_info.get('class_context')
        import_target = class_context['class_name'] if class_context else function_name

        # If we found it's part of a package
        if package_parts:
            root_path = str(current_dir)
            module_path = ".".join(package_parts + [source_name])
            sys.path.insert(0, root_path)
            import_stmt = f"from {module_path} import {import_target}"
            print(f"Detected package structure. Root: {root_path}, Module: {module_path}")
        else:
            # Standalone file
            sys.path.insert(0, source_dir)
            import_stmt = f"from {source_name} import {import_target}"

        header = f'''"""
Auto-generated test cases for function: {function_name}
Generated using: Groq LLM ({Config.GROQ_MODEL})
Generated on: {self._get_timestamp()}
Source file: {Path(file_path).name}
Function signature: {func_info['signature']}
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"{root_path if package_parts else source_dir}")

# Import the function to be tested
{import_stmt}

'''
        
        complete_content = header + test_code
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        
        return str(output_file)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")