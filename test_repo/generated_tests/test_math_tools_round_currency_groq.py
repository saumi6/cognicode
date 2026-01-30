"""
Auto-generated test cases for function: round_currency
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:11:29
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
# Normal cases  simple, everyday values
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (0.0, 0.0),
        (1.0, 1.0),
        (1.234, 1.23),
        (1.235, 1.24),
        (0.999, 1.0),
        (0.004, 0.0),
        (123.456, 123.46),
        (-1.234, -1.23),
        (-1.235, -1.24),
    ],
)
def test_round_currency_normal_cases(input_val, expected):
    """Test normal rounding behaviour for typical values."""
    result = round_currency(input_val)
    assert result == pytest.approx(expected, rel=1e-9)


# --------------------------------------------------------------------------- #
# Edge cases  boundary conditions, large numbers, many decimals
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "input_val, expected",
    [
        # Large number
        (123456789.987654321, 123456789.99),
        # Numbers exactly on a rounding boundary
        (1.005, 1.0),          # Python's round uses banker's rounding
        (1.0049999, 1.0),
        (1.0050001, 1.01),
        (1.9999, 2.0),
        (2.0001, 2.0),
        (2.005, 2.0),
        # Negative large number
        (-123456789.987654321, -123456789.99),
        # Very small number
        (0.0000001234, 0.0),
    ],
)
def test_round_currency_edge_cases(input_val, expected):
    """Test edge cases such as large numbers, boundary values, and many decimals."""
    result = round_currency(input_val)
    assert result == pytest.approx(expected, rel=1e-9)


# --------------------------------------------------------------------------- #
# Error cases  invalid inputs that should raise an exception
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "not a number",
        [1, 2, 3],
        {"a": 1},
        object(),
    ],
)
def test_round_currency_error_cases(invalid_input):
    """Test that round_currency raises a TypeError for nonnumeric inputs."""
    with pytest.raises(TypeError):
        round_currency(invalid_input)