"""
Auto-generated test cases for function: round_currency
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 22:18:18
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

# --------------------------------------------------------------------------- #
# 1. Normal cases – typical values that should round cleanly
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (1.2345, 1.23),          # round down
        (1.2355, 1.24),          # round up
        (0.0, 0.0),              # zero
        (123456.789, 123456.79), # large number
        (-1.2345, -1.23),        # negative number
        (2.5, 2.5),              # exact half
        (2.5001, 2.5),           # just above half
        (2.4999, 2.5),           # just below half
    ],
)
def test_round_currency_normal_cases(input_val, expected):
    """
    Test that round_currency correctly rounds typical floating‑point values
    to two decimal places.
    """
    result = round_currency(input_val)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# 2. Edge cases – values near rounding thresholds and very large numbers
# --------------------------------------------------------------------------- #
def test_round_currency_edge_cases():
    """
    Test boundary conditions such as values just below or above a rounding
    threshold, and very large or very small numbers.
    """
    # Just below the threshold – should round down
    assert round_currency(1.2349999) == pytest.approx(1.23)

    # Just above the threshold – should round up
    assert round_currency(1.2350001) == pytest.approx(1.24)

    # Large positive number with a small fractional part
    assert round_currency(1e10 + 0.005) == pytest.approx(1e10 + 0.01)

    # Large negative number with a small fractional part
    assert round_currency(-1e10 - 0.0049) == pytest.approx(-1e10)

    # Very small positive number
    assert round_currency(0.0004) == pytest.approx(0.0)

    # Very small negative number
    assert round_currency(-0.0004) == pytest.approx(0.0)


# --------------------------------------------------------------------------- #
# 3. Error cases – invalid inputs that should raise ValueError
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "string",
        [1, 2],
        {"a": 1},
        (1, 2),
        set([1, 2]),
    ],
)
def test_round_currency_error_cases(invalid_input):
    """
    Test that round_currency raises ValueError when given an invalid input type.
    """
    with pytest.raises(ValueError):
        round_currency(invalid_input)