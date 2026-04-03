"""
Auto-generated test cases for function: calculate_discount
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:44:18
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

# The function under test is assumed to be imported in the test module, e.g.:
# from my_package.pricing import calculate_discount


@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (100.0, 10.0, 90.0),          # simple 10% discount
        (59.99, 25.0, 44.9925),       # typical retail price with quarteroff
        (2000.0, 5.5, 1890.0),        # larger price with fractional percent
        (9.99, 0.0, 9.99),            # zero percent discount  unchanged price
        (123.45, 100.0, 0.0),         # full discount  free
    ],
)
def test_calculate_discount_normal_cases(price, discount_percent, expected):
    """
    Verify that ``calculate_discount`` returns the correct discounted price
    for a variety of typical inputs.
    """
    result = calculate_discount(price, discount_percent)
    # Use ``pytest.approx`` to handle floatingpoint rounding differences.
    assert result == pytest.approx(expected)


def test_calculate_discount_edge_cases():
    """
    Test boundary conditions such as zero price, very small discounts,
    and extremely large prices to ensure the function behaves correctly.
    """
    # Zero price should always stay zero regardless of discount.
    assert calculate_discount(0.0, 0.0) == pytest.approx(0.0)
    assert calculate_discount(0.0, 50.0) == pytest.approx(0.0)

    # Very small discount (e.g., 0.01%) on a normal price.
    assert calculate_discount(1000.0, 0.01) == pytest.approx(999.9)

    # Very large price with a modest discount.
    large_price = 1e9  # 1billion
    discount = 12.5    # 12.5%
    expected = large_price * (1 - discount / 100)
    assert calculate_discount(large_price, discount) == pytest.approx(expected)

    # Discount exactly at the upper boundary (100%) should yield zero.
    assert calculate_discount(1234.56, 100.0) == pytest.approx(0.0)


@pytest.mark.parametrize(
    "price, discount_percent",
    [
        (-10.0, 10.0),    # negative price
        (100.0, -5.0),    # negative discount percent
        (50.0, 150.0),    # discount greater than 100%
        ("100", 10.0),    # nonnumeric price
        (100.0, "10%"),   # nonnumeric discount
    ],
)
def test_calculate_discount_error_cases(price, discount_percent):
    """
    Ensure that ``calculate_discount`` raises ``ValueError`` for invalid inputs.
    """
    with pytest.raises(ValueError):
        calculate_discount(price, discount_percent)