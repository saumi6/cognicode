"""
Auto-generated test cases for function: apply_tax
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:07:52
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

# The function under test is assumed to be importable directly in the test module,
# e.g. `from my_module import apply_tax`.  The import itself is handled elsewhere,
# so we only reference the name here.


@pytest.mark.parametrize(
    "amount, expected",
    [
        (100.0, 120.0),          # typical positive amount (20% tax)
        (0.0, 0.0),              # zero amount should stay zero
        (50, 60.0),              # integer input, tax applied
        (1_000_000.0, 1_200_000.0),  # large amount
        (0.01, 0.012),           # small amount, still taxed
    ],
)
def test_apply_tax_normal_cases(amount, expected):
    """
    Test normal, expected behaviour of ``apply_tax`` with a variety of
    typical inputs.  The function is assumed to apply a 20% tax, so the
    expected result is ``amount * 1.20``.
    """
    result = apply_tax(amount)
    # Use ``pytest.approx`` to avoid floatingpoint precision issues.
    assert result == pytest.approx(expected, rel=1e-9)


def test_apply_tax_edge_cases():
    """
    Test boundary and edgecase values such as very small, very large,
    and zero amounts.  The tax rate is still assumed to be 20%.
    """
    # Zero amount  should remain zero.
    assert apply_tax(0.0) == pytest.approx(0.0)

    # Very small positive amount.
    tiny = 1e-12
    assert apply_tax(tiny) == pytest.approx(tiny * 1.20, rel=1e-9)

    # Very large amount (close to float max but still safe).
    huge = 1e+20
    assert apply_tax(huge) == pytest.approx(huge * 1.20, rel=1e-9)


def test_apply_tax_error_cases():
    """
    Verify that ``apply_tax`` raises appropriate exceptions for invalid
    inputs such as negative numbers or nonnumeric types.
    """
    # Negative amounts are not allowed.
    with pytest.raises(ValueError):
        apply_tax(-10.0)

    # Passing a string should raise a TypeError (or ValueError depending on impl).
    with pytest.raises(TypeError):
        apply_tax("100")

    # ``None`` is also invalid.
    with pytest.raises(TypeError):
        apply_tax(None)
These three test functions cover:

1. **Normal cases**  a range of typical positive amounts using `@pytest.mark.parametrize`.
2. **Edge cases**  boundary values like zero, extremely small, and extremely large numbers.
3. **Error cases**  invalid inputs that should trigger exceptions (`ValueError` for negatives, `TypeError` for nonnumeric data).

Floatingpoint results are compared with `pytest.approx` to handle precision safely. No external modules are imported beyond `pytest`, satisfying the given constraints.