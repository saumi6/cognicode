"""
Auto-generated test cases for function: send_order_confirmation
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:12:44
Source file: notification_service.py
Function signature: def send_order_confirmation(user: User, order_id: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.notification_service import send_order_confirmation

import pytest

# The function under test is expected to live in the ``test_repo`` package.
# Import it directly  the test runner will make the package available.
from test_repo import send_order_confirmation


# ----------------------------------------------------------------------
# Helper objects
# ----------------------------------------------------------------------
class DummyUser:
    """A minimal standin for the real ``User`` model used by the code."""
    def __init__(self, user_id: str, email: str):
        self.id = user_id
        self.email = email


# ----------------------------------------------------------------------
# Normal cases
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "user, order_id, mock_return",
    [
        (DummyUser("u1", "alice@example.com"), "ORD-001", True),
        (DummyUser("u2", "bob@example.org"), "12345", True),
        (DummyUser("u3", "carol@sample.net"), "order-xyz-999", True),
    ],
)
def test_send_order_confirmation_normal_cases(monkeypatch, user, order_id, mock_return):
    """
    Verify that ``send_order_confirmation`` forwards the correct data to the
    underlying email service and returns the value produced by that service
    for typical inputs.
    """
    # Capture the arguments the email service receives.
    captured = {}

    def fake_send_email(to_address: str, subject: str, body: str):
        captured["to_address"] = to_address
        captured["subject"] = subject
        captured["body"] = body
        return mock_return

    # ``send_order_confirmation`` is expected to call
    # ``test_repo.email_service.send_email``  patch it with our fake.
    monkeypatch.setattr(
        "test_repo.email_service.send_email", fake_send_email
    )

    result = send_order_confirmation(user, order_id)

    # The function should return whatever the email service returns.
    assert result is mock_return

    # Verify that the email service was called with the expected values.
    assert captured["to_address"] == user.email
    assert order_id in captured["subject"]
    assert user.id in captured["body"]
    assert order_id in captured["body"]


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------
def test_send_order_confirmation_edge_cases(monkeypatch):
    """
    Test boundary conditions such as an empty order ID, a very long order ID,
    and a user with an empty email address.
    """
    # Prepare a user with an empty email address.
    user_empty_email = DummyUser("edge_user", "")

    # Very long order ID (200 characters).
    long_order_id = "ORD-" + "X" * 195

    # Store calls for later inspection.
    calls = []

    def fake_send_email(to_address: str, subject: str, body: str):
        calls.append((to_address, subject, body))
        return True

    monkeypatch.setattr(
        "test_repo.email_service.send_email", fake_send_email
    )

    # 1. Empty order ID  should still be sent (the function may allow it).
    result_empty = send_order_confirmation(user_empty_email, "")
    assert result_empty is True
    assert calls[-1][0] == ""  # to_address is empty
    assert "order" in calls[-1][1].lower()  # subject still mentions order

    # 2. Very long order ID  ensure it is passed through unchanged.
    result_long = send_order_confirmation(user_empty_email, long_order_id)
    assert result_long is True
    to_addr, subject, body = calls[-1]
    assert to_addr == ""  # still empty email
    assert long_order_id in subject
    assert long_order_id in body
    assert len(subject) <= 255  # typical email subject length limit (soft check)


# ----------------------------------------------------------------------
# Error cases
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad_user, bad_order_id, expected_exc",
    [
        (None, "ORD-123", ValueError),                     # user is None
        (DummyUser("u4", "dave@example.com"), None, TypeError),  # order_id is None
        ("not_a_user_obj", "ORD-456", TypeError),         # user is wrong type
        (DummyUser("u5", None), "ORD-789", ValueError),   # user.email is None
    ],
)
def test_send_order_confirmation_error_cases(monkeypatch, bad_user, bad_order_id, expected_exc):
    """
    Ensure that ``send_order_confirmation`` raises appropriate exceptions when
    supplied with invalid arguments.
    """
    # Patch the email service to guarantee it is **not** called in error paths.
    def should_not_be_called(*args, **kwargs):
        raise AssertionError("Email service should not be invoked on invalid input")

    monkeypatch.setattr(
        "test_repo.email_service.send_email", should_not_be_called
    )

    with pytest.raises(expected_exc):
        send_order_confirmation(bad_user, bad_order_id)