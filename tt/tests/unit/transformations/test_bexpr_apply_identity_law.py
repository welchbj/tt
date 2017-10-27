"""Tests for the apply_identity_law transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import apply_identity_law


class TestApplyIdentityLaw(unittest.TestCase):

    def assert_apply_identity_law_transformation(self, original, expected):
        """Helper for asserting correct apply_identity_law_transformation."""
        self.assertEqual(expected, str(apply_identity_law(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as an argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            apply_identity_law(None)

    def test_from_boolean_expression_object(self):
        """Test passing an expression object as an argument."""
        self.assert_apply_identity_law_transformation(
            BooleanExpression('A and 1'),
            'A')

    def test_no_effect_expected(self):
        """Test passing expressions where no transformation should occur."""
        no_effect_expected_exprs = [
            'A and B',
            'A -> B',
            '1 xor B',
            'A -> B -> C -> D',
            'A',
            '~A',
            '~~A']
        for expr in no_effect_expected_exprs:
            self.assert_apply_identity_law_transformation(expr, expr)

    def test_simple_binary_cases(self):
        """Test simple binary expressions."""
        self.assert_apply_identity_law_transformation(
            'A and 0', '0')
        self.assert_apply_identity_law_transformation(
            '0 and A', '0')
        self.assert_apply_identity_law_transformation(
            'A and 1', 'A')
        self.assert_apply_identity_law_transformation(
            '1 and A', 'A')
        self.assert_apply_identity_law_transformation(
            'A or 0', 'A')
        self.assert_apply_identity_law_transformation(
            '0 or A', 'A')
        self.assert_apply_identity_law_transformation(
            'A or 1', '1')
        self.assert_apply_identity_law_transformation(
            '1 or A', '1')

    def test_only_constant_binary_expressions(self):
        """Test binary expressions of only constant operands."""
        self.assert_apply_identity_law_transformation(
            '0 or 1', '1')
        self.assert_apply_identity_law_transformation(
            '0 and 1', '0')
        self.assert_apply_identity_law_transformation(
            '1 or 0', '1')
        self.assert_apply_identity_law_transformation(
            '1 and 0', '0')

    def test_bubbling_up_constants(self):
        """Test constants that bubble up from sub-expressions."""
        self.assert_apply_identity_law_transformation(
            '(A and 1) or (0 and B)',
            'A')
        self.assert_apply_identity_law_transformation(
            'A and ((B or 0) and (1 and C) and (D and 0))',
            '0')
        self.assert_apply_identity_law_transformation(
            '(A and B and C) and (0 or (D or 1))',
            'A and B and C')
        self.assert_apply_identity_law_transformation(
            '(A and B and C and D and E and 1) and (F and G and 1)',
            'A and B and C and D and E and F and G')
        self.assert_apply_identity_law_transformation(
            '(A and 0 and B) or (0 and 1) or (1)',
            '1')
