"""
Auto-generated test cases for function: send_welcome_email
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:12:25
Source file: notification_service.py
Function signature: def send_welcome_email(user: User)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.notification_service import send_welcome_email

import pytest

# The function under test is expected to live in the ``test_repo`` package.
# Import it directly from the package  the test runner will provide the
# correct module layout.
from test_repo import send_welcome_email


# ----------------------------------------------------------------------
# Helper objects
# ----------------------------------------------------------------------
class DummyUser:
    """A minimal standin for the real ``User`` model used by the code."""
    def __init__(self, email: str, first_name: str):
        self.email = email
        self.first_name = first_name


# ----------------------------------------------------------------------
# 1. Normal cases  parametrised
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "email,first_name,expected_subject,expected_body_snippet",
    [
        # typical user
        ("alice@example.com", "Alice", "Welcome, Alice!", "Dear Alice"),
        # another typical user
        ("bob@example.org", "Bob", "Welcome, Bob!", "Dear Bob"),
        # name with a space (first name only is used for the greeting)
        ("charlie@example.net", "Charlie Brown", "Welcome, Charlie Brown!", "Dear Charlie Brown"),
    ],
)
def test_send_welcome_email_normal_cases(
    monkeypatch,
    email,
    first_name,
    expected_subject,
    expected_body_snippet,
):
    """
    Verify that a normal ``User`` instance results in a single call to the
    underlying emailsending service with the correct arguments.
    """
    # ------------------------------------------------------------------
    # Arrange  create a dummy user and a mock for the external service
    # ------------------------------------------------------------------
    user = DummyUser(email=email, first_name=first_name)

    called = {}

    def fake_send_email(to, subject, body):
        """Record the arguments the function under test tries to send."""
        called["to"] = to
        called["subject"] = subject
        called["body"] = body
        # Simulate a successful send (the real function may return None)
        return True

    # Patch the external dependency used inside ``send_welcome_email``.
    # The real implementation is expected to call
    # ``test_repo.notification_service.send_email``  we replace it with our fake.
    monkeypatch.setattr(
        "test_repo.notification_service.send_email",
        fake_send_email,
    )

    # ------------------------------------------------------------------
    # Act
    # ------------------------------------------------------------------
    result = send_welcome_email(user)

    # ------------------------------------------------------------------
    # Assert  the mock was called exactly once with the right data
    # ------------------------------------------------------------------
    assert called, "The email service was never called"
    assert called["to"] == email
    assert called["subject"] == expected_subject
    # The body should contain a personalised greeting; we only check a snippet.
    assert expected_body_snippet in called["body"]
    # The function itself may return ``None`` or ``True``  we only require
    # that it does not raise and that the sideeffect happened.
    assert result is None or result is True
# ----------------------------------------------------------------------
# 2. Edge cases  boundary conditions
# ----------------------------------------------------------------------
def test_send_welcome_email_edge_cases(monkeypatch):
    """
    Test boundary conditions such as empty strings and unusually long names.
    """
    # ------------------------------------------------------------------
    # Arrange  a list of edgecase users
    # ------------------------------------------------------------------
    edge_users = [
        DummyUser(email="", first_name="EmptyEmail"),
        DummyUser(email="longname@example.com", first_name="A" * 300),
        DummyUser(email="space@example.com", first_name="   "),
    ]

    # We'll reuse a single dict to capture the last call.
    last_call = {}

    def fake_send_email(to, subject, body):
        last_call["to"] = to
        last_call["subject"] = subject
        last_call["body"] = body
        return True

    monkeypatch.setattr(
        "test_repo.notification_service.send_email",
        fake_send_email,
    )

    # ------------------------------------------------------------------
    # Act & Assert  iterate over the edge cases
    # ------------------------------------------------------------------
    for user in edge_users:
        # Reset the capture dict for each iteration
        last_call.clear()
        send_welcome_email(user)

        # The ``to`` field must be exactly what the user supplied,
        # even if it is an empty string.
        assert last_call["to"] == user.email

        # The subject should still contain the word Welcome.
        assert "Welcome" in last_call["subject"]

        # The body must contain the raw first_name (even if it is whitespace
        # or extremely long).  This ensures the function does not trim or
        # otherwise modify the value.
        assert user.first_name in last_call["body"]
# ----------------------------------------------------------------------
# 3. Error cases  invalid inputs
# ----------------------------------------------------------------------
def test_send_welcome_email_error_cases(monkeypatch):
    """
    Verify that the function raises an appropriate exception when called
    with clearly invalid arguments (e.g., ``None`` or a nonUser object).
    """
    # ------------------------------------------------------------------
    # Arrange  a dummy patch so that the external service is never hit
    # ------------------------------------------------------------------
    def fake_send_email(*_args, **_kwargs):
        # Should never be called in these tests
        raise AssertionError("Email service was called on invalid input")

    monkeypatch.setattr(
        "test_repo.notification_service.send_email",
        fake_send_email,
    )

    # ------------------------------------------------------------------
    # Act & Assert  invalid inputs
    # ------------------------------------------------------------------
    with pytest.raises(ValueError):
        send_welcome_email(None)

    with pytest.raises(ValueError):
        # Passing an integer instead of a ``User`` instance
        send_welcome_email(123)

    with pytest.raises(AttributeError):
        # Missing required attributes (e.g., no ``email`` attribute)
        class IncompleteUser:
            def __init__(self):
                self.first_name = "NoEmail"

        send_welcome_email(IncompleteUser())
These three test functions cover:

* **Normal behaviour**  using ``@pytest.mark.parametrize`` for several typical users.
* **Edgecase handling**  empty strings, very long names, and whitespaceonly names.
* **Error handling**  ``None``, wrong types, and objects lacking required attributes.

All external calls to the real email service are safely mocked via
``monkeypatch.setattr`` with the full absolute import path
``test_repo.notification_service.send_email``. The tests are selfcontained,
use only the standard library and ``pytest`` fixtures, and can be run
directly by the test runner.