"""
Auto-generated test cases for function: qualifies_for_free_shipping
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:07:44
Source file: cart_manager.py
Function signature: def qualifies_for_free_shipping(self) -> bool
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

# The class under test is assumed to live in a module named ``cart_manager``.
# Adjust the import path if the actual module name differs.
from cart_manager import CartManager


@pytest.mark.parametrize(
    "subtotal, threshold, expected",
    [
        (0.0, 50.0, False),          # empty cart  far below threshold
        (10.99, 20.0, False),        # below threshold
        (20.01, 20.0, True),         # just above threshold
        (100.0, 75.5, True),         # well above threshold
        (75.5, 75.5, False),         # exactly equal  not free
    ],
)
def test_qualifies_for_free_shipping_normal_cases(monkeypatch, subtotal, threshold, expected):
    """
    Normal cases for ``qualifies_for_free_shipping``:
    - Subtotal below the freeshipping threshold should return ``False``.
    - Subtotal strictly greater than the threshold should return ``True``.
    """
    # Mock a user  the concrete type is irrelevant for this test.
    mock_user = Mock()

    # Instantiate the manager.
    cart = CartManager(mock_user)

    # Force the ``FREE_SHIPPING_THRESHOLD`` used inside the method.
    monkeypatch.setattr("cart_manager.FREE_SHIPPING_THRESHOLD", threshold)

    # Monkeypatch ``get_subtotal`` to return the desired subtotal without
    # having to build real ``CartItem`` objects.
    monkeypatch.setattr(cart, "get_subtotal", lambda: subtotal)

    # Exercise the method under test.
    result = cart.qualifies_for_free_shipping()

    # Verify the outcome.
    assert result is expected


def test_qualifies_for_free_shipping_edge_cases(monkeypatch):
    """
    Edgecase tests:
    - Subtotal exactly equal to the threshold (should be ``False``).
    - Very large subtotal (should be ``True``).
    - Empty cart (subtotal = 0, should be ``False``).
    """
    mock_user = Mock()
    cart = CartManager(mock_user)

    # 1  Exactthreshold case
    monkeypatch.setattr("cart_manager.FREE_SHIPPING_THRESHOLD", 100.0)
    monkeypatch.setattr(cart, "get_subtotal", lambda: 100.0)
    assert cart.qualifies_for_free_shipping() is False

    # 2  Very large subtotal
    monkeypatch.setattr(cart, "get_subtotal", lambda: 1_000_000.0)
    assert cart.qualifies_for_free_shipping() is True

    # 3  Empty cart (subtotal 0)
    monkeypatch.setattr(cart, "get_subtotal", lambda: 0.0)
    assert cart.qualifies_for_free_shipping() is False


def test_qualifies_for_free_shipping_error_cases(monkeypatch):
    """
    Errorcase tests:
    - ``get_subtotal`` raises a ``TypeError`` (e.g., due to corrupted item data).
    - ``FREE_SHIPPING_THRESHOLD`` is set to a nonnumeric value, causing a ``TypeError``.
    """
    mock_user = Mock()
    cart = CartManager(mock_user)

    # Case 1: ``get_subtotal`` raises an exception.
    def broken_subtotal():
        raise TypeError("subtotal is not a number")

    monkeypatch.setattr(cart, "get_subtotal", broken_subtotal)
    monkeypatch.setattr("cart_manager.FREE_SHIPPING_THRESHOLD", 50.0)

    with pytest.raises(TypeError):
        cart.qualifies_for_free_shipping()

    # Case 2: ``FREE_SHIPPING_THRESHOLD`` is nonnumeric.
    monkeypatch.setattr(cart, "get_subtotal", lambda: 60.0)
    monkeypatch.setattr("cart_manager.FREE_SHIPPING_THRESHOLD", "not-a-number")

    with pytest.raises(TypeError):
        cart.qualifies_for_free_shipping()