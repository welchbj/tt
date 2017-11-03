"""Test for the apply_idempotent_law transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import apply_idempotent_law


class TestApplyIdempotentLaw(unittest.TestCase):

    def assert_apply_idempotent_law_transformation(self, original, expected):
        """Helper for asserting correct apply_idempotent_law transformation."""
        self.assertEqual(expected, str(apply_idempotent_law(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as an argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            apply_idempotent_law(True)

    def test_from_boolean_expression_object(self):
        """Test passing an expression object as argument."""
        self.assert_apply_idempotent_law_transformation(
            BooleanExpression('A and A'),
            'A')

    def test_no_effect_expected(self):
        """Test passing expressions where no transformation should occur."""
        no_effected_expected_exprs = [
            'A and ~A',
            '~A and A',
            '~~~A and A',
            'A and ~~~A',
            'A -> B',
            'A -> A',
            '~A or A',
            'A or ~A']
        for expr in no_effected_expected_exprs:
            self.assert_apply_idempotent_law_transformation(expr, expr)

    def test_simple_binary_cases(self):
        """Test simple binary expressions where a transformation occurs."""
        exprs_simplifying_to_A = [
            'A {} A',
            '~~A {} ~~A',
            '~~~~A {} ~~~~A',
            '~~A {} ~~~~A',
            '~~~~A {} ~~A']
        for expr in exprs_simplifying_to_A:
            for op in ('and', 'or',):
                expr = expr.format(op)
                self.assert_apply_idempotent_law_transformation(expr, 'A')

        exprs_simplifying_to_not_A = [
            '~A {} ~A',
            '~~~A {} ~~~A',
            '~A {} ~~~A',
            '~~~A {} ~A']
        for expr in exprs_simplifying_to_not_A:
            for op in ('and', 'or',):
                expr = expr.format(op)
                self.assert_apply_idempotent_law_transformation(expr, '~A')

    def test_expressions_with_constants(self):
        """Test binary expressions of only constant operands."""
        self.assert_apply_idempotent_law_transformation(
            '0 or 0', '0')
        self.assert_apply_idempotent_law_transformation(
            '0 and 0', '0')
        self.assert_apply_idempotent_law_transformation(
            '1 or 1', '1')
        self.assert_apply_idempotent_law_transformation(
            '1 and 1', '1')
        self.assert_apply_idempotent_law_transformation(
            '1 or ~0', '1')
        self.assert_apply_idempotent_law_transformation(
            '~0 or 1', '1')
        self.assert_apply_idempotent_law_transformation(
            '0  or ~1', '0')
        self.assert_apply_idempotent_law_transformation(
            '~1 or 0', '0')
        self.assert_apply_idempotent_law_transformation(
            '1 and ~0', '1')
        self.assert_apply_idempotent_law_transformation(
            '~0 and 1', '1')
        self.assert_apply_idempotent_law_transformation(
            '0 and ~1', '0')
        self.assert_apply_idempotent_law_transformation(
            '~1 and 0', '0')
        self.assert_apply_idempotent_law_transformation(
            '0 and A and B and C and 0',
            '0 and A and B and C')
        self.assert_apply_idempotent_law_transformation(
            'A and 1 and 1 and B and 0 and C and 0 and D',
            'A and 1 and B and 0 and C and D')
        self.assert_apply_idempotent_law_transformation(
            '(1 or 1) and (1 or 1)',
            '1 and 1')
        self.assert_apply_idempotent_law_transformation(
            'A or B or 1 or ~0',
            'A or B or 1')

    def test_cnf_clauses(self):
        """Test expressions where we prune operands from cnf clauses."""
        self.assert_apply_idempotent_law_transformation(
            '(A or B or C or C or C or C or B or B or A) and (A or B)',
            '(A or B or C) and (A or B)')
        self.assert_apply_idempotent_law_transformation(
            '(A or A) and (B or B) and (C or C)',
            'A and B and C')
        self.assert_apply_idempotent_law_transformation(
            '(A or ~A or ~B or B or C or C) and (D or D or E)',
            '(A or ~A or ~B or B or C) and (D or E)')

    def test_dnf_clauses(self):
        """Test expressions where we prune operands from dnf clauses."""
        self.assert_apply_idempotent_law_transformation(
            '(A and B and C and A and B and C) or (A and A and A and A)',
            '(A and B and C) or A')
        self.assert_apply_idempotent_law_transformation(
            '(A and B and A and B and A and B) or (A and A and A and B and C)',
            '(A and B) or (A and B and C)')
        self.assert_apply_idempotent_law_transformation(
            '(A and ~A and ~~A) or (~~~B and ~~B and ~B and B)',
            '(A and ~A) or (~B and B)')

    def test_multi_clause_expressions(self):
        """Test expressions of mixed cnf, dnf, and non-normal clauses."""
        self.assert_apply_idempotent_law_transformation(
            '(A xor B) and (C or D or C or D) -> (A and B and B and B and C)',
            '(A xor B) and ((C or D) -> (A and B and C))')
