"""
Auto-generated test cases for function: calculate_discount
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:25:59
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
# 1. Normal cases  a variety of typical inputs
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (100.0, 10.0, 90.0),          # 10% off
        (200.0, 25.0, 150.0),         # 25% off
        (50.0, 0.0, 50.0),            # no discount
        (75.5, 5.0, 71.725),          # small discount
        (123.45, 12.5, 108.4875),     # fractional discount
    ],
)
def test_calculate_discount_normal_cases(price, discount_percent, expected):
    """Test normal, everyday discount calculations."""
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# 2. Edge cases  boundary values and extreme inputs
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (0.0, 10.0, 0.0),                 # zero price
        (100.0, 0.0, 100.0),              # zero discount
        (100.0, 100.0, 0.0),              # full discount
        (1e9, 50.0, 5e8),                 # very large price
        (123.456, 0.001, 123.452543544),  # tiny discount
    ],
)
def test_calculate_discount_edge_cases(price, discount_percent, expected):
    """Test boundary and extreme values for calculate_discount."""
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected)


# --------------------------------------------------------------------------- #
# 3. Error cases  invalid inputs should raise appropriate exceptions
# --------------------------------------------------------------------------- #
def test_calculate_discount_error_cases():
    """Test that invalid inputs raise the expected exceptions."""
    # Negative price
    with pytest.raises(ValueError):
        calculate_discount(-10.0, 10.0)

    # Negative discount
    with pytest.raises(ValueError):
        calculate_discount(10.0, -5.0)

    # Discount greater than 100%
    with pytest.raises(ValueError):
        calculate_discount(10.0, 150.0)

    # Nonnumeric price
    with pytest.raises(TypeError):
        calculate_discount("100", 10.0)

    # Nonnumeric discount
    with pytest.raises(TypeError):
        calculate_discount(100.0, "10")