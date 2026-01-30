"""
Auto-generated test cases for function: deactivate
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:34:47
Source file: user.py
Function signature: def deactivate(self)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.user import User

import pytest
from unittest.mock import Mock

# The class under test is assumed to live in a module named ``user``.
# Import the public symbols that the class depends on so they can be
# monkeypatched to deterministic standins.
from user import User, generate_uuid, sanitize_email


@pytest.fixture(autouse=True)
def deterministic_helpers(monkeypatch):
    """
    Replace ``generate_uuid`` and ``sanitize_email`` with deterministic
    mocks for every test. This prevents sideeffects and makes the
    ``User`` objects predictable.
    """
    # ``generate_uuid`` normally returns a UUID string  we replace it with a
    # simple counter so each instance gets a unique but predictable id.
    counter = {"value": 0}

    def fake_uuid():
        counter["value"] += 1
        return f"uuid-{counter['value']}"

    monkeypatch.setattr("user.generate_uuid", fake_uuid)

    # ``sanitize_email`` normally normalises an email address  we just
    # return the lowercased string so the behaviour is obvious.
    monkeypatch.setattr("user.sanitize_email", lambda e: e.lower())

    # The fixture yields nothing; it only sets up the patches.
    yield


@pytest.mark.parametrize(
    "name,email,expected_id,expected_email",
    [
        ("Alice", "ALICE@EXAMPLE.COM", "uuid-1", "alice@example.com"),
        ("Bob", "bob@example.org", "uuid-2", "bob@example.org"),
        ("", "empty@domain.net", "uuid-3", "empty@domain.net"),
    ],
)
def test_deactivate_normal_cases(name, email, expected_id, expected_email):
    """
    Normal usage: a freshly created ``User`` is active; after calling
    ``deactivate`` the ``is_active`` flag must be ``False`` while other
    attributes stay unchanged.
    """
    # Arrange  create a user with deterministic helpers in place.
    user = User(name=name, email=email)

    # Sanity checks before deactivation.
    assert user.is_active is True
    assert user.id == expected_id
    assert user.email == expected_email
    assert user.name == name

    # Act  deactivate the user.
    user.deactivate()

    # Assert  the user is now inactive and no other attribute changed.
    assert user.is_active is False
    assert user.id == expected_id
    assert user.email == expected_email
    assert user.name == name


def test_deactivate_edge_cases():
    """
    Edge cases:
    * Deactivating a user that is already inactive should keep the flag ``False``.
    * Calling ``deactivate`` multiple times must be idempotent.
    * A user with no addresses (the default) should still deactivate correctly.
    """
    # Arrange  a normal user.
    user = User(name="Charlie", email="charlie@sample.com")

    # Edge case 1: already inactive.
    user.is_active = False
    user.deactivate()
    assert user.is_active is False, "Deactivating an already inactive user should stay False"

    # Edge case 2: multiple calls.
    user.is_active = True
    for _ in range(3):
        user.deactivate()
    assert user.is_active is False, "Multiple deactivate calls must leave the user inactive"

    # Edge case 3: user without any addresses (addresses list is empty by default).
    assert user.addresses == [], "User should start with an empty address list"
    user.deactivate()
    assert user.is_active is False, "User without addresses must still deactivate correctly"


def test_deactivate_error_cases():
    """
    Error cases:
    * ``deactivate`` does not accept any positional arguments  passing one
      should raise ``TypeError``.
    * Calling ``deactivate`` on an object that is not a ``User`` instance
      (e.g., ``None``) should also raise ``AttributeError`` when the method
      lookup fails.
    """
    # Arrange  a proper user instance for the first error scenario.
    user = User(name="Dana", email="dana@domain.org")

    # Error case 1: too many arguments.
    with pytest.raises(TypeError):
        # ``deactivate`` is defined without parameters; providing one triggers
        # the builtin Python argument checking.
        user.deactivate("unexpected_argument")

    # Error case 2: calling the unbound method on a nonUser object.
    # We retrieve the function object from the class and invoke it with an
    # inappropriate ``self``.
    unbound_deactivate = User.deactivate
    with pytest.raises(AttributeError):
        unbound_deactivate(None)  # ``None`` has no ``is_active`` attribute