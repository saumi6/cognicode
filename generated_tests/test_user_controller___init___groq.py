"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-02 03:12:35
Source file: user_controller.py
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
from test_repo.user_controller import UserController

import pytest
from unittest.mock import Mock, MagicMock

# The class lives in ``test_repo/user_controller.py``  use the full import path.
from test_repo.user_controller import UserController


# ----------------------------------------------------------------------
# Normal cases
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "user_svc_cls, auth_svc_cls",
    [
        (Mock, Mock),                     # both simple Mock objects
        (MagicMock, MagicMock),           # both MagicMock objects
        (type("CustomUserSvc", (object,), {}),  # a custom empty class
         type("CustomAuthSvc", (object,), {})),
    ],
)
def test___init___normal_cases(monkeypatch, user_svc_cls, auth_svc_cls):
    """
    Verify that ``UserController.__init__`` creates the expected attributes
    using the patched ``UserService`` and ``AuthService`` classes.
    """
    # Patch the external dependencies with the parametrised classes
    monkeypatch.setattr("test_repo.user_controller.UserService", user_svc_cls)
    monkeypatch.setattr("test_repo.user_controller.AuthService", auth_svc_cls)

    # Instantiate the controller (the original __init__ runs here, but we will
    # call it again after patching  this satisfies the requirement to
    # instantiate before calling __init__).
    controller = UserController()

    # Call __init__ explicitly so the patched classes are used.
    controller.__init__()

    # ``user_svc`` must be an instance of the patched ``UserService`` class.
    assert isinstance(controller.user_svc, user_svc_cls)

    # ``auth_svc`` must be an instance of the patched ``AuthService`` class.
    assert isinstance(controller.auth_svc, auth_svc_cls)

    # The ``AuthService`` constructor receives the ``user_svc`` instance.
    # For the simple mock classes we can only check that the attribute exists.
    if hasattr(controller.auth_svc, "user_svc"):
        assert controller.auth_svc.user_svc is controller.user_svc


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------
def test___init___edge_cases(monkeypatch):
    """
    Edge case: ``AuthService`` raises an exception during construction.
    """
    class DummyUserService:
        """A dummy service that does nothing."""
        pass

    class FailingAuthService:
        """AuthService that raises when instantiated."""
        def __init__(self, user_svc):
            raise RuntimeError("failed to initialise AuthService")

    # Patch the dependencies
    monkeypatch.setattr("test_repo.user_controller.UserService", DummyUserService)
    monkeypatch.setattr("test_repo.user_controller.AuthService", FailingAuthService)

    controller = UserController()

    # The second call to __init__ should raise the RuntimeError from AuthService.
    with pytest.raises(RuntimeError) as excinfo:
        controller.__init__()
    assert "failed to initialise AuthService" in str(excinfo.value)


# ----------------------------------------------------------------------
# Error cases
# ----------------------------------------------------------------------
def test___init___error_cases():
    """
    ``UserController.__init__`` does not accept any arguments.
    Passing extra arguments must raise ``TypeError``.
    """
    controller = UserController()

    # Directly calling the bound method with an unexpected argument.
    with pytest.raises(TypeError):
        controller.__init__("unexpected_argument")

    # Calling the unbound function via the class also raises TypeError.
    with pytest.raises(TypeError):
        UserController.__init__(controller, "another_bad_arg")