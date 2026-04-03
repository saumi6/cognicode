"""
Auto-generated test cases for function: update_price
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:42:08
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
from product import Product, ValidationError  # the module that contains the class


def _mock_round_currency(x):
    """Simple deterministic rounding used for the tests."""
    return round(x, 2)


def _mock_generate_sku(category, name):
    """Return a predictable SKU for testing."""
    return f"{category[:3].upper()}-{name[:3].upper()}"


@pytest.mark.parametrize(
    "initial_price, new_price, expected_price",
    [
        (10.0, 15.99, 15.99),          # normal increase
        (20.555, 30.1234, 30.12),      # rounding to 2 decimals
        (5.0, 5.0, 5.0),               # same price
        (99.999, 100.001, 100.0),      # rounding up/down edge
    ],
)
def test_update_price_normal_cases(monkeypatch, initial_price, new_price, expected_price):
    """
    Verify that ``update_price`` correctly stores a rounded price for typical inputs.
    """
    # Patch the external helpers used by ``Product.__init__`` and ``update_price``.
    monkeypatch.setattr("product.round_currency", _mock_round_currency)
    monkeypatch.setattr("product.generate_sku", _mock_generate_sku)

    # Create a product instance  the constructor also uses the mocked helpers.
    prod = Product(name="TestProduct", price=initial_price, category="General")

    # Call the method under test.
    prod.update_price(new_price)

    # The stored price must be the rounded value returned by the mock.
    assert prod.price == pytest.approx(expected_price)


def test_update_price_edge_cases(monkeypatch):
    """
    Test boundary conditions such as zero price, extremely large values,
    and verify that unrelated attributes (e.g., ``stock``) stay unchanged.
    """
    monkeypatch.setattr("product.round_currency", _mock_round_currency)
    monkeypatch.setattr("product.generate_sku", _mock_generate_sku)

    # Edge case 1  price set to zero.
    prod_zero = Product(name="ZeroPrice", price=0.0)
    prod_zero.update_price(0.0)
    assert prod_zero.price == pytest.approx(0.0)

    # Edge case 2  very large price.
    huge_price = 1e9 + 0.5555
    prod_huge = Product(name="HugePrice", price=huge_price)
    prod_huge.update_price(huge_price * 1.1)  # increase by 10%
    expected_huge = round(huge_price * 1.1, 2)
    assert prod_huge.price == pytest.approx(expected_huge)

    # Edge case 3  price with many decimal places.
    prod_precise = Product(name="Precise", price=1.234567)
    prod_precise.update_price(2.718281828)
    assert prod_precise.price == pytest.approx(2.72)

    # Ensure that ``stock`` is untouched by price updates.
    prod_precise.add_stock(10)
    assert prod_precise.stock == 10
    prod_precise.update_price(3.33)
    assert prod_precise.stock == 10  # stock unchanged


def test_update_price_error_cases(monkeypatch):
    """
    ``update_price`` must raise ``ValidationError`` when a negative price is supplied.
    """
    monkeypatch.setattr("product.round_currency", _mock_round_currency)
    monkeypatch.setattr("product.generate_sku", _mock_generate_sku)

    prod = Product(name="ErrorCase", price=10.0)

    with pytest.raises(ValidationError):
        prod.update_price(-0.01)

    # Also verify that the original price remains unchanged after the failed update.
    assert prod.price == pytest.approx(10.0)