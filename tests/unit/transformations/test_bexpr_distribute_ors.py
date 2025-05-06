"""Tests for the distribute_ors transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import distribute_ors


class TestDistributeOrs(unittest.TestCase):

    def assert_distribute_ors_tranformation(self, original, expected):
        """Helper for asserting correct distribute_ands transformation."""
        self.assertEqual(expected, str(distribute_ors(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as the argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            distribute_ors([])

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_distribute_ors_tranformation(
            BooleanExpression('A and B'),
            'A and B')

    def test_distributing_single_operand_from_left(self):
        """Test distributing a single operand from the left."""
        self.assert_distribute_ors_tranformation(
            'A or (B and C and D and E and F)',
            '(A or B) and (A or C) and (A or D) and (A or E) and (A or F)')

    def test_distributing_single_operand_from_right(self):
        """Test distributing a single operand from the right."""
        self.assert_distribute_ors_tranformation(
            '(A and B and C) or D',
            '(A or D) and (B or D) and (C or D)')

    def test_distributing_sub_expr_over_single_operands_from_left(self):
        """Test distributing a sub-expr from left over single-operands."""
        self.assert_distribute_ors_tranformation(
            '(B or C) or (E and F and G)',
            '(B or C or E) and (B or C or F) and (B or C or G)')

    def test_distributing_sub_expr_over_single_operands_from_right(self):
        """Test distributing a sub-expr from right over single-operands."""
        self.assert_distribute_ors_tranformation(
            '(A and B and C and D) or (E or F)',
            '(A or E or F) and (B or E or F) and (C or E or F) and '
            '(D or E or F)')

    def test_distributing_sub_expr_over_sub_exprs_from_left(self):
        """Test distributing a sub-expr from left over other sub-exprs."""
        self.assert_distribute_ors_tranformation(
            '(A -> B) or (A and B and C)',
            '((A -> B) or A) and ((A -> B) or B) and ((A -> B) or C)')

    def test_distributing_sub_expr_over_sub_exprs_from_right(self):
        """Test distributing a sub-expr from right over other sub-exprs."""
        self.assert_distribute_ors_tranformation(
            '(A and (B xor C) and D) or (E xor F)',
            '(A or (E xor F)) and ((B xor C) or (E xor F)) and '
            '(D or (E xor F))')

    def test_distribruting_single_operand_over_sub_exprs_from_left(self):
        """Test distributing a single-operand over sub-exprs from the left."""
        self.assert_distribute_ors_tranformation(
            'A or (B and (C -> D) and (E or F or G))',
            '(A or B) and (A or (C -> D)) and (A or E or F or G)')

    def test_distribruting_single_operand_over_sub_exprs_from_right(self):
        """Test distributing a single-operand over sub-exprs from the right."""
        self.assert_distribute_ors_tranformation(
            '(A and (B or C or D) and (E or F) and G) or I',
            '(A or I) and (B or C or D or I) and (E or F or I) and (G or I)')

    def test_distribute_sub_exprs_over_sub_exprs_from_left(self):
        """Test distributing sub-exprs over other sub-exprs from the left."""
        self.assert_distribute_ors_tranformation(
            '(A or B) or ((C or (D and E)) and F and (G or H or I))',
            '(A or B or C or D) and (A or B or C or E) and (A or B or F) and '
            '(A or B or G or H or I)')

    def test_distribute_sub_exprs_over_sub_exprs_from_right(self):
        """Test distributing sub-exprs over other sub-exprs from the right."""
        self.assert_distribute_ors_tranformation(
            '(A and B and (C or D) and E) or F',
            '(A or F) and (B or F) and (C or D or F) and (E or F)')
