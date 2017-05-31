"""Tests for the apply_de_morgans transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import apply_de_morgans


class TestApplyDeMorgans(unittest.TestCase):

    def assert_apply_de_morgans_transformation(self, original, expected):
        """Helper for asserting correct apply_de_morgans transformation."""
        self.assertEqual(expected, str(apply_de_morgans(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as an argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            apply_de_morgans(False)

    def test_from_boolean_expression_object(self):
        """Test passing an expression object as an argument."""
        self.assert_apply_de_morgans_transformation(
            BooleanExpression('not (A or B)'),
            'not A and not B')

    def test_no_effect_expected(self):
        """Test scenarios where no change to the expression should occur."""
        self.assert_apply_de_morgans_transformation(
            'A nand B',
            'A nand B')

        self.assert_apply_de_morgans_transformation(
            '~A and B',
            '~A and B')

        self.assert_apply_de_morgans_transformation(
            'A or B',
            'A or B')

    def test_negated_and(self):
        """Test the transformation on a negated AND."""
        self.assert_apply_de_morgans_transformation(
            '~(A and B)',
            r'~A \/ ~B')

        self.assert_apply_de_morgans_transformation(
            '(not (A and B))',
            'not A or not B')

    def test_negated_or(self):
        """Test the transformation on a negated OR."""
        self.assert_apply_de_morgans_transformation(
            '~(A and B)',
            r'~A \/ ~B')

        self.assert_apply_de_morgans_transformation(
            '(not (A and B))',
            'not A or not B')

    def test_compound_expression(self):
        """Test the transformation of compound expressions."""
        self.assert_apply_de_morgans_transformation(
            'not (~(A or B) and ~(C and D))',
            r'not (~A /\ ~B) or not (~C \/ ~D)')

    def test_chained_and(self):
        """Test the transformation on expressions of chained ANDs."""
        self.assert_apply_de_morgans_transformation(
            '~(A & B & C & D & E)',
            '~A \/ ~B \/ ~C \/ ~D \/ ~E')

    def test_chained_or(self):
        """Test the transformation on expressions of chained ORs."""
        self.assert_apply_de_morgans_transformation(
            '~(A || B || C || D || E)',
            '~A /\ ~B /\ ~C /\ ~D /\ ~E')

    def test_multi_level_negated_expressions(self):
        """Test that the transformation works on multiple levels of an expr."""
        self.assert_apply_de_morgans_transformation(
            '~(A and ~(B or ~(C and D) or D))',
            '~A \/ ~(~B /\ ~(~C \/ ~D) /\ ~D)')
