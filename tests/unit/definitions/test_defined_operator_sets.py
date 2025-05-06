"""Tests for the pre-defined sets of operators."""

import unittest

from tt.definitions import (
    BINARY_OPERATORS,
    NON_PRIMITIVE_OPERATORS,
    TT_AND_OP,
    TT_IMPL_OP,
    TT_NAND_OP,
    TT_NOR_OP,
    TT_OR_OP,
    TT_XNOR_OP,
    TT_XOR_OP)


class TestDefinedOperatorSets(unittest.TestCase):

    def test_binary_operators_is_proper_size(self):
        """Ensure the set is of the expected size."""
        self.assertEqual(7, len(BINARY_OPERATORS))

    def test_binary_operators_contains_expected_operators(self):
        """Ensure the set contains all operators."""
        self.assertTrue(TT_AND_OP in BINARY_OPERATORS)
        self.assertTrue(TT_IMPL_OP in BINARY_OPERATORS)
        self.assertTrue(TT_NAND_OP in BINARY_OPERATORS)
        self.assertTrue(TT_NOR_OP in BINARY_OPERATORS)
        self.assertTrue(TT_OR_OP in BINARY_OPERATORS)
        self.assertTrue(TT_XNOR_OP in BINARY_OPERATORS)
        self.assertTrue(TT_XOR_OP in BINARY_OPERATORS)

    def test_non_primitive_operators_is_proper_size(self):
        """Ensure the set is of the expected size."""
        self.assertEqual(5, len(NON_PRIMITIVE_OPERATORS))

    def test_non_primitive_operators_contains_expected_operators(self):
        """Ensure the set contains all operators."""
        self.assertTrue(TT_IMPL_OP in NON_PRIMITIVE_OPERATORS)
        self.assertTrue(TT_NAND_OP in NON_PRIMITIVE_OPERATORS)
        self.assertTrue(TT_NOR_OP in NON_PRIMITIVE_OPERATORS)
        self.assertTrue(TT_XNOR_OP in NON_PRIMITIVE_OPERATORS)
        self.assertTrue(TT_XOR_OP in NON_PRIMITIVE_OPERATORS)
