"""
Auto-generated test cases for function: get_logger
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:09:46
Source file: logger.py
Function signature: def get_logger(name: str) -> Logger
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.logger import get_logger

import logging
import pytest

# The function under test lives in ``test_repo/logger.py`` (module name ``test_repo.logger``)
from test_repo.logger import get_logger


@pytest.mark.parametrize(
    "logger_name, expected_name",
    [
        ("app", "app"),
        ("my_module.submodule", "my_module.submodule"),
        ("service-logger", "service-logger"),
    ],
)
def test_get_logger_normal_cases(monkeypatch, logger_name, expected_name):
    """
    Normal usage  the function should return a ``logging.Logger`` whose ``name``
    attribute matches the supplied ``logger_name``.  The test also verifies that
    the underlying ``logging.getLogger`` function is called exactly once with the
    correct argument by monkeypatching it.
    """
    called = {}

    def fake_get_logger(name):
        # Record that we were called and with which name
        called["name"] = name
        # Return a real Logger instance so the rest of the code works unchanged
        return logging.Logger(name)

    # Patch the stdlib ``logging.getLogger`` used inside ``get_logger``
    monkeypatch.setattr("logging.getLogger", fake_get_logger)

    result = get_logger(logger_name)

    # ``get_logger`` must have delegated to ``logging.getLogger`` with the same name
    assert called.get("name") == logger_name, "logging.getLogger was not called with the expected name"

    # The returned object must be a Logger and its ``name`` attribute must match
    assert isinstance(result, logging.Logger)
    assert result.name == expected_name
        

def test_get_logger_edge_cases(monkeypatch):
    """
    Edgecase handling  test empty strings, very long names and names containing
    unusual characters (including Unicode).  The function should still return a
    ``logging.Logger`` instance whose ``name`` attribute reflects the input.
    """
    edge_names = [
        "",                                 # empty string
        "a" * 1024,                         # very long name
        "spaced name",                      # spaces are allowed in logger names
        "unicode---",                    # Unicode characters
    ]

    # Use a simple stub that returns a real Logger so we can inspect the name
    def fake_get_logger(name):
        return logging.Logger(name)

    monkeypatch.setattr("logging.getLogger", fake_get_logger)

    for name in edge_names:
        logger = get_logger(name)
        assert isinstance(logger, logging.Logger)
        # ``logging.Logger`` stores the name exactly as passed
        assert logger.name == name


def test_get_logger_error_cases():
    """
    (or ``ValueError``) when the supplied ``name`` is not a string.  Each
    nonstring value is exercised individually.
    """
    invalid_inputs = [
        None,
        123,
        45.6,
        ["list", "of", "strings"],
        {"key": "value"},
    ]

    for bad_input in invalid_inputs:
        with pytest.raises((TypeError, ValueError)):
            get_logger(bad_input)  # type: ignore[arg-type]  # intentional bad type