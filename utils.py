import ast
import inspect
import os
import sys
from typing import Dict, List, Optional, Any, Tuple
import importlib.util

class FunctionAnalyzer:
    """Utility class for analyzing Python functions and extracting metadata"""
    
    def __init__(self, file_path: str):
        """
        Initialize analyzer with a Python file path
        
        Args:
            file_path: Path to the Python file to analyze
        """
        self.file_path = os.path.abspath(file_path)
        self.module_name = None
        self.tree = None
        self.source_code = None
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        if not self.file_path.endswith('.py'):
            raise ValueError("File must be a Python file (.py)")
        
        self._load_file()
    
    def _load_file(self):
        """Load and parse the Python file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
            
            self.tree = ast.parse(self.source_code)
            self.module_name = os.path.splitext(os.path.basename(self.file_path))[0]
        except Exception as e:
            raise Exception(f"Failed to load and parse file: {e}")
    
    def get_all_functions(self) -> List[str]:
        """
        Get names of all functions defined in the file
        
        Returns:
            List of function names
        """
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions
    
    def function_exists(self, function_name: str) -> bool:
        """
        Check if a function exists in the file
        
        Args:
            function_name: Name of the function to check
            
        Returns:
            True if function exists, False otherwise
        """
        return function_name in self.get_all_functions()
    
    def analyze_function(self, function_name: str) -> Dict[str, Any]:
        """
        Analyze a specific function and extract its metadata
        
        Args:
            function_name: Name of the function to analyze
            
        Returns:
            Dictionary containing function metadata
        """
        if not self.function_exists(function_name):
            raise ValueError(f"Function '{function_name}' not found in {self.file_path}")
        
        function_node = self._find_function_node(function_name)
        if not function_node:
            raise ValueError(f"Could not locate function '{function_name}'")
        
        return {
            'name': function_name,
            'signature': self._get_function_signature(function_node),
            'parameters': self._get_function_parameters(function_node),
            'return_type': self._get_return_type(function_node),
            'docstring': self._get_docstring(function_node),
            'code': self._get_function_code(function_node),
            'line_number': function_node.lineno,
            'is_async': isinstance(function_node, ast.AsyncFunctionDef),
            'decorators': self._get_decorators(function_node),
            'complexity': self._calculate_complexity(function_node),
            'imports_needed': self._get_imports_needed(),
            'class_context': self._get_class_context(function_node)
        }

    def _get_class_context(self, function_node: ast.FunctionDef) -> Optional[Dict[str, str]]:
        """Check if function belongs to a class and return class info"""
        # This is a simple heuristic since we don't have parent pointers in AST
        # We walk the tree and check if the function node is a direct child of a ClassDef
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item is function_node:
                        # Found the class!
                        return {
                            'class_name': node.name,
                            'class_code': self._get_function_code(node) # Reusing this to get class body
                        }
        return None
    
    def _find_function_node(self, function_name: str) -> Optional[ast.FunctionDef]:
        """Find the AST node for a specific function"""
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
                return node
        return None
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature as string"""
        args = []
        
        # Regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)
        
        # Default arguments
        defaults = node.args.defaults
        if defaults:
            # Apply defaults to the last len(defaults) arguments
            for i, default in enumerate(defaults):
                idx = len(args) - len(defaults) + i
                if idx >= 0:
                    args[idx] += f" = {ast.unparse(default)}"
        
        # *args
        if node.args.vararg:
            vararg = f"*{node.args.vararg.arg}"
            if node.args.vararg.annotation:
                vararg += f": {ast.unparse(node.args.vararg.annotation)}"
            args.append(vararg)
        
        # **kwargs
        if node.args.kwarg:
            kwarg = f"**{node.args.kwarg.arg}"
            if node.args.kwarg.annotation:
                kwarg += f": {ast.unparse(node.args.kwarg.annotation)}"
            args.append(kwarg)
        
        signature = f"def {node.name}({', '.join(args)})"
        
        # Return type annotation
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"
        
        return signature
    
    def _get_function_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract detailed parameter information"""
        parameters = []
        
        # Regular arguments
        for i, arg in enumerate(node.args.args):
            param_info = {
                'name': arg.arg,
                'type': ast.unparse(arg.annotation) if arg.annotation else 'Any',
                'has_default': i >= len(node.args.args) - len(node.args.defaults),
                'default_value': None,
                'kind': 'positional'
            }
            
            # Add default value if present
            if param_info['has_default']:
                default_idx = i - (len(node.args.args) - len(node.args.defaults))
                param_info['default_value'] = ast.unparse(node.args.defaults[default_idx])
            
            parameters.append(param_info)
        
        # *args
        if node.args.vararg:
            parameters.append({
                'name': node.args.vararg.arg,
                'type': ast.unparse(node.args.vararg.annotation) if node.args.vararg.annotation else 'Any',
                'has_default': False,
                'default_value': None,
                'kind': 'var_positional'
            })
        
        # **kwargs
        if node.args.kwarg:
            parameters.append({
                'name': node.args.kwarg.arg,
                'type': ast.unparse(node.args.kwarg.annotation) if node.args.kwarg.annotation else 'Any',
                'has_default': False,
                'default_value': None,
                'kind': 'var_keyword'
            })
        
        return parameters
    
    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation"""
        if node.returns:
            return ast.unparse(node.returns)
        return 'Any'
    
    def _get_docstring(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract function docstring"""
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            
            if isinstance(node.body[0].value, ast.Str):
                return node.body[0].value.s
            elif isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                return node.body[0].value.value
        return None
    
    def _get_function_code(self, node: ast.FunctionDef) -> str:
        """Extract the complete function code"""
        # Get the lines of the source code
        source_lines = self.source_code.split('\n')
        
        # Find the end line of the function
        start_line = node.lineno - 1  # Convert to 0-based indexing
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else self._find_function_end(node, source_lines)
        
        # Extract function code
        function_lines = source_lines[start_line:end_line]
        return '\n'.join(function_lines)
    
    def _find_function_end(self, node: ast.FunctionDef, source_lines: List[str]) -> int:
        """Find the end line of a function (fallback for older Python versions)"""
        start_line = node.lineno - 1
        current_line = start_line + 1
        
        # Simple heuristic: find the next function or class definition, or end of file
        while current_line < len(source_lines):
            line = source_lines[current_line].strip()
            if line.startswith(('def ', 'class ', 'async def ')) and not line.startswith('    '):
                return current_line
            current_line += 1
        
        return len(source_lines)
    
    def _get_decorators(self, node: ast.FunctionDef) -> List[str]:
        """Extract function decorators"""
        decorators = []
        for decorator in node.decorator_list:
            decorators.append(ast.unparse(decorator))
        return decorators
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of the function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _get_imports_needed(self) -> List[str]:
        """Extract import statements from the file"""
        imports = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")
        
        return imports

def load_function_dynamically(file_path: str, function_name: str) -> Optional[callable]:
    """
    Dynamically load a function from a Python file
    
    Args:
        file_path: Path to the Python file
        function_name: Name of the function to load
        
    Returns:
        The loaded function object or None if not found
    """
    try:
        spec = importlib.util.spec_from_file_location("module", file_path)
        if spec is None or spec.loader is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return getattr(module, function_name, None)
    except Exception:
        return None

def validate_python_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a Python file is syntactically correct
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"