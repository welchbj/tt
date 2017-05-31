"""Tests for the distribute_ands transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import distribute_ands


class TestDistributeAnds(unittest.TestCase):

    def assert_distribute_ands_tranformation(self, original, expected):
        """Helper for asserting correct distribute_ands transformation."""
        self.assertEqual(expected, str(distribute_ands(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as the argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            distribute_ands(None)

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_distribute_ands_tranformation(
            BooleanExpression('A and B'),
            'A and B')

    def test_distributing_single_operand_over_single_operand_clauses(self):
        """Test distributing a single operand over a larger clause."""
        self.assert_distribute_ands_tranformation(
            'A and (B or C or D or E or F)',
            '(A and B) or (A and C) or (A and D) or (A and E) or (A and F)')

    def test_distributing_sub_expr_over_single_operand_clauses(self):
        """Test distributing a sub-expression over single-operand clauses."""
        self.assert_distribute_ands_tranformation(
            '(B and C) and (D or E or F or G)',
            '(B and C and D) or (B and C and E) or (B and C and F) or '
            '(B and C and G)')

    def test_distribruting_single_operand_over_sub_exprs(self):
        """Test distributing a single operand clause over sub expressions."""
        self.assert_distribute_ands_tranformation(
            'A and ((B xor C) or D or (E and F))',
            '(A and (B xor C)) or (A and D) or (A and E and F)')

    def test_distribute_sub_exprs_over_sub_exprs(self):
        """Test distributing sub-expressions over other sub-expressions."""
        self.assert_distribute_ands_tranformation(
            '(A and B and C) and ((D xor E) or (F and G and H) or (I impl J))',
            '((A and B and C) and (D xor E)) or '
            '(A and B and C and F and G and H) or '
            '((A and B and C) and (I impl J))')
