"""
Auto-generated test cases for function: apply_tax
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:12
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

@pytest.mark.parametrize(
    "amount, expected",
    [
        (0.0, 0.0),                # zero amount  tax should not change it
        (10.0, 12.0),              # simple positive amount
        (99.99, 119.988),          # typical price with two decimals
        (1234.56, 1481.472),       # larger amount
        (0.01, 0.012),             # very small amount
    ],
)
def test_apply_tax_normal_cases(amount, expected):
    """Verify that ``apply_tax`` returns the correct total for typical inputs.

    The function is expected to add a 20% tax (i.e. multiply by 1.2).
    """
    result = apply_tax(amount)
    # ``apply_tax`` should return a float; ``pytest.approx`` handles rounding issues.
    assert isinstance(result, float)
    assert result == pytest.approx(expected, rel=1e-9)


def test_apply_tax_edge_cases():
    """Test boundary and extreme values for ``apply_tax``."""
    # Very large amount  check that the function still returns a sensible value
    huge_amount = 1e12
    huge_expected = huge_amount * 1.2
    assert apply_tax(huge_amount) == pytest.approx(huge_expected, rel=1e-9)

    # Very small positive amount  ensure no underflow or rounding problems
    tiny_amount = 1e-9
    tiny_expected = tiny_amount * 1.2
    assert apply_tax(tiny_amount) == pytest.approx(tiny_expected, rel=1e-9)

    # Amount that is already a whole number after tax
    whole_amount = 5.0
    whole_expected = whole_amount * 1.2
    assert apply_tax(whole_amount) == pytest.approx(whole_expected, rel=1e-9)


def test_apply_tax_error_cases():
    """Check that ``apply_tax`` raises appropriate exceptions for invalid input."""
    # Negative amounts are not allowed
    with pytest.raises(ValueError):
        apply_tax(-10.0)

    # Nonnumeric types should raise a TypeError
    with pytest.raises(TypeError):
        apply_tax("100")

    # ``None`` is also invalid
    with pytest.raises(TypeError):
        apply_tax(None)