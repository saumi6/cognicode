"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:12:22
Source file: payment_method.py
Function signature: def __init__(self, number: str, expiry: str, cvv: str)
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

# The class under test is assumed to be importable from the module where it is defined.
# Replace `my_module` with the actual module name if needed.
from __main__ import CreditCard  # using __main__ because the class definition is provided in the prompt


@pytest.mark.parametrize(
    "number, expiry, cvv",
    [
        ("4111111111111111", "2025-12-31", "123"),          # typical Visa, 3digit CVV
        ("5500000000000004", "2030-01-01", "1234"),         # typical MasterCard, 4digit CVV
        ("378282246310005", "2024-06-30", "999"),           # Amex, 3digit CVV
        ("6011000990139424", "2028-11-15", "000"),          # Discover, 3digit CVV
    ],
)
def test___init___normal_cases(number, expiry, cvv):
    """
    Test that the ``CreditCard.__init__`` method correctly stores the provided
    values for a set of normal, realistic inputs.
    """
    # Instantiate the object *without* invoking __init__ automatically
    card = CreditCard.__new__(CreditCard)
    # Manually call __init__
    card.__init__(number, expiry, cvv)

    # Verify that the attributes were set exactly as passed
    assert card.number == number
    assert card.expiry == expiry
    assert card.cvv == cvv


def test___init___edge_cases():
    """
    Test edgecase inputs such as empty strings, extremely long numbers,
    and unusual but still stringtyped expiry dates.
    """
    # Edge case 1: empty strings for all fields
    card1 = CreditCard.__new__(CreditCard)
    card1.__init__("", "", "")
    assert card1.number == ""
    assert card1.expiry == ""
    assert card1.cvv == ""

    # Edge case 2: very long card number (e.g., 30 digits)
    long_number = "9" * 30
    card2 = CreditCard.__new__(CreditCard)
    card2.__init__(long_number, "2099-12-31", "123")
    assert card2.number == long_number
    assert card2.expiry == "2099-12-31"
    assert card2.cvv == "123"

    # Edge case 3: expiry date far in the past (still a string)
    card3 = CreditCard.__new__(CreditCard)
    card3.__init__("1234567890123456", "1900-01-01", "999")
    assert card3.expiry == "1900-01-01"

    # Edge case 4: CVV with maximum allowed length (4) and leading zeros
    card4 = CreditCard.__new__(CreditCard)
    card4.__init__("4111111111111111", "2025-12-31", "0000")
    assert card4.cvv == "0000"


def test___init___error_cases():
    """
    Verify that ``CreditCard.__init__`` raises the appropriate builtin errors
    when called with an incorrect number of arguments.
    """
    # Missing one required argument (cvv)
    card = CreditCard.__new__(CreditCard)
    with pytest.raises(TypeError):
        card.__init__("4111111111111111", "2025-12-31")  # cvv omitted

    # Too many arguments
    card = CreditCard.__new__(CreditCard)
    with pytest.raises(TypeError):
        card.__init__("4111111111111111", "2025-12-31", "123", "extra_arg")

    # Passing nonstring types  while the implementation does not enforce type
    # checking, Python will still accept them; however, we can assert that a
    # ``TypeError`` is raised when the method signature is violated (e.g., None
    # for the ``self`` argument). This demonstrates error handling for misuse.
    with pytest.raises(TypeError):
        CreditCard.__init__(None, "4111111111111111", "2025-12-31", "123")