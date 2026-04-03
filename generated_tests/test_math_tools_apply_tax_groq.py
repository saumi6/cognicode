"""
Auto-generated test cases for function: apply_tax
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:44:13
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

# The function under test is assumed to be imported in the test module, e.g.:
# from my_module import apply_tax
# For the purpose of these examples we just refer to it directly.


@pytest.mark.parametrize(
    "amount, expected",
    [
        (100.0, 120.0),          # typical positive amount
        (0.0, 0.0),              # zero amount  tax should not change it
        (50.5, 60.6),            # amount with cents
        (1_000_000.0, 1_200_000.0),  # very large amount
        (19.99, 23.988),         # typical price with twodecimal precision
    ],
)
def test_apply_tax_normal_cases(amount, expected):
    """
    Test normal, expected usage of ``apply_tax`` with a variety of
    realistic monetary values.
    """
    result = apply_tax(amount)
    # Use ``pytest.approx`` to avoid floatingpoint precision issues.
    assert result == pytest.approx(expected, rel=1e-9)


def test_apply_tax_edge_cases():
    """
    Test boundary and edgecase inputs such as negative amounts and
    extremely small positive amounts.
    """
    # Edge case: negative amount  many implementations raise an error,
    # but if they allow it, the tax should still be applied proportionally.
    # Here we assert the function raises a ``ValueError`` for negatives.
    with pytest.raises(ValueError):
        apply_tax(-10.0)

    # Edge case: a very small positive amount (close to zero)
    tiny_amount = 1e-9
    expected = tiny_amount * 1.20  # assuming a 20% tax rate
    result = apply_tax(tiny_amount)
    assert result == pytest.approx(expected, rel=1e-9)

    # Edge case: amount exactly at a typical rounding threshold
    amount = 0.05  # 5cents
    expected = 0.05 * 1.20
    result = apply_tax(amount)
    assert result == pytest.approx(expected, rel=1e-9)


def test_apply_tax_error_cases():
    """
    Verify that ``apply_tax`` raises appropriate exceptions for
    invalid input types.
    """
    # Nonnumeric string
    with pytest.raises(TypeError):
        apply_tax("100")

    # ``None`` as input
    with pytest.raises(TypeError):
        apply_tax(None)

    # List instead of a number
    with pytest.raises(TypeError):
        apply_tax([100])