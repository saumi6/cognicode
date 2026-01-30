"""
Auto-generated test cases for function: fibonacci
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 19:28:20
Source file: math_utils.py
Function signature: def fibonacci(n: int) -> int
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add the directory containing the source file to Python path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode\examples")

# Import the function to be tested
from math_utils import fibonacci

import pytest

# ------------------------------------------------------------------
# Normal cases – a variety of Fibonacci numbers
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (20, 6765),
        (30, 832040),
    ],
)
def test_fibonacci_normal_cases(input_val, expected):
    """Test that fibonacci returns the correct value for a range of normal inputs."""
    result = fibonacci(input_val)
    assert result == expected, f"fibonacci({input_val}) should be {expected}, got {result}"


# ------------------------------------------------------------------
# Edge cases – boundary conditions and typical small values
# ------------------------------------------------------------------
def test_fibonacci_edge_cases():
    """Test boundary conditions and typical small values for fibonacci."""
    # Boundary conditions
    assert fibonacci(0) == 0, "fibonacci(0) should be 0"
    assert fibonacci(1) == 1, "fibonacci(1) should be 1"

    # Small values
    assert fibonacci(2) == 1, "fibonacci(2) should be 1"
    assert fibonacci(3) == 2, "fibonacci(3) should be 2"
    assert fibonacci(4) == 3, "fibonacci(4) should be 3"

    # Larger but still manageable values
    assert fibonacci(10) == 55, "fibonacci(10) should be 55"
    assert fibonacci(20) == 6765, "fibonacci(20) should be 6765"
    assert fibonacci(30) == 832040, "fibonacci(30) should be 832040"


# ------------------------------------------------------------------
# Error cases – negative inputs should raise ValueError
# ------------------------------------------------------------------
def test_fibonacci_error_cases():
    """Test that fibonacci raises ValueError for negative inputs."""
    with pytest.raises(ValueError):
        fibonacci(-1)
    with pytest.raises(ValueError):
        fibonacci(-5)
    with pytest.raises(ValueError):
        fibonacci(-100)