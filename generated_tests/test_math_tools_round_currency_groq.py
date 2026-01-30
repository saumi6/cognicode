"""
Auto-generated test cases for function: round_currency
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:19
Source file: math_tools.py
Function signature: def round_currency(amount: float) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.math_tools import round_currency

import pytest

# Import the function under test.
# Replace `round_currency_module` with the actual module name where `round_currency` is defined.
from round_currency_module import round_currency


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (0.0, 0.0),
        (1.234, 1.23),
        (1.235, 1.24),
        (123.4567, 123.46),
        (-2.555, -2.56),
        (-2.554, -2.55),
        (10.0, 10.0),
        (99.999, 100.0),
    ],
)
def test_round_currency_normal_cases(input_val, expected):
    """
    Test normal rounding behaviour for a variety of positive,
    negative and zero values.
    """
    result = round_currency(input_val)
    # Use pytest.approx to avoid floatingpoint representation issues.
    assert result == pytest.approx(expected, rel=1e-12)


def test_round_currency_edge_cases():
    """
    Test boundary and edge conditions such as very large numbers,
    very small numbers, and the classic halfawayfromzero rounding cases.
    """
    # Very large number
    large = 9_999_999_999.9999
    assert round_currency(large) == pytest.approx(10_000_000_000.0, rel=1e-12)

    # Very small positive number (close to zero)
    tiny_pos = 0.000_004_9
    assert round_currency(tiny_pos) == pytest.approx(0.0, rel=1e-12)

    # Very small negative number (close to zero)
    tiny_neg = -0.000_004_9
    assert round_currency(tiny_neg) == pytest.approx(-0.0, rel=1e-12)

    # Halfway cases (banker's rounding is not required by the spec,
    # we just verify the typical roundhalfup behaviour)
    assert round_currency(2.345) == pytest.approx(2.35, rel=1e-12)
    assert round_currency(2.344) == pytest.approx(2.34, rel=1e-12)
    assert round_currency(-2.345) == pytest.approx(-2.35, rel=1e-12)
    assert round_currency(-2.344) == pytest.approx(-2.34, rel=1e-12)


@pytest.mark.parametrize(
    "bad_input, exc_type",
    [
        (None, TypeError),
        ("123.45", TypeError),
        (["1.23"], TypeError),
        ({'amount': 1.23}, TypeError),
        (complex(1, 2), TypeError),
    ],
)
def test_round_currency_error_cases(bad_input, exc_type):
    """
    Ensure that nonnumeric inputs raise the appropriate exception.
    """
    with pytest.raises(exc_type):
        round_currency(bad_input)