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

    def test_distributing_single_operand_over_single_operand_clauses(self):
        """Test distributing a single operand over a larger clause."""
        self.assert_distribute_ors_tranformation(
            'A or (B and C and D and E and F)',
            '(A or B) and (A or C) and (A or D) and (A or E) and (A or F)')

    def test_distributing_sub_expr_over_single_operand_clauses(self):
        """Test distributing a sub-expression over single-operand clauses."""
        self.assert_distribute_ors_tranformation(
            '(B or C) or (E and F and G)',
            '(B or C or E) and (B or C or F) and (B or C or G)')

    def test_distribruting_single_operand_over_sub_exprs(self):
        """Test distributing a single operand clause over sub expressions."""
        self.assert_distribute_ors_tranformation(
            'A or (B and (C -> D) and (E or F or G))',
            '(A or B) and (A or (C -> D)) and (A or E or F or G)')

    def test_distribute_sub_exprs_over_sub_exprs(self):
        """Test distributing sub-expressions over other sub-expressions."""
        self.assert_distribute_ors_tranformation(
            '(A or B) or ((C or (D and E)) and F and (G or H or I))',
            '((A or B) or ((C or D) and (C or E))) and '
            '(A or B or F) and (A or B or G or H or I)')
