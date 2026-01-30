"""
Auto-generated test cases for function: calculate_discount
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:15
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

@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (100.0, 10.0, 90.0),          # typical 10% discount
        (59.99, 25.0, 44.9925),       # noninteger price & discount
        (200.0, 0.0, 200.0),          # zero percent discount  no change
        (150.0, 50.0, 75.0),          # half price
        (1234.56, 5.5, 1166.588),     # fractional percent
    ],
)
def test_calculate_discount_normal_cases(price, discount_percent, expected):
    """
    Verify that ``calculate_discount`` returns the correct discounted price
    for a variety of typical inputs.
    """
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected)


def test_calculate_discount_edge_cases():
    """
    Test boundary conditions such as a full (100%) discount,
    a zero price, and the smallest positive discount.
    """
    # 100% discount should reduce any price to zero
    assert calculate_discount(99.99, 100.0) == pytest.approx(0.0)

    # Zero price should stay zero regardless of discount
    assert calculate_discount(0.0, 20.0) == pytest.approx(0.0)

    # Very small discount (e.g., 0.01%) on a normal price
    small_discount = calculate_discount(1000.0, 0.01)
    expected = 1000.0 * (1 - 0.0001)  # 0.01% = 0.0001 as a fraction
    assert small_discount == pytest.approx(expected)


def test_calculate_discount_error_cases():
    """
    Ensure that invalid inputs raise ``ValueError``.
    """
    # Negative price
    with pytest.raises(ValueError):
        calculate_discount(-10.0, 10.0)

    # Discount percent below 0
    with pytest.raises(ValueError):
        calculate_discount(50.0, -5.0)

    # Discount percent above 100
    with pytest.raises(ValueError):
        calculate_discount(50.0, 150.0)