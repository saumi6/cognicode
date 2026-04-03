"""
Auto-generated test cases for function: suggest_products
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:27:38
Source file: recommendation_engine.py
Function signature: def suggest_products(self, user: User) -> List[Product]
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.recommendation_engine import RecommendationEngine

import pytest
from unittest.mock import MagicMock, Mock

# ----------------------------------------------------------------------
# Helper factories
# ----------------------------------------------------------------------
def make_product(name: str, stock: int):
    """Create a simple mock product with a name and stock attribute."""
    prod = Mock()
    prod.name = name
    prod.stock = stock
    return prod


def make_inventory(product_list):
    """
    Build a mock ``InventoryManager`` whose ``products`` attribute is a dict
    that preserves insertion order (Python 3.7+ guarantees this).
    """
    inventory = Mock()
    # Use the product name as the key  the actual key is irrelevant for the
    # algorithm, only the order matters.
    inventory.products = {p.name: p for p in product_list}
    return inventory


# ----------------------------------------------------------------------
# 1. Normal cases  parametrized
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "product_stocks, expected_names",
    [
        # More than three available  only first three are returned
        ([("A", 5), ("B", 2), ("C", 1), ("D", 10)], ["A", "B", "C"]),
        # Exactly three available  all are returned
        ([("X", 3), ("Y", 4), ("Z", 1)], ["X", "Y", "Z"]),
        # Fewer than three available  return whatever is available
        ([("M", 2), ("N", 0), ("O", 5)], ["M", "O"]),
        # No stock at all  empty list
        ([("P", 0), ("Q", 0)], []),
    ],
)
def test_suggest_products_normal_cases(product_stocks, expected_names):
    """
    Verify that ``suggest_products`` returns up to three products that have
    ``stock > 0`` and respects the order of the inventory dictionary.
    """
    # Build mock products from the parametrized data
    products = [make_product(name, stock) for name, stock in product_stocks]

    # Create a mock inventory containing those products
    mock_inventory = make_inventory(products)

    # The ``user`` argument is not used by the implementation, but we still
    # provide a dummy object to satisfy the signature.
    dummy_user = Mock()

    # Instantiate the engine with the mocked inventory
    from recommendation_engine import RecommendationEngine  # adjust import as needed
    engine = RecommendationEngine(mock_inventory)

    # Call the method under test
    result = engine.suggest_products(dummy_user)

    # Extract the names of the returned products for easy comparison
    result_names = [p.name for p in result]

    assert result_names == expected_names
    # Also assert that we never return more than three items
    assert len(result) <= 3


# ----------------------------------------------------------------------
# 2. Edge cases  boundary conditions
# ----------------------------------------------------------------------
def test_suggest_products_edge_cases():
    """
    Test boundary conditions such as an empty inventory, products with
    zero or negative stock, and exactly three products with stock.
    """
    # ---- Edge case 1: empty inventory ----
    empty_inventory = Mock()
    empty_inventory.products = {}
    dummy_user = Mock()
    from recommendation_engine import RecommendationEngine
    engine = RecommendationEngine(empty_inventory)

    result = engine.suggest_products(dummy_user)
    assert result == []  # No products should be suggested

    # ---- Edge case 2: products with zero or negative stock ----
    prod1 = make_product("Neg", -5)   # negative stock should be ignored
    prod2 = make_product("Zero", 0)   # zero stock should be ignored
    prod3 = make_product("Pos", 3)    # only this one is available
    inventory = make_inventory([prod1, prod2, prod3])

    engine = RecommendationEngine(inventory)
    result = engine.suggest_products(dummy_user)
    assert len(result) == 1
    assert result[0].name == "Pos"

    # ---- Edge case 3: exactly three products with stock ----
    p_a = make_product("A", 1)
    p_b = make_product("B", 2)
    p_c = make_product("C", 3)
    inventory = make_inventory([p_a, p_b, p_c])
    engine = RecommendationEngine(inventory)

    result = engine.suggest_products(dummy_user)
    assert len(result) == 3
    assert [p.name for p in result] == ["A", "B", "C"]


# ----------------------------------------------------------------------
# 3. Error cases  invalid inputs / missing attributes
# ----------------------------------------------------------------------
def test_suggest_products_error_cases():
    """
    Ensure that ``suggest_products`` raises appropriate exceptions when the
    ``RecommendationEngine`` is constructed with an invalid inventory
    (e.g., missing the ``products`` attribute) or when the inventory's
    ``products`` is not iterable.
    """
    dummy_user = Mock()

    # ---- Error case 1: inventory missing ``products`` attribute ----
    bad_inventory = Mock()
    # Deliberately do NOT set ``products`` on this mock
    from recommendation_engine import RecommendationEngine
    engine = RecommendationEngine(bad_inventory)

    with pytest.raises(AttributeError):
        engine.suggest_products(dummy_user)

    # ---- Error case 2: ``products`` is not a dict (e.g., None) ----
    bad_inventory2 = Mock()
    bad_inventory2.products = None  # Not iterable, will raise TypeError
    engine = RecommendationEngine(bad_inventory2)

    with pytest.raises(TypeError):
        engine.suggest_products(dummy_user)

    # ---- Error case 3: product objects missing ``stock`` attribute ----
    # The algorithm accesses ``p.stock``; if missing, AttributeError should be raised.
    incomplete_product = Mock()
    # No ``stock`` attribute set
    inventory = make_inventory([incomplete_product])
    engine = RecommendationEngine(inventory)

    with pytest.raises(AttributeError):
        engine.suggest_products(dummy_user)