"""Tests for the apply_inverse_law transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import apply_inverse_law


class TestApplyInverseLaw(unittest.TestCase):

    def assert_apply_inverse_law_transformation(self, original, expected):
        """Helper for asserting correct apply_inverse_law transformation."""
        self.assertEqual(expected, str(apply_inverse_law(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as an argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            apply_inverse_law(float('inf'))

    def test_from_boolean_expression_object(self):
        """Test passing an expression object as an object."""
        self.assert_apply_inverse_law_transformation(
            BooleanExpression('A or ~A'),
            '1')

    def test_no_effect_expected(self):
        """Test passing expressions where no transformation is expected."""
        exprs = [
            'A -> B -> 0',
            'A xor B',
            'A and ~~A and ~~~~A and ~~~~~~A',
            'A nand B nand C nand ~A',
            'A',
            'A or ~~A',
            '~~~~~~~B',
            'B or B']
        for expr in exprs:
            self.assert_apply_inverse_law_transformation(expr, expr)

    def test_simple_binary_cases(self):
        """Test simple binary cases where expect a transformation."""
        self.assert_apply_inverse_law_transformation(
            'A and ~A', '0')

        self.assert_apply_inverse_law_transformation(
            '~A and A', '0')

        self.assert_apply_inverse_law_transformation(
            'B or not B', '1')

        self.assert_apply_inverse_law_transformation(
            '!B or B', '1')

    def test_complex_expressions(self):
        """Test expressions with nested cnf, dnf and non-normal clauses."""
        self.assert_apply_inverse_law_transformation(
            '(A or B or C or D or ~~A or ~A) -> (A and B and C and ~~B)',
            '1 -> (A and B and C and ~~B)')

        self.assert_apply_inverse_law_transformation(
            'A xor B -> (~A and A)',
            'A xor (B -> 0)')

        self.assert_apply_inverse_law_transformation(
            '(A and B and C and ~C) or (D or ~~~D)',
            '0 or 1')
