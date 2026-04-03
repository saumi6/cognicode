"""
Auto-generated test cases for function: register
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:52:24
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

# The module that contains the implementation is assumed to be named ``user_service``.
# Adjust the import path if the actual module name differs.
from user_service import UserService, User, ValidationError


@pytest.fixture(autouse=True)
def mock_logger(monkeypatch):
    """
    Replace the modulelevel ``logger`` with a ``MagicMock`` so that
    calls to ``logger.info`` do not produce real log output and can be
    inspected in the tests.
    """
    mock = MagicMock()
    # ``user_service`` is the absolute import path of the file that defines
    # ``UserService`` (i.e. the file you are testing).
    monkeypatch.setattr("user_service.logger", mock)
    return mock


@pytest.mark.parametrize(
    "name,email",
    [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.org"),
        ("Charlie", "charlie123@sub.domain.co"),
    ],
)
def test_register_normal_cases(name, email):
    """
    Normal registration scenarios:
    * a new user with a unique email address is created,
    * the returned ``User`` instance contains the supplied data,
    * the user is stored inside ``UserService.users``,
    * a log entry is emitted.
    """
    service = UserService()

    # Act
    user = service.register(name, email)

    # Assert the returned object
    assert isinstance(user, User)
    assert user.name == name
    assert user.email == email
    assert user.id in service.users

    # The stored user must be the same instance
    assert service.users[user.id] is user

    # Verify that a log call was made (the fixture replaces logger with a mock)
    from user_service import logger  # reimport to get the patched object
    logger.info.assert_called_once_with(f"User registered: {email}")


def test_register_edge_cases():
    """
    Edgecase registrations:
    * empty name is allowed (the service does not validate it),
    * very long email strings are accepted,
    * email addresses that differ only by case are treated as distinct.
    """
    service = UserService()

    # 1. Empty name
    empty_name_user = service.register("", "emptyname@example.com")
    assert empty_name_user.name == ""
    assert empty_name_user.email == "emptyname@example.com"

    # 2. Very long email (200 characters before the @)
    long_local = "a" * 200
    long_email = f"{long_local}@example.com"
    long_email_user = service.register("LongEmail", long_email)
    assert long_email_user.email == long_email
    assert len(long_email_user.email) > 200

    # 3. Casesensitive email handling
    lower = service.register("CaseTest", "case@example.com")
    upper = service.register("CaseTest2", "CASE@example.com")
    assert lower.email != upper.email
    assert lower.email == "case@example.com"
    assert upper.email == "CASE@example.com"
    # Both users must be present
    assert lower.id in service.users and upper.id in service.users


def test_register_error_cases():
    """
    Error scenarios:
    * registering a second user with an email that is already taken raises
      ``ValidationError``,
    * passing a nonstring email (e.g. ``None``) results in a ``TypeError``
      because the equality check fails.
    """
    service = UserService()
    # First registration succeeds
    service.register("First", "duplicate@example.com")

    # 1. Duplicate email
    with pytest.raises(ValidationError) as excinfo:
        service.register("Second", "duplicate@example.com")
    assert "Email taken" in str(excinfo.value)

    # 2. Nonstring email (None)  the ``==`` comparison will raise a TypeError
    with pytest.raises(TypeError):
        service.register("BadEmail", None)

    # 3. Nonstring name (integer)  the ``User`` constructor may accept it,
    #    but we ensure the service does not silently break; we expect a TypeError
    #    when the ``User`` class tries to use the value as a string.
    with pytest.raises(TypeError):
        service.register(12345, "intname@example.com")