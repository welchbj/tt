"""Tests for valid identifiers."""

import unittest

from ....definitions import is_valid_identifier


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

    def test_valid_identifiers(self):
        """Test a few valid identifiers."""
        self.assertTrue(is_valid_identifier('_____var'))
        self.assertTrue(is_valid_identifier('var_20'))
        self.assertTrue(is_valid_identifier('variable'))
