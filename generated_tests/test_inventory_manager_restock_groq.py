"""
Auto-generated test cases for function: restock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:11:47
Source file: inventory_manager.py
Function signature: def restock(self, sku: str, qty: int)
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

import builtins
from unittest.mock import MagicMock, Mock

import pytest

# The class under test is expected to live in a module called ``inventory_manager``.
# Adjust the import path if the actual file name differs.
from inventory_manager import InventoryManager


@pytest.fixture(autouse=True)
def mock_logger(monkeypatch):
    """
    Replace the modulelevel ``logger`` with a mock so that calls to
    ``logger.info`` do not produce real log output and can be inspected.
    """
    fake_logger = Mock()
    monkeypatch.setattr("inventory_manager.logger", fake_logger)
    return fake_logger


def _make_product(sku: str, stock: int = 0) -> MagicMock:
    """
    Helper that creates a ``Product``like mock with the attributes used by
    ``InventoryManager`` (``sku``, ``stock`` and ``add_stock``).
    """
    product = MagicMock()
    product.sku = sku
    product.stock = stock
    # ``add_stock`` should modify ``stock`` like a real implementation would.
    def _add_stock(qty):
        product.stock += qty
    product.add_stock.side_effect = _add_stock
    return product


@pytest.mark.parametrize(
    "initial_stock, restock_qty, expected_stock",
    [
        (10, 5, 15),      # normal increase
        (0, 20, 20),      # restocking from zero
        (100, 0, 100),    # restocking with zero (no change)
        (5, -2, 3),       # negative qty  method does not guard against it
    ],
)
def test_restock_normal_cases(mock_logger, initial_stock, restock_qty, expected_stock):
    """
    Verify that ``restock`` correctly forwards the quantity to the product's
    ``add_stock`` method and that the internal stock value reflects the change.
    """
    manager = InventoryManager()
    sku = "TESTSKU"
    product = _make_product(sku, stock=initial_stock)
    manager.products[sku] = product

    # Act
    manager.restock(sku, restock_qty)

    # Assert that ``add_stock`` was called exactly once with the supplied qty
    product.add_stock.assert_called_once_with(restock_qty)

    # The mock's sideeffect updates ``stock``  check the final value
    assert product.stock == expected_stock

    # Ensure a log entry was emitted
    mock_logger.info.assert_called_once_with(f"Restocked {sku} by {restock_qty}")


def test_restock_edge_cases(mock_logger):
    """
    Edgecase tests:
    * Restocking a SKU that does **not** exist  should be a noop.
    * Restocking with a very large integer  should still call ``add_stock``.
    """
    manager = InventoryManager()

    # 1 SKU not present
    missing_sku = "MISSING"
    manager.restock(missing_sku, 10)

    # No product, therefore ``add_stock`` must never be called and no log entry.
    mock_logger.info.assert_not_called()

    # 2 Very large quantity
    large_qty = 10**12
    sku = "BIGSKU"
    product = _make_product(sku, stock=0)
    manager.products[sku] = product

    manager.restock(sku, large_qty)

    product.add_stock.assert_called_once_with(large_qty)
    assert product.stock == large_qty
    mock_logger.info.assert_called_once_with(f"Restocked {sku} by {large_qty}")


def test_restock_error_cases(mock_logger):
    """
    ``restock`` itself does not raise for bad input, but the underlying
    ``Product.add_stock`` may. These tests ensure that such exceptions are
    propagated correctly.
    """
    manager = InventoryManager()
    sku = "ERRSKU"
    product = MagicMock()
    product.sku = sku

    # Simulate ``add_stock`` raising a ``ValueError`` when a nonint qty is used.
    def raise_on_bad_qty(qty):
        if not isinstance(qty, int):
            raise ValueError("Quantity must be an integer")
        # otherwise behave normally
        product.stock += qty

    product.add_stock.side_effect = raise_on_bad_qty
    manager.products[sku] = product

    # ---- invalid qty type -------------------------------------------------
    with pytest.raises(ValueError):
        manager.restock(sku, "not-an-int")

    # ``add_stock`` should have been called with the bad value before raising.
    product.add_stock.assert_called_once_with("not-an-int")
    # No log entry should be made because the exception aborts the method.
    mock_logger.info.assert_not_called()

    # Reset mock for the next scenario
    product.add_stock.reset_mock()
    mock_logger.info.reset_mock()

    # ---- negative qty that the product explicitly rejects -----------------
    def reject_negative(qty):
        if qty < 0:
            raise ValueError("Negative restock not allowed")
        product.stock += qty

    product.add_stock.side_effect = reject_negative

    with pytest.raises(ValueError):
        manager.restock(sku, -5)

    product.add_stock.assert_called_once_with(-5)
    mock_logger.info.assert_not_called()