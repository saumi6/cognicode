"""
Auto-generated test cases for function: info
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:00:30
Source file: logger.py
Function signature: def info(self, message: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.logger import Logger

import pytest
from logger import Logger  # the file that contains the Logger class


# ----------------------------------------------------------------------
# Helper: a deterministic timestamp used for all normal / edge tests
# ----------------------------------------------------------------------
FIXED_TS = "2023-01-01 12:00:00"


def _patch_timestamp(monkeypatch):
    """
    Replace the global ``get_current_timestamp`` used inside ``Logger.info``
    with a stub that always returns ``FIXED_TS``.
    """
    # NOTE: the absolute import path must match the real module name.
    # Here we assume the class lives in a file called ``logger.py``.
    monkeypatch.setattr("logger.get_current_timestamp", lambda: FIXED_TS)


# ----------------------------------------------------------------------
# 1. Normal cases  parametrised
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "logger_name, message, expected",
    [
        ("App", "started", f"[INFO] {FIXED_TS} [App]: started"),
        ("Service", "processing request", f"[INFO] {FIXED_TS} [Service]: processing request"),
        ("DB", "connection ok", f"[INFO] {FIXED_TS} [DB]: connection ok"),
    ],
)
def test_info_normal_cases(monkeypatch, capsys, logger_name, message, expected):
    """
    Verify that ``Logger.info`` prints the correctly formatted string for
    typical inputs.
    """
    _patch_timestamp(monkeypatch)

    logger = Logger(logger_name)
    logger.info(message)

    captured = capsys.readouterr()
    # ``print`` adds a trailing newline  strip it for a clean comparison
    assert captured.out.strip() == expected


# ----------------------------------------------------------------------
# 2. Edge cases  empty / long / specialcharacter messages and names
# ----------------------------------------------------------------------
def test_info_edge_cases(monkeypatch, capsys):
    """
    Test boundary conditions such as an empty message, a very long message,
    special characters and an empty logger name.
    """
    _patch_timestamp(monkeypatch)

    # a) empty message
    logger = Logger("Edge")
    logger.info("")
    out = capsys.readouterr().out.strip()
    assert out == f"[INFO] {FIXED_TS} [Edge]: "

    # b) very long message
    long_msg = "x" * 10_000  # 10k characters
    logger.info(long_msg)
    out = capsys.readouterr().out.strip()
    assert out == f"[INFO] {FIXED_TS} [Edge]: {long_msg}"

    # c) special characters (unicode, newlines, tabs)
    special_msg = "\n\t"
    logger.info(special_msg)
    out = capsys.readouterr().out.strip()
    # ``print`` will keep the newline inside the string, so we compare the raw output
    assert out == f"[INFO] {FIXED_TS} [Edge]: {special_msg}"

    # d) empty logger name
    nameless_logger = Logger("")
    nameless_logger.info("no name")
    out = capsys.readouterr().out.strip()
    assert out == f"[INFO] {FIXED_TS} []: no name"


# ----------------------------------------------------------------------
# 3. Error cases  situations that should raise an exception
# ----------------------------------------------------------------------
def test_info_error_cases(monkeypatch):
    """
    Force an internal failure (e.g., ``get_current_timestamp`` is not callable)
    and ensure that ``Logger.info`` propagates the exception.
    """
    # Replace the timestamp function with a noncallable object
    monkeypatch.setattr("logger.get_current_timestamp", None)

    logger = Logger("Broken")

    with pytest.raises(TypeError):
        # ``None`` is not callable, so the attempt to execute it inside ``info``
        # must raise a ``TypeError``.
        logger.info("this will fail")