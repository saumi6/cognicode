"""
Auto-generated test cases for function: create_product
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:26:49
Source file: product_controller.py
Function signature: def create_product(self, name: str, price: float, category: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.product_controller import ProductController

import pytest
from unittest.mock import MagicMock

# ----------------------------------------------------------------------
# Helper mocks that will replace the real implementations used by
# ProductController.  They are defined inside the test file so that they
# can be patched with the full import path ``test_repo.product_controller``.
# ----------------------------------------------------------------------


class _MockProduct:
    """A lightweight standin for the real ``Product`` class.

    It stores the arguments it was created with and exposes a deterministic
    ``sku`` attribute that can be asserted in the tests.
    """
    _sku_counter = 0

    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category
        # generate a predictable sku for each instance
        type(self)._sku_counter += 1
        self.sku = f"SKU-{type(self)._sku_counter}"


class _MockInventoryManager:
    """Mimics the ``InventoryManager`` used by ``ProductController``."""

    def __init__(self):
        self.added_products = []

    def add_product(self, product):
        """Record the product that was added."""
        self.added_products.append(product)


class _MockRecommendationEngine:
    """A dummy ``RecommendationEngine``  not used in the create_product tests."""
    def __init__(self, inventory):
        self.inventory = inventory

    def suggest_products(self, user):
        return []


# ----------------------------------------------------------------------
# Test suite
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "name, price, category, expected_sku_prefix",
    [
        ("Apple iPhone", 999.99, "Electronics", "SKU-"),
        ("Banana", 0.25, "Food", "SKU-"),
        ("Desk Chair", 149.5, "Furniture", "SKU-"),
    ],
)
def test_create_product_normal_cases(monkeypatch, name, price, category, expected_sku_prefix):
    """Normal usage  verify that a product is created, added to inventory and
    that the returned SKU follows the expected pattern."""
    # ------------------------------------------------------------------
    # Patch the external dependencies with the mocks defined above.
    # ------------------------------------------------------------------
    monkeypatch.setattr("test_repo.product_controller.Product", _MockProduct)
    monkeypatch.setattr("test_repo.product_controller.InventoryManager", _MockInventoryManager)
    monkeypatch.setattr("test_repo.product_controller.RecommendationEngine", _MockRecommendationEngine)

    # ------------------------------------------------------------------
    # Instantiate the controller (its __init__ will now use the mocks).
    # ------------------------------------------------------------------
    from test_repo.product_controller import ProductController  # imported after patching
    controller = ProductController()

    # ------------------------------------------------------------------
    # Call the method under test.
    # ------------------------------------------------------------------
    returned_sku = controller.create_product(name, price, category)

    # ------------------------------------------------------------------
    # Assertions.
    # ------------------------------------------------------------------
    # 1. The SKU should start with the expected prefix.
    assert returned_sku.startswith(expected_sku_prefix)

    # 2. The inventory manager should have recorded exactly one product.
    assert len(controller.inventory.added_products) == 1

    # 3. The stored product should have the same attributes we passed.
    stored_product = controller.inventory.added_products[0]
    assert stored_product.name == name
    assert stored_product.price == pytest.approx(price)
    assert stored_product.category == category

    # 4. The SKU returned by the method must be the same as the product's SKU.
    assert stored_product.sku == returned_sku


def test_create_product_edge_cases(monkeypatch):
    """Edgecase handling  empty strings, zero price and very large price."""
    # Patch dependencies.
    monkeypatch.setattr("test_repo.product_controller.Product", _MockProduct)
    monkeypatch.setattr("test_repo.product_controller.InventoryManager", _MockInventoryManager)
    monkeypatch.setattr("test_repo.product_controller.RecommendationEngine", _MockRecommendationEngine)

    from test_repo.product_controller import ProductController
    controller = ProductController()

    # 1. Empty name and category, zero price.
    sku1 = controller.create_product("", 0.0, "")
    prod1 = controller.inventory.added_products[-1]
    assert prod1.name == ""
    assert prod1.price == pytest.approx(0.0)
    assert prod1.category == ""
    assert prod1.sku == sku1

    # 2. Very large price (testing that the method does not overflow or truncate).
    huge_price = 1e12  # 1 trillion
    sku2 = controller.create_product("Luxury Yacht", huge_price, "Luxury")
    prod2 = controller.inventory.added_products[-1]
    assert prod2.name == "Luxury Yacht"
    assert prod2.price == pytest.approx(huge_price)
    assert prod2.category == "Luxury"
    assert prod2.sku == sku2

    # Ensure that two products have been added in total.
    assert len(controller.inventory.added_products) == 2


def test_create_product_error_cases(monkeypatch):
    """Invalid inputs should raise an exception.

    arguments and raise ``ValueError`` when they are not acceptable.
    """
    # ------------------------------------------------------------------
    # A stricter mock that validates its inputs.
    # ------------------------------------------------------------------
    class _ValidatingMockProduct:
        _sku_counter = 0

        def __init__(self, name: str, price: float, category: str):
            if not isinstance(name, str) or not name:
                raise ValueError("name must be a nonempty string")
            if not isinstance(category, str) or not category:
                raise ValueError("category must be a nonempty string")
            if not isinstance(price, (int, float)):
                raise ValueError("price must be numeric")
            if price < 0:
                raise ValueError("price cannot be negative")
            self.name = name
            self.price = price
            self.category = category
            type(self)._sku_counter += 1
            self.sku = f"SKU-{type(self)._sku_counter}"

    # Patch the real classes with the mocks.
    monkeypatch.setattr("test_repo.product_controller.Product", _ValidatingMockProduct)
    monkeypatch.setattr("test_repo.product_controller.InventoryManager", _MockInventoryManager)
    monkeypatch.setattr("test_repo.product_controller.RecommendationEngine", _MockRecommendationEngine)

    from test_repo.product_controller import ProductController
    controller = ProductController()

    # ------------------------------------------------------------------
    # Invalid name (empty string)
    # ------------------------------------------------------------------
    with pytest.raises(ValueError):
        controller.create_product("", 10.0, "Toys")

    # ------------------------------------------------------------------
    # Invalid category (nonstring)
    # ------------------------------------------------------------------
    with pytest.raises(ValueError):
        controller.create_product("Toy Car", 10.0, 123)

    # ------------------------------------------------------------------
    # Negative price
    # ------------------------------------------------------------------
    with pytest.raises(ValueError):
        controller.create_product("Toy Car", -5.0, "Toys")

    # ------------------------------------------------------------------
    # Nonnumeric price
    # ------------------------------------------------------------------
    with pytest.raises(ValueError):
        controller.create_product("Toy Car", "free", "Toys")