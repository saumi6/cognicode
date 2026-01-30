"""
Auto-generated test cases for function: gcd
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2025-10-03 14:46:58
Source file: math_utils.py
Function signature: def gcd(a: int, b: int) -> int
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add the directory containing the source file to Python path
sys.path.insert(0, r"C:\Users\rickh\OneDrive\Desktop\Cogni\examples")

# Import the function to be tested
from math_utils import gcd

import pytest

# --------------------------------------------------------------------------- #
# 1. Normal cases – typical positive integers
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (48, 18, 6),          # common divisor
        (13, 13, 13),         # identical numbers
        (100, 25, 25),        # one is a multiple of the other
        (7, 3, 1),            # coprime numbers
        (27, 9, 9),           # one divides the other
        (12, 18, 6),          # mixed numbers
        (1, 1, 1),            # smallest positive numbers
        (1234567890, 9876543210, 90),  # large numbers
    ],
)
def test_gcd_normal_cases(a, b, expected):
    """
    Test gcd with a variety of normal, positive integer inputs.
    """
    result = gcd(a, b)
    assert result == expected, f"gcd({a}, {b}) should be {expected}, got {result}"


# --------------------------------------------------------------------------- #
# 2. Edge cases – zeros, negatives, and very large values
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, 0),            # both zero
        (0, 5, 5),            # first zero
        (5, 0, 5),            # second zero
        (-12, 18, 6),         # negative first
        (18, -12, 6),         # negative second
        (-12, -18, 6),        # both negative
        (10**20 + 7, 10**20 + 13, 1),  # very large coprime numbers
    ],
)
def test_gcd_edge_cases(a, b, expected):
    """
    Test gcd with edge conditions such as zeros, negative numbers,
    and extremely large integers.
    """
    result = gcd(a, b)
    assert result == expected, f"gcd({a}, {b}) should be {expected}, got {result}"


# --------------------------------------------------------------------------- #
# 3. Error cases – invalid input types
# --------------------------------------------------------------------------- #
def test_gcd_error_cases():
    """
    Test that gcd raises a TypeError when called with non‑integer arguments.
    """
    invalid_inputs = [
        ("a", 5),
        (5, "b"),
        (None, 5),
        (5, None),
        (5.5, 5),
        (5, 5.5),
        ([1, 2], 3),
        (3, {4: 5}),
    ]

    for a, b in invalid_inputs:
        with pytest.raises(TypeError, msg=f"gcd({a!r}, {b!r}) should raise TypeError"):
            gcd(a, b)