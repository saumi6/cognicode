"""
Auto-generated test cases for function: update_price
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:27:04
Source file: product.py
Function signature: def update_price(self, new_price: float)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.product import Product

import pytest

# Import the class and exception that are under test.
# The module name is assumed to be `product`. Adjust if your module has a different name.
from product import Product, ValidationError


@pytest.mark.parametrize(
    "new_price, expected",
    [
        (20.0, 20.0),
        (15.75, 15.75),
        (0.0, 0.0),
        (123456.789, 123456.789),
    ],
)
def test_update_price_normal_cases(monkeypatch, new_price, expected):
    """
    Test that `update_price` correctly updates the price for a variety of normal inputs.
    The rounding function is patched to the identity function to isolate the test from
    rounding logic.
    """
    # Patch the rounding helper to avoid sideeffects.
    monkeypatch.setattr("product.round_currency", lambda x: x)
    # Patch the SKU generator to a deterministic value.
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU123")

    # Instantiate a product with a valid initial price.
    prod = Product(name="Widget", price=10.0, category="Tools")

    # Update the price.
    prod.update_price(new_price)

    # Assert that the price was updated correctly.
    assert prod.price == pytest.approx(expected)


@pytest.mark.parametrize(
    "new_price, expected",
    [
        # Boundary: zero price
        (0.0, 0.0),
        # Very small positive number
        (1e-9, 0.0),
        # Very large number
        (1e9, 1e9),
        # Price that requires rounding to two decimals
        (12.3456, 12.35),
        (12.3444, 12.34),
    ],
)
def test_update_price_edge_cases(monkeypatch, new_price, expected):
    """
    Test boundary and edge cases for `update_price`, including very small,
    very large, and values that should be rounded to two decimal places.
    """
    # Patch the rounding helper to round to two decimal places.
    monkeypatch.setattr("product.round_currency", lambda x: round(x, 2))
    # Patch the SKU generator to a deterministic value.
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU123")

    prod = Product(name="Gadget", price=5.0, category="Electronics")

    prod.update_price(new_price)

    assert prod.price == pytest.approx(expected)


def test_update_price_error_cases(monkeypatch):
    """
    Test that `update_price` raises the appropriate exceptions for invalid inputs.
    """
    # Patch the rounding helper to the identity function.
    monkeypatch.setattr("product.round_currency", lambda x: x)
    # Patch the SKU generator to a deterministic value.
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU123")

    prod = Product(name="Thing", price=10.0, category="Misc")

    # Negative price should raise ValidationError.
    with pytest.raises(ValidationError):
        prod.update_price(-5.0)

    # Nonnumeric input should raise a TypeError when the comparison is attempted.
    with pytest.raises(TypeError):
        prod.update_price("invalid")

    # None input should also raise a TypeError.
    with pytest.raises(TypeError):
        prod.update_price(None)