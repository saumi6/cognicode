"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:26:56
Source file: product.py
Function signature: def __init__(self, name: str, price: float, category: str = 'General')
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

# Import the class and the exception that are defined in the module under test.
# The module name is assumed to be `product`.  Adjust the import path if the
# actual module name differs.
from product import Product, ValidationError


# --------------------------------------------------------------------------- #
# 1. Normal cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, price, category, expected_price, expected_sku",
    [
        ("Apple", 1.2345, "Fruit", 1.23, "FRT-APP"),
        ("Banana", 0.99, "Fruit", 0.99, "FRT-BAN"),
        ("Laptop", 999.999, "Electronics", 1000.0, "ELE-LAP"),
        ("", 10.0, "Misc", 10.0, "MIS-"),
        ("Book", 12.5, "", 12.5, "-BOO"),
    ],
)
def test___init___normal_cases(monkeypatch, name, price, category, expected_price, expected_sku):
    """
    Test that Product.__init__ correctly assigns attributes for a variety of
    normal inputs.  The rounding and SKU generation functions are monkeypatched
    to deterministic behaviours so that the test does not depend on their
    implementation.
    """
    # Monkeypatch the helper functions to avoid external dependencies.
    monkeypatch.setattr("product.round_currency", lambda x: round(x, 2))
    monkeypatch.setattr(
        "product.generate_sku",
        lambda cat, nm: f"{cat[:3].upper() if cat else ''}-{nm[:3].upper() if nm else ''}",
    )

    prod = Product(name=name, price=price, category=category)

    assert prod.name == name
    assert prod.price == pytest.approx(expected_price)
    assert prod.category == category
    assert prod.sku == expected_sku
    assert prod.stock == 0


# --------------------------------------------------------------------------- #
# 2. Edge cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, price, category, expected_price, expected_sku",
    [
        # Zero price
        ("Freebie", 0.0, "Promotions", 0.0, "PRO-FRE"),
        # Very large price
        ("GoldBar", 1e9, "Precious", 1e9, "PRE-GOL"),
        # Price with many decimal places
        ("Precise", 123.456789, "Tools", 123.46, "TOO-PRE"),
        # Empty category (default)
        ("Generic", 5.5, "", 5.5, "-GEN"),
        # Empty name
        ("", 7.7, "Misc", 7.7, "MIS-"),
    ],
)
def test___init___edge_cases(monkeypatch, name, price, category, expected_price, expected_sku):
    """
    Test boundary and edge conditions such as zero price, very large prices,
    highprecision prices, and empty strings for name or category.
    """
    # Use the same deterministic monkeypatches as in the normal case tests.
    monkeypatch.setattr("product.round_currency", lambda x: round(x, 2))
    monkeypatch.setattr(
        "product.generate_sku",
        lambda cat, nm: f"{cat[:3].upper() if cat else ''}-{nm[:3].upper() if nm else ''}",
    )

    prod = Product(name=name, price=price, category=category)

    assert prod.name == name
    assert prod.price == pytest.approx(expected_price)
    assert prod.category == category
    assert prod.sku == expected_sku
    assert prod.stock == 0


# --------------------------------------------------------------------------- #
# 3. Error cases
# --------------------------------------------------------------------------- #
def test___init___error_cases(monkeypatch):
    """
    Test that Product.__init__ raises the appropriate exceptions for invalid
    inputs such as negative prices or nonnumeric values.
    """
    # The helper functions are not needed for error cases, but we patch them
    # anyway to keep the test isolated from external implementations.
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr("product.generate_sku", lambda cat, nm: f"{cat}-{nm}")

    # Negative price should raise ValidationError
    with pytest.raises(ValidationError):
        Product(name="BadPrice", price=-1.0, category="Test")

    # Passing a string as price should raise a TypeError because the
    # comparison `price < 0` is invalid for a string.
    with pytest.raises(TypeError):
        Product(name="StringPrice", price="10", category="Test")

    # Passing None as price should raise a TypeError for the same reason.
    with pytest.raises(TypeError):
        Product(name="NonePrice", price=None, category="Test")