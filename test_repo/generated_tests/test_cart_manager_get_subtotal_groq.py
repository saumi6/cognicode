"""
Auto-generated test cases for function: get_subtotal
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:07:40
Source file: cart_manager.py
Function signature: def get_subtotal(self) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.cart_manager import CartManager

import pytest
from unittest.mock import Mock, MagicMock

# The class under test  adjust the import path to match the actual file name.
# For example, if the class lives in `cart_manager.py` the import would be:
# from cart_manager import CartManager
from cart_manager import CartManager


@pytest.mark.parametrize(
    "item_prices,expected",
    [
        # single item
        ([10.0], 10.0),
        # two items
        ([5.5, 4.5], 10.0),
        # three items with different values
        ([1.99, 2.01, 3.00], 7.0),
        # mixture of ints and floats
        ([100, 0.99, 20.01], 121.0),
    ],
)
def test_get_subtotal_normal_cases(item_prices, expected):
    """
    Normal cases  the subtotal should be the exact sum of the total prices
    returned by each CartItem.
    """
    # Arrange  create a CartManager with a dummy user and inject mocked items
    dummy_user = Mock()
    cart = CartManager(dummy_user)

    mocked_items = []
    for price in item_prices:
        item = Mock()
        item.get_total_price.return_value = price
        mocked_items.append(item)

    cart.items = mocked_items

    # Act
    result = cart.get_subtotal()

    # Assert
    assert result == pytest.approx(expected)


def test_get_subtotal_edge_cases():
    """
    Edgecase tests:
    * Empty cart  subtotal should be 0.0.
    * Very large numbers  ensure no overflow and correct float handling.
    * Floatingpoint rounding  use pytest.approx for tolerance.
    """
    dummy_user = Mock()
    cart = CartManager(dummy_user)

    # ---- Empty cart ---------------------------------------------------------
    cart.items = []
    assert cart.get_subtotal() == pytest.approx(0.0)

    # ---- Very large numbers -------------------------------------------------
    large_price = 1e18
    large_item = Mock()
    large_item.get_total_price.return_value = large_price
    cart.items = [large_item, large_item]  # two huge items
    expected_large = large_price * 2
    assert cart.get_subtotal() == pytest.approx(expected_large)

    # ---- Floatingpoint rounding --------------------------------------------
    # 0.1 + 0.2 is a classic floatingpoint pitfall; we expect 0.3 within tolerance.
    item_a = Mock()
    item_a.get_total_price.return_value = 0.1
    item_b = Mock()
    item_b.get_total_price.return_value = 0.2
    cart.items = [item_a, item_b]
    assert cart.get_subtotal() == pytest.approx(0.3)


def test_get_subtotal_error_cases():
    """
    Error cases  ensure that exceptions raised by a CartItems
    `get_total_price` method propagate out of `get_subtotal`.
    """
    dummy_user = Mock()
    cart = CartManager(dummy_user)

    # Item that raises a ValueError when its price is requested
    bad_item = Mock()
    bad_item.get_total_price.side_effect = ValueError("invalid price")

    # Normal item for control
    good_item = Mock()
    good_item.get_total_price.return_value = 10.0

    # ---- Single bad item ----------------------------------------------------
    cart.items = [bad_item]
    with pytest.raises(ValueError) as excinfo:
        cart.get_subtotal()
    assert "invalid price" in str(excinfo.value)

    # ---- Mixed good and bad items  the first bad one should raise ----------
    cart.items = [good_item, bad_item, good_item]
    with pytest.raises(ValueError):
        cart.get_subtotal()

    # ---- Item missing `get_total_price` attribute  AttributeError expected ---
    missing_method_item = MagicMock(spec=[])
    cart.items = [missing_method_item]
    with pytest.raises(AttributeError):
        cart.get_subtotal()