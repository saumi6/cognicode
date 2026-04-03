"""
Auto-generated test cases for function: get_user_data
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 13:01:58
Source file: external_api.py
Function signature: def get_user_data(user_id: int) -> dict
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.external_api import get_user_data

import json
import types

import pytest
import requests

# The function under test is expected to be importable from the projects
# source tree.  Adjust the import path if the module name differs.
from my_module import get_user_data  # <-- replace `my_module` with the real module name


def _make_mock_response(json_data: dict, status_code: int = 200):
    """
    Helper that creates a minimal ``requests.Response``like object
    with the required ``json`` method and ``status_code`` attribute.
    """
    mock_resp = types.SimpleNamespace()
    mock_resp.status_code = status_code
    mock_resp.json = lambda: json_data
    mock_resp.text = json.dumps(json_data)
    return mock_resp


@pytest.mark.parametrize(
    "user_id, api_return, expected",
    [
        # typical successful responses
        (1, {"id": 1, "name": "Alice", "email": "alice@example.com"},
         {"id": 1, "name": "Alice", "email": "alice@example.com"}),
        (42, {"id": 42, "name": "Bob", "email": "bob@example.org"},
         {"id": 42, "name": "Bob", "email": "bob@example.org"}),
        (999, {"id": 999, "name": "Carol", "email": "carol@sample.net"},
         {"id": 999, "name": "Carol", "email": "carol@sample.net"}),
    ],
)
def test_get_user_data_normal_cases(monkeypatch, user_id, api_return, expected):
    """
    Normal cases  the external API returns a 200 response with a wellformed JSON
    payload.  The function should return the JSON unchanged.
    """
    # Patch ``requests.get`` so no real HTTP request is performed.
    def fake_get(url, params=None, **kwargs):
        # Verify that the URL contains the user_id we expect (basic sanity check)
        assert str(user_id) in url
        return _make_mock_response(api_return, status_code=200)

    monkeypatch.setattr("requests.get", fake_get)

    result = get_user_data(user_id)
    assert result == expected


def test_get_user_data_edge_cases(monkeypatch):
    """
    Edge cases  test boundary values and unusual but still valid API responses.
    """
    # 1. user_id = 0 (often used as a sentinel).  Assume the API returns an empty dict.
    def fake_get_zero(url, params=None, **kwargs):
        assert "/0" in url
        return _make_mock_response({}, status_code=200)

    monkeypatch.setattr("requests.get", fake_get_zero)
    assert get_user_data(0) == {}

    # 2. Very large user_id  ensure the function can handle big integers.
    large_id = 2**31 - 1
    large_payload = {"id": large_id, "name": "MaxInt", "email": "max@example.com"}

    def fake_get_large(url, params=None, **kwargs):
        assert str(large_id) in url
        return _make_mock_response(large_payload, status_code=200)

    monkeypatch.setattr("requests.get", fake_get_large)
    assert get_user_data(large_id) == large_payload

    # 3. API returns a 200 but with missing fields  the function should still
    #    return whatever the API gave us.
    incomplete_payload = {"id": 5, "name": "Partial"}  # email missing

    def fake_get_incomplete(url, params=None, **kwargs):
        return _make_mock_response(incomplete_payload, status_code=200)

    monkeypatch.setattr("requests.get", fake_get_incomplete)
    assert get_user_data(5) == incomplete_payload


def test_get_user_data_error_cases(monkeypatch):
    """
    Error cases  verify that the function raises appropriate exceptions for
    invalid input or unexpected HTTP status codes.
    """
    # 1. Noninteger user_id should raise a ``ValueError`` (or ``TypeError`` depending on implementation).
    with pytest.raises(ValueError):
        get_user_data("not-an-int")

    # 2. Negative user_id  treat as invalid.
    with pytest.raises(ValueError):
        get_user_data(-10)

    # 3. API returns a non200 status code (e.g., 404).  The function is expected
    #    to raise an exception (here we assume ``RuntimeError``; adjust if the
    #    implementation uses a different type).
    def fake_get_404(url, params=None, **kwargs):
        return _make_mock_response({"detail": "Not found"}, status_code=404)

    monkeypatch.setattr("requests.get", fake_get_404)

    with pytest.raises(RuntimeError):
        get_user_data(123)