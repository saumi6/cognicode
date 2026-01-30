"""
Cleanup script to fix existing generated test files
"""
import os
import re
from pathlib import Path

def clean_test_file(file_path: Path):
    """Clean up a single test file"""
    print(f"🧹 Cleaning {file_path.name}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    cleaned_lines = []
    i = 0
    skip_until_test = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip separator lines
        if '=' in stripped and len(stripped) > 10:
            i += 1
            continue
        
        # Skip "GENERATED TEST CASES" comments
        if 'GENERATED TEST CASES' in stripped:
            i += 1
            continue
        
        # Skip duplicate function definitions (not test functions)
        if stripped.startswith('def ') and not stripped.startswith('def test_'):
            # Skip this function definition
            i = skip_function_definition(lines, i)
            continue
        
        # Fix import statements
        if 'from my_module import' in line or 'from your_module import' in line:
            # Skip - will be handled by proper import in header
            i += 1
            continue
        
        # Skip comments about imports
        if stripped.startswith('#') and ('your_module' in stripped or 'my_module' in stripped):
            i += 1
            continue
        
        # Skip duplicate imports
        if stripped.startswith('import pytest') and any('import pytest' in cl for cl in cleaned_lines):
            i += 1
            continue
        
        cleaned_lines.append(line)
        i += 1
    
    # Write back the cleaned content
    cleaned_content = '\n'.join(cleaned_lines)
    cleaned_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"✅ Cleaned {file_path.name}")

def skip_function_definition(lines, start_idx):
    """Skip a function definition block"""
    i = start_idx + 1
    base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
    
    while i < len(lines):
        if lines[i].strip():
            current_indent = len(lines[i]) - len(lines[i].lstrip())
            if current_indent <= base_indent:
                break
        i += 1
    
    return i

def main():
    """Clean all test files in the generated_tests directory"""
    test_dir = Path('generated_tests')
    
    if not test_dir.exists():
        print("❌ No generated_tests directory found")
        return
    
    test_files = list(test_dir.glob('test_*.py'))
    
    if not test_files:
        print("❌ No test files found")
        return
    
    print(f"🎯 Found {len(test_files)} test files to clean")
    
    for test_file in test_files:
        clean_test_file(test_file)
    
    print(f"\n🎉 Cleaned {len(test_files)} test files successfully!")

if __name__ == "__main__":
    main()