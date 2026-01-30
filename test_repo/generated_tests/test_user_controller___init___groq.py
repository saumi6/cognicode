"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:15:57
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
from unittest.mock import MagicMock, Mock

# The class under test lives in a module named ``user_controller``.
# Adjust the import path if the actual module name differs.
from user_controller import UserController


@pytest.mark.parametrize(
    "user_svc_cls, auth_svc_cls, expected_user_svc_type, expected_auth_svc_type",
    [
        # Normal case  both services are simple MagicMock instances.
        (MagicMock, MagicMock, MagicMock, MagicMock),
        # Normal case  custom lightweight mock classes that record init arguments.
        (
            lambda: Mock(name="CustomUserService"),
            lambda user_svc: Mock(name="CustomAuthService", spec=["login"], user_svc=user_svc),
            Mock,
            Mock,
        ),
    ],
)
def test___init___normal_cases(
    monkeypatch,
    user_svc_cls,
    auth_svc_cls,
    expected_user_svc_type,
    expected_auth_svc_type,
):
    """
    Verify that ``UserController.__init__`` correctly creates and assigns
    ``user_svc`` and ``auth_svc`` attributes for typical (nonerror) scenarios.
    """
    # ------------------------------------------------------------------ #
    # Patch the concrete service classes that ``UserController`` imports.
    # The full absolute import path is required for ``monkeypatch.setattr``.
    # ------------------------------------------------------------------ #
    monkeypatch.setattr("user_controller.UserService", user_svc_cls)
    monkeypatch.setattr("user_controller.AuthService", auth_svc_cls)

    # Create an *uninitialized* instance and call ``__init__`` manually so that
    # the monkeypatched classes are used.
    controller = UserController.__new__(UserController)
    controller.__init__()  # pylint: disable=unnecessary-dunder-call

    # ------------------------------------------------------------------ #
    # Assertions  the attributes must exist and be instances of the expected
    # (mocked) types.
    # ------------------------------------------------------------------ #
    assert hasattr(controller, "user_svc")
    assert hasattr(controller, "auth_svc")
    assert isinstance(controller.user_svc, expected_user_svc_type)
    assert isinstance(controller.auth_svc, expected_auth_svc_type)

    # For the custom mock case we also ensure that ``AuthService`` received the
    # exact ``user_svc`` instance that ``UserController`` created.
    if isinstance(controller.auth_svc, Mock) and hasattr(controller.auth_svc, "user_svc"):
        assert controller.auth_svc.user_svc is controller.user_svc


def test___init___edge_cases(monkeypatch):
    """
    Edgecase tests for ``UserController.__init__``:
    * ``UserService`` returns ``None``  ``AuthService`` should still be
      instantiated with that ``None`` value.
    * ``AuthService`` raises an exception during its construction  the
      exception must propagate.
    """
    # ------------------------------------------------------------------ #
    # Edge case 1  ``UserService`` returns ``None``.
    # ------------------------------------------------------------------ #
    class NullUserService:
        """A standin that mimics a service returning ``None`` on init."""
        def __init__(self):
            # Simulate a failure to create a usable service object.
            pass

    class DummyAuthService:
        """Accepts any argument; records what it received."""
        def __init__(self, user_svc):
            self.received_user_svc = user_svc

    monkeypatch.setattr("user_controller.UserService", NullUserService)
    monkeypatch.setattr("user_controller.AuthService", DummyAuthService)

    controller = UserController.__new__(UserController)
    controller.__init__()  # pylint: disable=unnecessary-dunder-call

    # ``user_svc`` should be an instance of ``NullUserService`` (not ``None``).
    assert isinstance(controller.user_svc, NullUserService)
    # ``auth_svc`` must have received the same (nonNone) object.
    assert controller.auth_svc.received_user_svc is controller.user_svc

    # ------------------------------------------------------------------ #
    # Edge case 2  ``AuthService`` raises during construction.
    # ------------------------------------------------------------------ #
    class RaisingAuthService:
        """Always raises when instantiated."""
        def __init__(self, *_):
            raise RuntimeError("AuthService failed to initialise")

    monkeypatch.setattr("user_controller.AuthService", RaisingAuthService)

    # ``UserService`` can be a simple mock  it is not the focus of this case.
    monkeypatch.setattr("user_controller.UserService", MagicMock)

    controller = UserController.__new__(UserController)
    with pytest.raises(RuntimeError, match="AuthService failed to initialise"):
        controller.__init__()  # pylint: disable=unnecessary-dunder-call


def test___init___error_cases(monkeypatch):
    """
    Errorcase tests for ``UserController.__init__``:
    * Calling ``__init__`` with unexpected positional arguments should raise
      ``TypeError``.
    * Providing a noncallable object for ``UserService`` should raise
      ``TypeError`` when the controller attempts to instantiate it.
    """
    # ------------------------------------------------------------------ #
    # Setup normal mocks so that the only error source is the misuse of __init__.
    # ------------------------------------------------------------------ #
    monkeypatch.setattr("user_controller.UserService", MagicMock)
    monkeypatch.setattr("user_controller.AuthService", MagicMock)

    # 1. ``__init__`` receives an unexpected argument.
    controller = UserController.__new__(UserController)
    with pytest.raises(TypeError):
        # The real ``__init__`` signature takes only ``self``.
        controller.__init__("unexpected_argument")  # pylint: disable=unnecessary-dunder-call

    # ------------------------------------------------------------------ #
    # 2. ``UserService`` is replaced with a noncallable (e.g., an int).
    # ------------------------------------------------------------------ #
    monkeypatch.setattr("user_controller.UserService", 123)  # not callable

    controller = UserController.__new__(UserController)
    with pytest.raises(TypeError):
        controller.__init__()  # pylint: disable=unnecessary-dunder-call