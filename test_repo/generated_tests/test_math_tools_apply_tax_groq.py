"""
Auto-generated test cases for function: apply_tax
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:25:55
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

# NOTE: The tests assume that the function `apply_tax` is available in the
# current namespace (e.g. it has been imported by the test runner or is
# defined in the same file).  If the function lives in a module named
# `tax_module`, you can replace the calls with
# `from tax_module import apply_tax` at the top of this file.

@pytest.mark.parametrize(
    "amount, expected",
    [
        (0.0, 0.0),          # zero amount
        (100.0, 110.0),      # typical case  10% tax
        (50.5, 55.55),       # noninteger amount
        (123.45, 135.795),   # another decimal amount
    ],
)
def test_apply_tax_normal_cases(amount: float, expected: float):
    """
    Test that `apply_tax` returns the expected total for a variety of
    normal input amounts.  The expected values are calculated assuming a
    10% tax rate (i.e. `amount * 1.10`).
    """
    result = apply_tax(amount)
    assert result == pytest.approx(expected, rel=1e-9)


def test_apply_tax_edge_cases():
    """
    Test boundary conditions and edge cases:
    * Very small amounts (close to zero)
    * Very large amounts
    * The result should always be greater than or equal to the input amount.
    """
    # Very small amount
    small_amount = 1e-10
    small_result = apply_tax(small_amount)
    assert small_result >= small_amount
    assert small_result == pytest.approx(small_amount * 1.10, rel=1e-9)

    # Very large amount
    large_amount = 1e12
    large_result = apply_tax(large_amount)
    assert large_result >= large_amount
    assert large_result == pytest.approx(large_amount * 1.10, rel=1e-9)

    # Zero amount (already covered in normal cases but repeated here for completeness)
    zero_result = apply_tax(0.0)
    assert zero_result == 0.0


def test_apply_tax_error_cases():
    """
    Test that `apply_tax` raises appropriate exceptions for invalid inputs:
    * Negative amounts should raise ValueError
    * Nonnumeric inputs (None, string, list) should raise TypeError
    """
    # Negative amount
    with pytest.raises(ValueError):
        apply_tax(-10.0)

    # None input
    with pytest.raises(TypeError):
        apply_tax(None)

    # String input
    with pytest.raises(TypeError):
        apply_tax("100")

    # List input
    with pytest.raises(TypeError):
        apply_tax([100])