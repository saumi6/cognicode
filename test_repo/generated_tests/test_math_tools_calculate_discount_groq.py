"""
Auto-generated test cases for function: calculate_discount
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:07:56
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

# The function under test is assumed to be importable in the test namespace.
# If it lives in a module called `discount`, you would normally do:
# from discount import calculate_discount
# For the purpose of these examples we call it directly.


@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (100.0, 10.0, 90.0),               # simple 10% off
        (59.99, 15.0, 50.9915),            # typical price with fractional cents
        (200.0, 25.0, 150.0),              # quarter off a round number
        (1234.56, 5.5, 1166.5888),         # mixedprecision case
        (1.0, 50.0, 0.5),                  # 50% off a tiny amount
    ],
)
def test_calculate_discount_normal_cases(price, discount_percent, expected):
    """
    Verify that ``calculate_discount`` returns the correct discounted price
    for a variety of typical inputs.
    """
    result = calculate_discount(price, discount_percent)
    # Use ``pytest.approx`` to avoid floatingpoint precision issues.
    assert result == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (0.0, 0.0, 0.0),          # zero price, zero discount
        (0.0, 50.0, 0.0),         # zero price, any discount stays zero
        (100.0, 0.0, 100.0),      # zero percent discount  original price
        (100.0, 100.0, 0.0),      # full discount  free
        (1e-9, 100.0, 0.0),       # extremely small price, full discount
        (1e9, 0.0, 1e9),          # very large price, no discount
    ],
)
def test_calculate_discount_edge_cases(price, discount_percent, expected):
    """
    Test boundary conditions such as zero values, full discount, and
    extreme magnitudes to ensure the function behaves correctly at the edges.
    """
    result = calculate_discount(price, discount_percent)
    assert result == pytest.approx(expected, rel=1e-9)


def test_calculate_discount_error_cases():
    """
    Ensure that ``calculate_discount`` raises ``ValueError`` for invalid inputs,
    such as negative prices, discount percentages outside the 0100 range,
    or nonnumeric arguments.
    """
    # Negative price
    with pytest.raises(ValueError):
        calculate_discount(-10.0, 10.0)

    # Discount percent less than 0
    with pytest.raises(ValueError):
        calculate_discount(100.0, -5.0)

    # Discount percent greater than 100
    with pytest.raises(ValueError):
        calculate_discount(100.0, 150.0)

    # Nonnumeric price
    with pytest.raises(ValueError):
        calculate_discount("100", 10.0)

    # Nonnumeric discount percent
    with pytest.raises(ValueError):
        calculate_discount(100.0, "10")