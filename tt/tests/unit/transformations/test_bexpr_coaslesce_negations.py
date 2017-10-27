"""Tests for the coalesce_negations transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import coalesce_negations


class TestCoalesceNegations(unittest.TestCase):

    def assert_coalesce_negations_transformation(self, original, expected):
        """Helper for asserting correct coalesce_negations transformation."""
        self.assertEqual(expected, str(coalesce_negations(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as an argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            coalesce_negations(float('inf'))

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_coalesce_negations_transformation(
            BooleanExpression('~~A'),
            'A')

    def test_only_constant_expressions(self):
        """Test the transformation on negated expression objects."""
        self.assert_coalesce_negations_transformation(
            '1', '1')
        self.assert_coalesce_negations_transformation(
            '0', '0')
        self.assert_coalesce_negations_transformation(
            '~0', '1')
        self.assert_coalesce_negations_transformation(
            '~1', '0')
        self.assert_coalesce_negations_transformation(
            '~~1', '1')
        self.assert_coalesce_negations_transformation(
            '~~0', '0')
        self.assert_coalesce_negations_transformation(
            '!!!1', '0')
        self.assert_coalesce_negations_transformation(
            'not not not not not 0', '1')
        self.assert_coalesce_negations_transformation(
            '~1 and ~0', '0 and 1')
        self.assert_coalesce_negations_transformation(
            '~~~1 -> 0', '0 -> 0')
        self.assert_coalesce_negations_transformation(
            '~~~0 -> ~~0 -> ~0 -> 0', '1 -> 0 -> 1 -> 0')

    def test_negated_single_operand(self):
        """Test condensing negations on single operand expressions."""
        self.assert_coalesce_negations_transformation(
            'A',
            'A')

        self.assert_coalesce_negations_transformation(
            '~A',
            '~A')

        self.assert_coalesce_negations_transformation(
            '~~A',
            'A')

        self.assert_coalesce_negations_transformation(
            '~~~A',
            '~A')

        self.assert_coalesce_negations_transformation(
            '~~~~A',
            'A')

        self.assert_coalesce_negations_transformation(
            '~~~~~A',
            '~A')

    def test_negated_expression(self):
        """Test condensing negations on expressions."""
        self.assert_coalesce_negations_transformation(
            '~(A or B)',
            '~(A or B)')

        self.assert_coalesce_negations_transformation(
            '~~(A && B)',
            'A && B')

        # ensure that the closest negation to the expression is preserved
        self.assert_coalesce_negations_transformation(
            '~~ not(A -> B)',
            'not (A -> B)')

        self.assert_coalesce_negations_transformation(
            '~ not ~ not !!(A iff B)',
            'A iff B')

    def test_compound_expression(self):
        """Test negations scattered throughout a compouned expression."""
        self.assert_coalesce_negations_transformation(
            '! not not (~~(~A xor ~~~~~B) <-> (~~A nand !!!C))',
            'not ((~A xor ~B) <-> (A nand !C))')
