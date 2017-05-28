"""Tests for valid identifiers."""

import unittest

from tt.definitions import is_valid_identifier
from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)


class TestIsValidIdentifier(unittest.TestCase):

    def test_keywords(self):
        """Test that some Python keywords not valid identifiers."""
        self.assertFalse(is_valid_identifier('True'))
        self.assertFalse(is_valid_identifier('False'))
        self.assertFalse(is_valid_identifier('is'))
        self.assertFalse(is_valid_identifier('not'))
        self.assertFalse(is_valid_identifier('while'))

    def test_numbers(self):
        """Test invalid identifier with leading number."""
        self.assertFalse(is_valid_identifier('9var'))
        self.assertFalse(is_valid_identifier('10var'))

        self.assertTrue(is_valid_identifier('v9ar'))
        self.assertTrue(is_valid_identifier('var12345'))

    def test_invalid_symbols(self):
        """Test invalid identifier containing bad symbols."""
        self.assertFalse(is_valid_identifier('#'))
        self.assertFalse(is_valid_identifier('!v!a!r!'))
        self.assertFalse(is_valid_identifier('var@'))
        self.assertFalse(is_valid_identifier('v(a)r'))
        self.assertFalse(is_valid_identifier('v``ar'))

    def test_underscores(self):
        """Test identifiers with underscores."""
        self.assertFalse(is_valid_identifier('_var'))
        self.assertFalse(is_valid_identifier('___var'))

        self.assertTrue(is_valid_identifier('va_r'))
        self.assertTrue(is_valid_identifier('var_'))

    def test_valid_identifiers(self):
        """Test a few valid identifiers."""
        self.assertTrue(is_valid_identifier('var11'))
        self.assertTrue(is_valid_identifier('var_20'))
        self.assertTrue(is_valid_identifier('variable'))

    def test_empty_str(self):
        """Test that an empty string raises an error."""
        with self.assertRaises(InvalidArgumentValueError):
            is_valid_identifier('')

    def test_non_str(self):
        """Test that a non-string argument raises an error."""
        with self.assertRaises(InvalidArgumentTypeError):
            is_valid_identifier(None)
