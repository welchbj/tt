"""Utilities for the tt command-line interface."""

from __future__ import print_function

import sys


def print_info(*args, **kwargs):
    """A thin wrapper around ``print``."""
    print(*args, **kwargs)


def print_err(*args, **kwargs):
    """A thin wrapper around ``print`` to print to stderr."""
    print(*args, file=sys.stderr, **kwargs)
