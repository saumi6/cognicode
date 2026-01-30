"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:56
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
from unittest.mock import MagicMock

# The class under test lives in the module `product`.
# Import the class and the custom exception so the tests can reference them.
from product import Product, ValidationError


@pytest.fixture(autouse=True)
def _mock_helpers(monkeypatch):
    """
    Replace the helper functions used by ``Product.__init__`` with deterministic
    standins so the tests are not dependent on their real implementations.
    """
    # ``round_currency`` should simply return the value it receives.
    monkeypatch.setattr(
        "product.round_currency", lambda x: x, raising=True
    )
    # ``generate_sku`` should return a predictable string based on its inputs.
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"SKU-{category[:3].upper()}-{name[:3].upper()}",
        raising=True,
    )
    # No return  the fixture only sets up the patches.
    yield


@pytest.mark.parametrize(
    "name, price, category, expected_sku",
    [
        ("Apple", 1.99, "Fruit", "SKU-FRU-APP"),
        ("Banana", 0.5, "Fruit", "SKU-FRU-BAN"),
        ("Notebook", 12.49, "Stationery", "SKU-STA-NOT"),
        ("Pen", 2.0, None, "SKU-GEN-PEN"),  # ``category`` defaults to "General"
        ("Water Bottle", 8.75, "Sports", "SKU-SPO-WAT"),
    ],
)
def test___init___normal_cases(name, price, category, expected_sku):
    """
    Verify that a ``Product`` instance is correctly initialised for typical inputs.
    """
    # ``category`` may be ``None`` to trigger the default argument.
    init_category = category if category is not None else "General"

    # Create an *uninitialised* instance and call ``__init__`` manually.
    product = Product.__new__(Product)
    product.__init__(name, price, init_category)

    # Assertions about the public attributes.
    assert product.name == name
    assert product.price == pytest.approx(price)  # round_currency is a noop
    assert product.category == init_category
    assert product.sku == expected_sku
    assert product.stock == 0  # default stock


def test___init___edge_cases():
    """
    Test boundary conditions such as zero price, empty strings and very large values.
    """
    # Edge case 1  price exactly zero.
    p_zero = Product.__new__(Product)
    p_zero.__init__("Freebie", 0.0, "Promotions")
    assert p_zero.price == pytest.approx(0.0)
    assert p_zero.sku == "SKU-PRO-FRE"

    # Edge case 2  empty name and empty category (category falls back to default).
    p_empty = Product.__new__(Product)
    p_empty.__init__("", 10.0, "")
    assert p_empty.name == ""
    # Empty category is accepted asis; the default is only used when the argument is omitted.
    assert p_empty.category == ""
    assert p_empty.sku == "SKU---"  # threechar slices of empty strings yield empty parts

    # Edge case 3  very large price with many decimal places.
    large_price = 9_999_999.9999
    p_large = Product.__new__(Product)
    p_large.__init__("Luxury Car", large_price, "Vehicles")
    assert p_large.price == pytest.approx(large_price)
    assert p_large.sku == "SKU-VEH-LUX"


def test___init___error_cases():
    """
    Ensure that invalid inputs raise the appropriate exceptions.
    """
    # Negative price should raise the custom ``ValidationError``.
    product = Product.__new__(Product)
    with pytest.raises(ValidationError):
        product.__init__("Bad Product", -5.0, "Misc")

    # Nonnumeric price (e.g., a string) will raise a ``TypeError`` when compared
    # to zero inside the method.
    product = Product.__new__(Product)
    with pytest.raises(TypeError):
        product.__init__("Weird", "not-a-number", "Misc")