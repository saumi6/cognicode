"""
Auto-generated test cases for function: is_valid
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:12:34
Source file: payment_method.py
Function signature: def is_valid(self) -> bool
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

# The class under test is assumed to live in a module named ``credit_card``.
# Adjust the import path if the actual module name differs.
from credit_card import CreditCard


@pytest.mark.parametrize(
    "expiry, cvv, expired_flag, expected",
    [
        # Normal, not expired and valid CVV lengths
        ("2025-12-31", "123", False, True),
        ("2025-12-31", "1234", False, True),
        # Not expired but invalid CVV length
        ("2025-12-31", "12", False, False),
        ("2025-12-31", "12345", False, False),
        # Expired card  should be invalid regardless of CVV length
        ("2020-01-01", "123", True, False),
        ("2020-01-01", "1234", True, False),
    ],
)
def test_is_valid_normal_cases(monkeypatch, expiry, cvv, expired_flag, expected):
    """
    Verify ``CreditCard.is_valid`` returns the correct boolean for typical
    combinations of expiry status and CVV length.
    """
    # Patch the ``is_expired`` helper used inside ``CreditCard.is_valid``.
    mock_is_expired = Mock(return_value=expired_flag)
    monkeypatch.setattr("credit_card.is_expired", mock_is_expired)

    card = CreditCard(number="4111111111111111", expiry=expiry, cvv=cvv)
    result = card.is_valid()

    # Ensure the helper was called with the exact expiry we supplied.
    mock_is_expired.assert_called_once_with(expiry)
    assert result is expected


def test_is_valid_edge_cases(monkeypatch):
    """
    Test boundary conditions such as the minimum/maximum allowed CVV length
    and a nonexpired flag that is explicitly ``False``.
    """
    # Edge CVV lengths (3 and 4) should be accepted.
    for cvv in ("000", "9999"):
        mock_is_expired = Mock(return_value=False)
        monkeypatch.setattr("credit_card.is_expired", mock_is_expired)

        card = CreditCard(number="5555555555554444", expiry="2099-12-31", cvv=cvv)
        assert card.is_valid() is True
        mock_is_expired.assert_called_once_with("2099-12-31")

    # Edge case: empty CVV (length 0)  should be invalid.
    mock_is_expired = Mock(return_value=False)
    monkeypatch.setattr("credit_card.is_expired", mock_is_expired)

    card = CreditCard(number="5555555555554444", expiry="2099-12-31", cvv="")
    assert card.is_valid() is False
    mock_is_expired.assert_called_once_with("2099-12-31")

    # Edge case: expiry string that would be considered today  we treat it as not expired.
    mock_is_expired = Mock(return_value=False)
    monkeypatch.setattr("credit_card.is_expired", mock_is_expired)

    card = CreditCard(number="5555555555554444", expiry="2024-04-02", cvv="123")
    assert card.is_valid() is True
    mock_is_expired.assert_called_once_with("2024-04-02")


def test_is_valid_error_cases(monkeypatch):
    """
    Ensure that ``CreditCard.is_valid`` propagates exceptions raised by the
    ``is_expired`` helper (e.g., when the expiry string is malformed).
    """
    # Simulate a malformed expiry date that causes ``is_expired`` to raise ``ValueError``.
    def explode(_):
        raise ValueError("invalid date format")

    monkeypatch.setattr("credit_card.is_expired", explode)

    card = CreditCard(number="378282246310005", expiry="not-a-date", cvv="123")
    with pytest.raises(ValueError):
        _ = card.is_valid()

    # Simulate a type error when a nonstring CVV is supplied.
    # ``len`` will raise ``TypeError`` for noniterables.
    mock_is_expired = Mock(return_value=False)
    monkeypatch.setattr("credit_card.is_expired", mock_is_expired)

    card = CreditCard(number="378282246310005", expiry="2025-01-01", cvv=123)  # cvv as int
    with pytest.raises(TypeError):
        _ = card.is_valid()