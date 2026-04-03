"""
Auto-generated test cases for function: get_logger
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:10:21
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

# Import the function under test. Adjust the import path if the function lives in a different module.
from logger import get_logger


@pytest.mark.parametrize(
    "logger_name",
    [
        "app",
        "module.submodule",
        "test_logger",
        "my-app",
        "service_123",
    ],
)
def test_get_logger_normal_cases(logger_name):
    """
    Test that ``get_logger`` returns a ``logging.Logger`` instance with the expected name
    for typical, wellformed logger names.
    """
    logger = get_logger(logger_name)

    # The returned object should be a Logger instance.
    assert isinstance(logger, logging.Logger)

    # The logger's name attribute should match the input name.
    assert logger.name == logger_name

    # Recalling ``get_logger`` with the same name should return the same logger object
    # (i.e. the logger is cached by name, as ``logging.getLogger`` does).
    same_logger = get_logger(logger_name)
    assert same_logger is logger


def test_get_logger_edge_cases():
    """
    Test edgecase inputs such as an empty string, a very long name,
    and names containing whitespace or special characters.
    """
    # 1. Empty string  ``logging.getLogger`` returns the root logger.
    empty_logger = get_logger("")
    assert isinstance(empty_logger, logging.Logger)
    # The root logger's name is "root".
    assert empty_logger.name == "root"

    # 2. Very long logger name (e.g., 300 characters).
    long_name = "a" * 300
    long_logger = get_logger(long_name)
    assert isinstance(long_logger, logging.Logger)
    assert long_logger.name == long_name

    # 3. Name with whitespace and special characters.
    special_name = "my logger!@# $%^&*()"
    special_logger = get_logger(special_name)
    assert isinstance(special_logger, logging.Logger)
    assert special_logger.name == special_name


@pytest.mark.parametrize(
    "invalid_input",
    [
        123,                     # integer
        None,                    # NoneType
        ["list", "of", "str"],   # list
        {"key": "value"},        # dict
        3.14,                    # float
        b"bytes_name",           # bytes
    ],
)
def test_get_logger_error_cases(invalid_input):
    """
    Test that ``get_logger`` raises a ``TypeError`` (or ``ValueError``) when the
    provided ``name`` argument is not a string.
    """
    with pytest.raises((TypeError, ValueError)):
        get_logger(invalid_input)