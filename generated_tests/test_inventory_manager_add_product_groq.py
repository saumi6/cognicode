"""
Auto-generated test cases for function: add_product
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:11:33
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

import pytest
from unittest.mock import Mock, MagicMock, call

# The class under test lives in ``test_repo.inventory_manager`` (the file name is
# ``inventory_manager.py``).  Import it using the full import path so that
# ``monkeypatch.setattr`` can later target the logger correctly.
from test_repo.inventory_manager import InventoryManager, InventoryError  # type: ignore


@pytest.fixture(autouse=True)
def mock_logger(monkeypatch):
    """
    Replace the modulelevel ``logger`` with a ``MagicMock`` for the duration of
    each test so that we can assert that ``logger.info`` is called with the
    expected message.
    """
    fake_logger = MagicMock()
    monkeypatch.setattr("test_repo.inventory_manager.logger", fake_logger)
    return fake_logger


@pytest.mark.parametrize(
    "sku, name, stock",
    [
        ("SKU001", "Widget A", 10),
        ("SKU002", "Gadget B", 0),
        ("SKU-XYZ-123", "Thingamajig", 9999),
    ],
)
def test_add_product_normal_cases(sku, name, stock, mock_logger):
    """
    Normal usage: adding a brandnew product should store it in the manager and
    emit a log entry.
    """
    manager = InventoryManager()

    # Build a lightweight ``Product`` mock that mimics the real interface.
    product = Mock()
    product.sku = sku
    product.name = name
    product.stock = stock
    # ``add_stock`` is used by ``restock`` only, but we provide it for completeness.
    product.add_stock = Mock()

    # Act
    manager.add_product(product)

    # Assert the product is now in the internal dictionary.
    assert sku in manager.products
    assert manager.products[sku] is product

    # Verify that a log message was emitted with the correct product name.
    mock_logger.info.assert_called_once_with(f"Added product {name}")


def test_add_product_edge_cases(mock_logger):
    """
    Edge cases such as an empty SKU or a very long SKU should still be accepted
    because the method only checks for existence, not format.
    """
    manager = InventoryManager()

    # Edge case 1: empty string SKU
    empty_sku_product = Mock()
    empty_sku_product.sku = ""
    empty_sku_product.name = "EmptySKU"
    empty_sku_product.stock = 5
    empty_sku_product.add_stock = Mock()

    manager.add_product(empty_sku_product)
    assert "" in manager.products
    assert manager.products[""] is empty_sku_product
    mock_logger.info.assert_called_with("Added product EmptySKU")
    mock_logger.info.reset_mock()

    # Edge case 2: extremely long SKU
    long_sku = "X" * 500  # 500 characters long
    long_sku_product = Mock()
    long_sku_product.sku = long_sku
    long_sku_product.name = "LongSKUProduct"
    long_sku_product.stock = 1
    long_sku_product.add_stock = Mock()

    manager.add_product(long_sku_product)
    assert long_sku in manager.products
    assert manager.products[long_sku] is long_sku_product
    mock_logger.info.assert_called_once_with("Added product LongSKUProduct")


def test_add_product_error_cases(mock_logger):
    """
    Adding a product whose SKU already exists must raise ``InventoryError``.
    """
    manager = InventoryManager()

    # First product  should be added without issue.
    first_product = Mock()
    first_product.sku = "DUPLICATE"
    first_product.name = "First"
    first_product.stock = 3
    first_product.add_stock = Mock()
    manager.add_product(first_product)

    # Second product with the same SKU  should raise.
    second_product = Mock()
    second_product.sku = "DUPLICATE"
    second_product.name = "Second"
    second_product.stock = 7
    second_product.add_stock = Mock()

    with pytest.raises(InventoryError) as exc_info:
        manager.add_product(second_product)

    # The exception message should contain the SKU.
    assert "DUPLICATE" in str(exc_info.value)

    # Ensure that the logger was *not* called a second time for the failing add.
    # It should have been called exactly once from the successful addition.
    mock_logger.info.assert_called_once_with("Added product First")