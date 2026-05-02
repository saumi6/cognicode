"""
Auto-generated test cases for function: register
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:13:09
Source file: user_service.py
Function signature: def register(self, name: str, email: str) -> User
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.user_service import UserService

import pytest
from unittest.mock import MagicMock

# The implementation lives in ``test_repo/user_service.py``.
# Import the public objects we need for the tests.
from test_repo.user_service import UserService, ValidationError, User


@pytest.mark.parametrize(
    "name,email",
    [
        ("Alice", "alice@example.com"),
        ("Bob", "bob.smith@example.co.uk"),
        ("Charlie Chaplin", "charlie+test@sub.domain.org"),
        ("Dana", "dana_123@example.io"),
    ],
)
def test_register_normal_cases(monkeypatch, name, email):
    """
    Normal registration scenarios.

    For each (name, email) pair we expect:
    * a ``User`` instance is returned,
    * the instance attributes match the inputs,
    * the user is stored in ``UserService.users`` under its ``id``,
    * a log entry is emitted via ``logger.info``.
    """
    # Arrange  create a fresh service and replace the logger with a mock.
    service = UserService()
    mock_logger = MagicMock()
    monkeypatch.setattr("test_repo.user_service.logger", mock_logger)

    # Act  register the user.
    user = service.register(name, email)

    # Assert  returned object type and attributes.
    assert isinstance(user, User)
    assert user.name == name
    assert user.email == email
    # The user must be stored in the internal dict keyed by its id.
    assert user.id in service.users
    assert service.users[user.id] is user
    # The logger should have been called exactly once with the expected message.
    mock_logger.info.assert_called_once_with(f"User registered: {email}")


def test_register_edge_cases(monkeypatch):
    """
    Edgecase registrations.

    Covers:
    * empty name,
    * extremely long name,
    * email with unusual but valid characters,
    * email containing uppercase letters (should be stored asis).
    """
    service = UserService()
    mock_logger = MagicMock()
    monkeypatch.setattr("test_repo.user_service.logger", mock_logger)

    # 1. Empty name  still allowed by the current implementation.
    empty_name_user = service.register("", "emptyname@example.com")
    assert empty_name_user.name == ""
    assert empty_name_user.email == "emptyname@example.com"
    assert empty_name_user.id in service.users

    # 2. Very long name (200 characters).
    long_name = "L" * 200
    long_name_user = service.register(long_name, "longname@example.com")
    assert long_name_user.name == long_name
    assert long_name_user.email == "longname@example.com"
    assert long_name_user.id in service.users

    # 3. Email with plus, dots and subdomains.
    complex_email = "first.last+category@sub.mail.example-domain.com"
    complex_user = service.register("Complex Email", complex_email)
    assert complex_user.email == complex_email
    assert complex_user.name == "Complex Email"
    assert complex_user.id in service.users

    # 4. Uppercase email  the service does not normalise case, so it should be stored unchanged.
    upper_email = "UPPERCASE@EXAMPLE.COM"
    upper_user = service.register("Uppercase", upper_email)
    assert upper_user.email == upper_email
    assert upper_user.name == "Uppercase"
    assert upper_user.id in service.users

    # Verify that logger.info was called once per successful registration (4 times total).
    assert mock_logger.info.call_count == 4
    expected_calls = [
        pytest.call(f"User registered: emptyname@example.com"),
        pytest.call(f"User registered: longname@example.com"),
        pytest.call(f"User registered: {complex_email}"),
        pytest.call(f"User registered: {upper_email}"),
    ]
    mock_logger.info.assert_has_calls(expected_calls, any_order=False)


def test_register_error_cases(monkeypatch):
    """
    Error scenarios for ``UserService.register``.

    * Registering a second user with an email that already exists must raise ``ValidationError``.
    * Passing a nonstring type for ``email`` should raise a ``TypeError`` when the equality check is performed.
    """
    service = UserService()
    mock_logger = MagicMock()
    monkeypatch.setattr("test_repo.user_service.logger", mock_logger)

    # First registration succeeds.
    first_user = service.register("First", "duplicate@example.com")
    assert first_user.email == "duplicate@example.com"

    # Attempt to register another user with the same email  expect ValidationError.
    with pytest.raises(ValidationError) as excinfo:
        service.register("Second", "duplicate@example.com")
    assert "Email taken" in str(excinfo.value)

    # The logger should have been called only for the successful first registration.
    mock_logger.info.assert_called_once_with("User registered: duplicate@example.com")

    # Passing a nonstring email (e.g., an integer) triggers a TypeError during the equality comparison.
    # The implementation does not explicitly check types, so Python will raise a TypeError when
    # ``u.email == email`` is evaluated (comparing ``str`` to ``int``).
    with pytest.raises(TypeError):
        service.register("InvalidEmail", 12345)  # type: ignore[arg-type]