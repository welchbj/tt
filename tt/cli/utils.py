"""Utilities for the tt command-line interface."""

import sys

from typing import Any


def print_info(*args: Any, **kwargs: Any) -> None:
    """A thin wrapper around ``print``."""
    print(*args, **kwargs)


def print_err(*args: Any, **kwargs: Any) -> None:
    """A thin wrapper around ``print`` to print to stderr."""
    print(*args, file=sys.stderr, **kwargs)
