"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:13:00
Source file: user_service.py
Function signature: def __init__(self)
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

# The UserService class lives in the module ``test_repo.user_service``.
# Import it using the full absolute import path as required by the guidelines.
from test_repo.user_service import UserService


@pytest.mark.parametrize(
    "description",
    [
        ("basic instantiation"),
        ("reinstantiation after previous use"),
        ("instantiation inside a fixturelike scope"),
    ],
)
def test___init___normal_cases(description):
    """
    Normal cases for ``UserService.__init__``.

    We instantiate the class and verify that the attribute exists, is a ``dict`` and is empty.
    """
    # Act  instantiate the service (which calls __init__ automatically)
    service = UserService()

    # Assert  the ``users`` attribute is present, is a dict and starts empty
    assert hasattr(service, "users"), "UserService should have a 'users' attribute after init"
    assert isinstance(service.users, dict), "'users' should be a dict"
    assert len(service.users) == 0, "'users' dict should be empty on fresh init"


def test___init___edge_cases():
    """
    Edge cases for ``UserService.__init__``.

    1. When the service already contains data, calling ``__init__`` again should reset it.
    2. Calling ``__init__`` multiple times in a row must keep the dict empty.
    """
    # Arrange  create a service and manually inject a fake user entry
    service = UserService()
    fake_user = MagicMock()
    fake_user.id = "uid-123"
    service.users[fake_user.id] = fake_user
    assert len(service.users) == 1  # sanity check that the injection worked

    # Act  explicitly call __init__ again to reset internal state
    service.__init__()

    # Assert  the internal dict has been cleared
    assert isinstance(service.users, dict), "'users' should still be a dict after reinit"
    assert len(service.users) == 0, "'users' dict should be empty after reinit"

    # Act  call __init__ a second time to ensure idempotency
    service.__init__()

    # Assert  still empty
    assert len(service.users) == 0, "Repeated __init__ calls must leave 'users' empty"


def test___init___error_cases():
    """
    Error cases for ``UserService.__init__``.

    Supplying extra positional arguments or calling it with an invalid ``self`` should raise
    ``TypeError`` or ``AttributeError`` respectively.
    """
    # 1. Passing an extra argument should raise TypeError
    service = UserService()
    with pytest.raises(TypeError):
        # The bound method expects no extra arguments
        service.__init__("unexpected_argument")

    # 2. Calling the unbound function with ``None`` as ``self`` should raise AttributeError
    #    because the implementation tries to assign to ``self.users``.
    with pytest.raises(AttributeError):
        UserService.__init__(None)

    # 3. Calling the unbound function with an object that does not allow attribute assignment
    class NoAttr:
        __slots__ = ()  # prevents dynamic attribute creation

    with pytest.raises(AttributeError):
        UserService.__init__(NoAttr())