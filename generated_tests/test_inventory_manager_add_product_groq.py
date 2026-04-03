"""
Auto-generated test cases for function: add_product
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:25:24
Source file: inventory_manager.py
Function signature: def add_product(self, product: Product)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.inventory_manager import InventoryManager

@pytest.mark.parametrize(
    "sku, name, stock",
    [
        ("ABC123", "Widget", 10),
        ("xyz-789", "Gadget", 0),
        ("SKU_001", "Thingamajig", 5),
    ],
)
def test_add_product_normal_cases(sku, name, stock):
    """Adding a new product with a unique SKU should store it in the inventory."""
    # Arrange
    manager = InventoryManager()
    product = Mock()
    product.sku = sku
    product.name = name
    product.stock = stock

    # Act
    manager.add_product(product)

    # Assert
    assert sku in manager.products, "SKU should be present after adding"
    stored = manager.products[sku]
    assert stored is product, "The stored product should be the same instance that was added"
    assert stored.name == name
    assert stored.stock == stock


def test_add_product_edge_cases():
    """Edgecase SKUs (empty string, very long, special characters) should still be accepted."""
    manager = InventoryManager()

    # Empty SKU
    empty_sku_product = Mock()
    empty_sku_product.sku = ""
    empty_sku_product.name = "EmptySKU"
    empty_sku_product.stock = 1
    manager.add_product(empty_sku_product)
    assert "" in manager.products
    assert manager.products[""].name == "EmptySKU"

    # Very long SKU
    long_sku = "L" * 255
    long_sku_product = Mock()
    long_sku_product.sku = long_sku
    long_sku_product.name = "LongSKU"
    long_sku_product.stock = 2
    manager.add_product(long_sku_product)
    assert long_sku in manager.products
    assert manager.products[long_sku].stock == 2

    # SKU with special characters
    special_sku = "SKU!@#$%^&*()_+"
    special_product = Mock()
    special_product.sku = special_sku
    special_product.name = "SpecialSKU"
    special_product.stock = 3
    manager.add_product(special_product)
    assert special_sku in manager.products
    assert manager.products[special_sku].name == "SpecialSKU"


def test_add_product_error_cases():
    """Adding a product with a duplicate SKU or an invalid product should raise errors."""
    manager = InventoryManager()

    # First add a product with a given SKU
    original = Mock()
    original.sku = "DUP001"
    original.name = "Original"
    original.stock = 5
    manager.add_product(original)

    # Attempt to add another product with the same SKU  should raise InventoryError
    duplicate = Mock()
    duplicate.sku = "DUP001"
    duplicate.name = "Duplicate"
    duplicate.stock = 1
    with pytest.raises(InventoryError):
        manager.add_product(duplicate)

    # Attempt to add a product that lacks a `sku` attribute  should raise AttributeError
    bad_product = Mock()
    # Deliberately do NOT set `sku`
    bad_product.name = "NoSKU"
    bad_product.stock = 0
    with pytest.raises(AttributeError):
        manager.add_product(bad_product)

    # Attempt to add None as a product  should raise AttributeError
    with pytest.raises(AttributeError):
        manager.add_product(None)