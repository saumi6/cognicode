"""
Auto-generated test cases for function: calculate_discount
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 22:31:21
Source file: math_tools.py
Function signature: def calculate_discount(price: float, discount_percent: float) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.math_tools import calculate_discount

import pytest

# --------------------------------------------------------------------------- #
# Normal cases  typical usage of the function
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        # Basic discounts
        (100.0, 10.0, 90.0),
        (200.0, 25.0, 150.0),
        (50.0, 0.0, 50.0),
        # Edge of the discount range
        (0.0, 50.0, 0.0),
        (100.0, 100.0, 0.0),
        # Noninteger values
        (123.45, 12.5, 108.4875),
    ],
)
def test_calculate_discount_normal_cases(price, discount_percent, expected):
    """Test normal discount calculations."""
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# Edge cases  boundary conditions and extreme values
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        # Zero price
        (0.0, 0.0, 0.0),
        (0.0, 100.0, 0.0),
        # Zero discount
        (100.0, 0.0, 100.0),
        # Maximum discount
        (100.0, 100.0, 0.0),
        # Very small price and discount
        (1e-9, 0.000001, 1e-9 * (1 - 0.000001)),
        # Discount just below 100%
        (100.0, 99.9999, 100.0 * (1 - 99.9999 / 100)),
    ],
)
def test_calculate_discount_edge_cases(price, discount_percent, expected):
    """Test boundary and edge cases for discount calculation."""
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# Error cases  invalid inputs should raise appropriate exceptions
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "price, discount_percent, exception",
    [
        # Negative values
        (-10.0, 10.0, ValueError),
        (10.0, -5.0, ValueError),
        # Discount greater than 100%
        (10.0, 150.0, ValueError),
        # Nonnumeric inputs
        ("100", 10.0, TypeError),
        (100.0, "10", TypeError),
        (None, 10.0, TypeError),
        (10.0, None, TypeError),
    ],
)
def test_calculate_discount_error_cases(price, discount_percent, exception):
    """Test that invalid inputs raise the expected exceptions."""
    with pytest.raises(exception):
        calculate_discount(price, discount_percent)