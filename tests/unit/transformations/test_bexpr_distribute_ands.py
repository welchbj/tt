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
            distribute_ands([])

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_distribute_ands_tranformation(
            BooleanExpression('A and B'),
            'A and B')

    def test_distributing_single_operand_from_left(self):
        """Test distributing a single operand from the left."""
        self.assert_distribute_ands_tranformation(
            'A and (B or C or D or E or F)',
            '(A and B) or (A and C) or (A and D) or (A and E) or (A and F)')

    def test_distributing_single_operand_from_right(self):
        """Test distributing a single operand from the right."""
        self.assert_distribute_ands_tranformation(
            '(A or B or C) and D',
            '(A and D) or (B and D) or (C and D)')

    def test_distributing_sub_expr_over_single_operands_from_left(self):
        """Test distributing a sub-expr from left over single-operands."""
        self.assert_distribute_ands_tranformation(
            '(B and C) and (E or F or G)',
            '(B and C and E) or (B and C and F) or (B and C and G)')

    def test_distributing_sub_expr_over_single_operands_from_right(self):
        """Test distributing a sub-expr from right over single-operands."""
        self.assert_distribute_ands_tranformation(
            '(A or B or C or D) and (E and F)',
            '(A and E and F) or (B and E and F) or (C and E and F) or '
            '(D and E and F)')

    def test_distributing_sub_expr_over_sub_exprs_from_left(self):
        """Test distributing a sub-expr from left over other sub-exprs."""
        self.assert_distribute_ands_tranformation(
            '(A iff B) and (A or B or C or D)',
            '((A iff B) and A) or ((A iff B) and B) or ((A iff B) and C) or '
            '((A iff B) and D)')

    def test_distributing_sub_expr_over_sub_exprs_from_right(self):
        """Test distributing a sub-expr from right over other sub-exprs."""
        self.assert_distribute_ands_tranformation(
            '(A or B or (C -> D)) and (E -> F -> G)',
            '(A and (E -> F -> G)) or (B and (E -> F -> G)) or '
            '((C -> D) and (E -> F -> G))')

    def test_distribruting_single_operand_over_sub_exprs_from_left(self):
        """Test distributing a single-operand over sub-exprs from the left."""
        self.assert_distribute_ands_tranformation(
            'A and (B or (C nand D) or (E and F and G))',
            '(A and B) or (A and (C nand D)) or (A and E and F and G)')

    def test_distribruting_single_operand_over_sub_exprs_from_right(self):
        """Test distributing a single-operand over sub-exprs from the right."""
        self.assert_distribute_ands_tranformation(
            '(A or (B and C and D) or (E and F) or G) and I',
            '(A and I) or (B and C and D and I) or (E and F and I) or '
            '(G and I)')

    def test_distribute_sub_exprs_over_sub_exprs_from_left(self):
        """Test distributing sub-exprs over other sub-exprs from the left."""
        self.assert_distribute_ands_tranformation(
            '(A and B and C) and ((C or (D and E)) or F or (G and H and I))',
            '(A and B and C and C) or (A and B and C and D and E) or '
            '(A and B and C and F) or (A and B and C and G and H and I)')

    def test_distribute_sub_exprs_over_sub_exprs_from_right(self):
        """Test distributing sub-exprs over other sub-exprs from the right."""
        self.assert_distribute_ands_tranformation(
            '(A or B or (C and D and E) or (F and G)) and H',
            '(A and H) or (B and H) or (C and D and E and H) or '
            '(F and G and H)')
