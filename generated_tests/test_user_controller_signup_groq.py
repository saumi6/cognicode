"""
Auto-generated test cases for function: signup
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-02 03:13:24
Source file: user_controller.py
Function signature: def signup(self, name: str, email: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.user_controller import UserController

import pytest
from unittest.mock import MagicMock

# NOTE: The module that contains `UserController` is assumed to be
# `test_repo.user_controller` (the repository name is `test_repo` as
# indicated in the prompt).  All monkeypatches therefore use the full
# absolute import path `test_repo.user_controller.<name>`.


@pytest.mark.parametrize(
    "name,email,expected",
    [
        ("Alice", "alice@example.com", {"id": 1, "name": "Alice", "email": "alice@example.com"}),
        ("Bob", "bob@example.org", {"id": 2, "name": "Bob", "email": "bob@example.org"}),
        ("Charlie", "c@example.net", {"id": 3, "name": "Charlie", "email": "c@example.net"}),
    ],
)
def test_signup_normal_cases(monkeypatch, name, email, expected):
    """Normal usage of ``UserController.signup`` with typical inputs."""
    # ------------------------------------------------------------------
    # Prepare a mock UserService whose ``register`` method returns the
    # ``expected`` value for the given inputs.
    # ------------------------------------------------------------------
    mock_user_service = MagicMock()
    mock_user_service.register.return_value = expected

    # Patch the concrete ``UserService`` class used inside ``UserController``.
    monkeypatch.setattr(
        "test_repo.user_controller.UserService",
        lambda: mock_user_service,
    )

    # Import the class after the patch so that the patched ``UserService``
    # is used during ``UserController`` construction.
    from test_repo.user_controller import UserController

    controller = UserController()

    # Call the method under test.
    result = controller.signup(name, email)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    assert result == expected
    mock_user_service.register.assert_called_once_with(name, email)


def test_signup_edge_cases(monkeypatch):
    """Edgecase handling such as empty strings, very long values and special characters."""
    # ------------------------------------------------------------------
    # Create a mock service that simply echoes back the received arguments
    # inside a dict (including a fabricated id).
    # ------------------------------------------------------------------
    def echo_register(name, email):
        # Produce a deterministic id based on length to keep the test simple.
        return {"id": len(name) + len(email), "name": name, "email": email}

    mock_user_service = MagicMock()
    mock_user_service.register.side_effect = echo_register

    monkeypatch.setattr(
        "test_repo.user_controller.UserService",
        lambda: mock_user_service,
    )

    from test_repo.user_controller import UserController

    controller = UserController()

    # 1. Empty strings  the mock will still return a dict.
    result_empty = controller.signup("", "")
    assert result_empty == {"id": 0, "name": "", "email": ""}

    # 2. Very long name (1000 characters) and a normal email.
    long_name = "A" * 1000
    email = "longname@example.com"
    result_long = controller.signup(long_name, email)
    expected_id = len(long_name) + len(email)
    assert result_long == {"id": expected_id, "name": long_name, "email": email}
    # Ensure the mock was called the correct number of times.
    assert mock_user_service.register.call_count == 2

    # 3. Name with Unicode characters and email with subdomains.
    name_unicode = "Jrgen "
    email_complex = "user@mail.sub.example.co.uk"
    result_unicode = controller.signup(name_unicode, email_complex)
    expected_id = len(name_unicode) + len(email_complex)
    assert result_unicode == {"id": expected_id, "name": name_unicode, "email": email_complex}


@pytest.mark.parametrize(
    "name,email,exception_type",
    [
        (None, "test@example.com", ValueError),
        ("Test", None, ValueError),
        (123, "test@example.com", TypeError),
        ("Test", 456, TypeError),
        ("BadEmail", "not-an-email", ValueError),
    ],
)
def test_signup_error_cases(monkeypatch, name, email, exception_type):
    """Invalid inputs should cause the underlying service to raise an exception,
    which propagates through ``UserController.signup``."""
    # ------------------------------------------------------------------
    # Mock ``UserService.register`` to raise the appropriate exception
    # based on the supplied arguments.
    # ------------------------------------------------------------------
    def register_side_effect(passed_name, passed_email):
        if not isinstance(passed_name, str):
            raise TypeError("name must be a string")
        if not isinstance(passed_email, str):
            raise TypeError("email must be a string")
        if passed_name is None or passed_email is None:
            raise ValueError("name and email cannot be None")
        if "@" not in passed_email:
            raise ValueError("invalid email format")
        # Normal path (should not be reached in these parametrized cases)
        return {"id": 0, "name": passed_name, "email": passed_email}

    mock_user_service = MagicMock()
    mock_user_service.register.side_effect = register_side_effect

    monkeypatch.setattr(
        "test_repo.user_controller.UserService",
        lambda: mock_user_service,
    )

    from test_repo.user_controller import UserController

    controller = UserController()

    # ------------------------------------------------------------------
    # The call should raise the expected exception type.
    # ------------------------------------------------------------------
    with pytest.raises(exception_type):
        controller.signup(name, email)

    # Verify that ``register`` was indeed invoked with the problematic values.
    mock_user_service.register.assert_called_once_with(name, email)