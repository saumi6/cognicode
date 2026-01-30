"""
Auto-generated test cases for function: get_primary_address
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:34:38
Source file: user.py
Function signature: def get_primary_address(self) -> Optional[Address]
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

# ----------------------------------------------------------------------
# Normal cases
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "address_count, expected_is_none",
    [
        (0, True),          # no addresses  None
        (1, False),         # single address  that address
        (3, False),         # multiple addresses  first address
    ],
)
def test_get_primary_address_normal_cases(address_count, expected_is_none):
    """
    Verify that ``User.get_primary_address`` returns the first address when
    addresses are present and ``None`` when the list is empty.
    """
    # Arrange  create a user and populate it with the requested number of mock
    # Address objects.
    user = User(name="John Doe", email="john.doe@example.com")
    mock_addresses = [Mock(name=f"addr_{i}") for i in range(address_count)]
    for addr in mock_addresses:
        user.add_address(addr)

    # Act
    primary = user.get_primary_address()

    # Assert
    if expected_is_none:
        assert primary is None
    else:
        # The first mock we added should be returned and it must be the exact
        # same object (identity check).
        assert primary is mock_addresses[0]
        # Ensure that the returned object is one of the mocks we supplied.
        assert primary in mock_addresses


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------
def test_get_primary_address_edge_cases():
    """
    Test boundary conditions such as a list containing ``None`` as the first
    element and the immutability of the returned reference.
    """
    # 1. List with a ``None`` as the first element  the method should return
    #    that ``None`` value (it does not filter the list).
    user_none_first = User(name="Edge", email="edge@example.com")
    user_none_first.addresses = [None, Mock(name="addr_valid")]
    assert user_none_first.get_primary_address() is None

    # 2. Verify that the returned address is the exact object stored in the
    #    list (i.e., a reference, not a copy). Mutating the mock after the call
    #    should be observable through the returned reference.
    user_mutable = User(name="Mutable", email="mutable@example.com")
    mutable_addr = Mock(name="mutable_addr")
    user_mutable.add_address(mutable_addr)

    primary_before = user_mutable.get_primary_address()
    assert primary_before is mutable_addr

    # Mutate the mock (add an attribute) and ensure the change is visible via
    # the previously obtained reference.
    mutable_addr.new_attribute = "changed"
    assert hasattr(primary_before, "new_attribute")
    assert primary_before.new_attribute == "changed"

    # 3. Adding addresses after the primary has been fetched should not alter
    #    the alreadyretrieved primary address.
    user_late_add = User(name="LateAdd", email="late@example.com")
    first_addr = Mock(name="first")
    second_addr = Mock(name="second")
    user_late_add.add_address(first_addr)

    primary_initial = user_late_add.get_primary_address()
    user_late_add.add_address(second_addr)  # add later

    # The primary should still be the original first address.
    assert primary_initial is first_addr
    assert user_late_add.get_primary_address() is first_addr


# ----------------------------------------------------------------------
# Error cases
# ----------------------------------------------------------------------
def test_get_primary_address_error_cases():
    """
    Ensure that inappropriate internal state of ``addresses`` raises a clear
    exception rather than silently failing.
    """
    user = User(name="ErrorCase", email="error@example.com")

    # Case 1  ``addresses`` set to ``None`` (not subscriptable)
    user.addresses = None
    with pytest.raises(TypeError):
        _ = user.get_primary_address()

    # Case 2  ``addresses`` set to an integer (also not subscriptable)
    user.addresses = 42
    with pytest.raises(TypeError):
        _ = user.get_primary_address()

    # Case 3  ``addresses`` set to an object that raises on indexing
    class BadContainer:
        def __getitem__(self, _):
            raise RuntimeError("indexing not allowed")

    user.addresses = BadContainer()
    with pytest.raises(RuntimeError, match="indexing not allowed"):
        _ = user.get_primary_address()