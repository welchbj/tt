"""Basic tests for expression __eq__ and __ne__."""

import unittest

from tt.expressions import BooleanExpression


class TestExpressionMagicEquals(unittest.TestCase):

    def assert_equal_expressions(self, one, two):
        """Assert two expressions (from strings) are equivalent."""
        self.assertEqual(
            BooleanExpression(one),
            BooleanExpression(two))

    def assert_not_equal_expressions(self, one, two):
        """Assert two expressions (from strings) are equivalent."""
        self.assertNotEqual(
            BooleanExpression(one),
            BooleanExpression(two))

    def test_non_bexpr_not_equal(self):
        """Test that a non-BooleanExpression object is not equal."""
        self.assertNotEqual(BooleanExpression('A'), 5)

    def test_single_operand_expressions(self):
        """Test equality for single operand expressions."""
        self.assert_equal_expressions('A', 'A')
        self.assert_equal_expressions('0', '0')
        self.assert_equal_expressions('1', '1')

        self.assert_not_equal_expressions('A', 'B')
        self.assert_not_equal_expressions('A', '0')
        self.assert_not_equal_expressions('A', '1')
        self.assert_not_equal_expressions('1', 'A')
        self.assert_not_equal_expressions('0', 'A')

    def test_only_unary_operator_expressions(self):
        """Test equality for expressions of only unary expressions."""
        self.assert_equal_expressions('~A', '~A')
        self.assert_equal_expressions('~A', 'not A')
        self.assert_equal_expressions('~~~A', '~~~A')

        self.assert_not_equal_expressions('~A', 'A')
        self.assert_not_equal_expressions('not not not A', 'not not A')

    def test_simple_binary_operator_expressions(self):
        """Test equality for simple expressions of binary operators."""
        self.assert_equal_expressions('A and B', 'A and B')
        self.assert_equal_expressions('A impl B', 'A -> B')
        self.assert_equal_expressions('~A or ~B', '~A or ~B')

        self.assert_not_equal_expressions('A and B', 'A and A')
        self.assert_not_equal_expressions('A and B', 'A or B')

    def test_chained_binary_operator_expressions(self):
        """Test equality for expressions of chained operators."""
        self.assert_equal_expressions('A or B or C', 'A or B or C')
        self.assert_equal_expressions('A and B and C', 'A & B & C')
        self.assert_equal_expressions('~A xor ~~B xor C', '~A xor ~~B xor C')

        self.assert_not_equal_expressions('A or B or C', 'A or C or B')
        self.assert_not_equal_expressions('A or B or C', 'D or C or B')
        self.assert_not_equal_expressions('A and B and C', 'A and !B and C')

    def test_negated_binary_operator_expressions(self):
        """Test equality for negated binary operator expressions."""
        self.assert_equal_expressions('~(A and B)', '~(A and B)')
        self.assert_equal_expressions('!!(A nand B)', '~~(A nand B)')
        self.assert_equal_expressions('~(A iff B)', 'not (A <-> B)')

        self.assert_not_equal_expressions('~~(A and B)', '~(A and B)')
        self.assert_not_equal_expressions('~(A or B)', '~(A xor B)')

    def test_nested_binary_operator_expressions(self):
        """Test equality for nested binary operator expressions."""
        self.assert_equal_expressions(
            '(A xor (B or C)) nand (D or E or F)',
            '(A xor (B or C)) nand (D or E or F)')
        self.assert_equal_expressions(
            '(A xor (B or C)) nand (D or E or F)',
            '(A xor (B | C)) nand (D \\/ E || F)')

        self.assert_not_equal_expressions(
            '(A xor (B or C)) nand (D or E or F)',
            '(A xor (B or C)) nand (D or G or F)')
        self.assert_not_equal_expressions(
            '(A xor (B or C)) nand (D or E or F)',
            '(B or C) nand (D or G or F)')
