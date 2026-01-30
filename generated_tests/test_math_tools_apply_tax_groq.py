"""
Auto-generated test cases for function: apply_tax
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 22:18:11
Source file: math_tools.py
Function signature: def apply_tax(amount: float) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.math_tools import apply_tax

import pytest

# --------------------------------------------------------------------------- #
# 1️⃣  Normal cases – typical positive amounts
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (100.0, 110.0),          # 10 % tax on a round number
        (0.0, 0.0),              # zero amount stays zero
        (50.5, 55.55),           # tax on a decimal amount
        (123.45, 135.795),       # another decimal example
    ],
)
def test_apply_tax_normal_cases(input_val, expected):
    """
    Test that `apply_tax` correctly adds a 10 % tax to typical positive amounts.
    """
    result = apply_tax(input_val)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# 2️⃣  Edge cases – boundary values and very small/large numbers
# --------------------------------------------------------------------------- #
def test_apply_tax_edge_cases():
    """
    Test boundary conditions such as zero, extremely small, and extremely large amounts.
    """
    # Zero amount
    assert apply_tax(0.0) == pytest.approx(0.0)

    # Very small amount (close to floating‑point precision limits)
    small_amount = 1e-12
    assert apply_tax(small_amount) == pytest.approx(small_amount * 1.1)

    # Very large amount
    large_amount = 1e12
    assert apply_tax(large_amount) == pytest.approx(large_amount * 1.1)


# --------------------------------------------------------------------------- #
# 3️⃣  Error cases – invalid input types and negative values
# --------------------------------------------------------------------------- #
def test_apply_tax_error_cases():
    """
    Verify that `apply_tax` raises appropriate exceptions for invalid inputs.
    """
    # Non‑numeric types should raise TypeError
    with pytest.raises(TypeError):
        apply_tax("not a number")
    with pytest.raises(TypeError):
        apply_tax(None)
    with pytest.raises(TypeError):
        apply_tax([100])

    # Negative amounts are considered invalid for this tax calculation
    with pytest.raises(ValueError):
        apply_tax(-10.0)