"""
Auto-generated test cases for function: display_number
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:12:54
Source file: payment_method.py
Function signature: def display_number(self) -> str
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.payment_method import CreditCard

import pytest
from unittest.mock import Mock

# NOTE:
# The class `CreditCard` and the helper `mask_card_number` are assumed to live in a module
# called ``credit_card`` (i.e. ``credit_card.py``).  Adjust the import path in the
# ``monkeypatch.setattr`` calls if the actual module name differs.
from credit_card import CreditCard


@pytest.mark.parametrize(
    "card_number, masked_result",
    [
        ("4111111111111111", "**** **** **** 1111"),
        ("5500000000000004", "**** **** **** 0004"),
        ("340000000000009",  "**** ****** *0009"),
        ("30000000000004",   "**** ****** *0004"),
    ],
)
def test_display_number_normal_cases(monkeypatch, card_number, masked_result):
    """
    Normal cases  verify that ``display_number`` returns the value produced by
    ``mask_card_number`` for typical creditcard numbers.
    """
    # Patch the helper so we can control its output without depending on its real implementation.
    def fake_mask(num):
        # Ensure the helper receives exactly the number we passed to the class.
        assert num == card_number
        return masked_result

    monkeypatch.setattr("credit_card.mask_card_number", fake_mask)

    # The other fields are not relevant for ``display_number``.
    card = CreditCard(number=card_number, expiry="2099-12-31", cvv="123")
    result = card.display_number()
    assert result == masked_result


def test_display_number_edge_cases(monkeypatch):
    """
    Edgecase tests  cover empty strings, extremely long numbers and numbers
    containing nondigit characters.
    """
    edge_cases = [
        ("", ""),                                 # empty number
        ("1", "1"),                               # single digit
        ("123456789012345678901234567890", "**** **** **** 7890"),  # very long number
        ("ABCD-1234-EFGH-5678", "****-****-****-5678"),            # mixed characters
    ]

    for raw_number, expected_mask in edge_cases:
        # Create a simple mask that just returns the expected value.
        fake_mask = Mock(return_value=expected_mask)
        monkeypatch.setattr("credit_card.mask_card_number", fake_mask)

        card = CreditCard(number=raw_number, expiry="2099-01-01", cvv="999")
        assert card.display_number() == expected_mask

        # Verify that the mocked helper was called exactly once with the raw number.
        fake_mask.assert_called_once_with(raw_number)
        fake_mask.reset_mock()


def test_display_number_error_cases(monkeypatch):
    """
    Error cases  ensure that ``display_number`` propagates exceptions raised by
    ``mask_card_number`` (e.g., when the input is not a string).
    """
    # Define inputs that should cause the helper to raise a ValueError.
    invalid_inputs = [None, 12345, 12.34, [], {}]

    for bad_input in invalid_inputs:
        # Configure the mock to raise ValueError when called.
        def raising_mask(_):
            raise ValueError("invalid card number")

        monkeypatch.setattr("credit_card.mask_card_number", raising_mask)

        # Initialise the CreditCard with the bad input; the constructor does not
        # validate the type, so the error will surface when ``display_number`` is called.
        card = CreditCard(number=bad_input, expiry="2099-06-30", cvv="321")

        with pytest.raises(ValueError):
            _ = card.display_number()