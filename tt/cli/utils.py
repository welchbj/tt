"""Utilities for the tt command-line interface."""

from __future__ import print_function

import sys


def print_info(*args, **kwargs):
    """A thin wrapper around ``print``, explicitly printing to stdout."""
    print(*args, file=sys.stdout, **kwargs)


def print_err(*args, **kwargs):
    """A thin wrapper around ``print``, explicitly printing to stderr."""
    print(*args, file=sys.stderr, **kwargs)
