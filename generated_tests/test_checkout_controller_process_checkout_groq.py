"""
Auto-generated test cases for function: process_checkout
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:16:51
Source file: checkout_controller.py
Function signature: def process_checkout(self, cart: CartManager, card: CreditCard)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.checkout_controller import CheckoutController

import pytest
from unittest.mock import Mock

# The class under test is assumed to be importable from the module where it is defined.
# Replace `your_module` with the actual module name if needed.
from your_module import CheckoutController, ValidationError, PaymentError


@pytest.mark.parametrize(
    "cart_items,total,card_number",
    [
        (["apple", "banana"], 23.50, "4111111111111111"),
        (["book"], 9.99, "5500000000000004"),
        (["laptop", "mouse", "keyboard"], 1250.00, "340000000000009"),
    ],
)
def test_process_checkout_normal_cases(cart_items, total, card_number, capsys):
    """
    Normal operation: a nonempty cart, a valid credit card and a successful charge.
    """
    # Arrange ---------------------------------------------------------------
    controller = CheckoutController()

    # Mock the cart manager
    mock_cart = Mock()
    mock_cart.items = cart_items

    # Mock the credit card
    mock_card = Mock()
    mock_card.is_valid.return_value = True
    mock_card.display_number.return_value = card_number

    # Stub out the price calculator to return the desired total
    controller.calc.calculate_total = Mock(return_value=total)

    # Act -------------------------------------------------------------------
    result = controller.process_checkout(mock_cart, mock_card)

    # Assert ----------------------------------------------------------------
    assert result is True

    captured = capsys.readouterr()
    expected_suffix = card_number[-4:]
    assert f"Charged {total} to card ending in {expected_suffix}" in captured.out


def test_process_checkout_edge_cases(capsys):
    """
    Edge cases:
    * Cart with a single item.
    * Total amount of zero (e.g., all items are free).
    * Card number that ends with ``0000``.
    """
    # Arrange ---------------------------------------------------------------
    controller = CheckoutController()

    # Cart with a single (free) item
    mock_cart = Mock()
    mock_cart.items = ["free_sample"]

    # Credit card that ends with 0000
    mock_card = Mock()
    mock_card.is_valid.return_value = True
    mock_card.display_number.return_value = "0000000000000000"

    # Force the total to be zero
    controller.calc.calculate_total = Mock(return_value=0)

    # Act -------------------------------------------------------------------
    result = controller.process_checkout(mock_cart, mock_card)

    # Assert ----------------------------------------------------------------
    assert result is True

    captured = capsys.readouterr()
    assert "Charged 0 to card ending in 0000" in captured.out


def test_process_checkout_error_cases():
    """
    Error handling:
    * Empty cart should raise ``ValidationError``.
    * Invalid credit card should raise ``PaymentError``.
    """
    controller = CheckoutController()

    # ---- Empty cart --------------------------------------------------------
    empty_cart = Mock()
    empty_cart.items = []  # No items

    valid_card = Mock()
    valid_card.is_valid.return_value = True
    valid_card.display_number.return_value = "4111111111111111"

    with pytest.raises(ValidationError):
        controller.process_checkout(empty_cart, valid_card)

    # ---- Invalid card -------------------------------------------------------
    nonempty_cart = Mock()
    nonempty_cart.items = ["item"]

    invalid_card = Mock()
    invalid_card.is_valid.return_value = False
    invalid_card.display_number.return_value = "5500000000000004"

    with pytest.raises(PaymentError):
        controller.process_checkout(nonempty_cart, invalid_card)