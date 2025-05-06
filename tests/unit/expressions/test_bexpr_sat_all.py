"""Tests for expression sat_all functionality."""

from tt.errors import NoEvaluationVariationError
from tt.expressions import BooleanExpression as be

from ._helpers import ExpressionTestCase


class TestExpressionSatAll(ExpressionTestCase):

    def test_only_constants_exprs_cause_exception(self):
        """Test that expressions of only constants cause exceptions."""
        with self.assertRaises(NoEvaluationVariationError):
            for solution in be('0').sat_all():
                pass

        with self.assertRaises(NoEvaluationVariationError):
            for solution in be('1').sat_all():
                pass

        with self.assertRaises(NoEvaluationVariationError):
            for solution in be('0 and (1 xor 0) and (1 -> 0 -> 1)').sat_all():
                pass

    def test_single_operand_expr(self):
        """Test a single-operand expression."""
        b = be('A')
        res = list(b.sat_all())
        self.assertEqual(1, len(res))
        self.assertEqual('A=1', str(res[0]))

    def test_expr_with_some_constant_only_clauses(self):
        """Test an expression with some clauses of only constants."""
        b = be('(A xor B) and (0 or 1) and ((1))')
        res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(2, len(res))
        self.assertIn('A=1, B=0', res)
        self.assertIn('A=0, B=1', res)

    def test_naturally_unsat_expr(self):
        """Test an expression that results in no solutions."""
        b = be('(A and ~A) and (B or C)')
        res = list(b.sat_all())
        self.assertEqual(0, len(res))

    def test_sat_expr_with_one_solution(self):
        """Test an expression that has only one solution."""
        b = be('A and B and ~C and D')
        res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(1, len(res))
        self.assertIn('A=1, B=1, C=0, D=1', res)

    def test_sat_expr_with_multiple_solutions(self):
        """Test an expression that has many solutions."""
        b = be('A and (B xor C) and D')
        res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(2, len(res))
        self.assertIn('A=1, B=1, C=0, D=1', res)
        self.assertIn('A=1, B=0, C=1, D=1', res)

    def test_constraints_eliminate_all_solutions(self):
        """Test constraints that eliminate all possible solutions."""
        b = be('(A xor B) and C')
        with b.constrain(A=True, B=True):
            res = list(b.sat_all())
        self.assertEqual(0, len(res))

    def test_constraints_eliminate_some_solutions(self):
        """Test constraints that only eliminate some solutions."""
        b = be('A xor B xor C xor D')
        with b.constrain(A=False, B=False):
            res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(2, len(res))
        self.assertIn('A=0, B=0, C=1, D=0', res)
        self.assertIn('A=0, B=0, C=0, D=1', res)

    def test_constraints_eliminate_no_solutions(self):
        """Test constraints that do not eliminate any possible solutions."""
        b = be('(A xor 0) and (B or C or D)')
        with b.constrain(A=1):
            res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(7, len(res))
        self.assertIn('A=1, B=0, C=0, D=1', res)
        self.assertIn('A=1, B=0, C=1, D=0', res)
        self.assertIn('A=1, B=0, C=1, D=1', res)
        self.assertIn('A=1, B=1, C=0, D=0', res)
        self.assertIn('A=1, B=1, C=0, D=1', res)
        self.assertIn('A=1, B=1, C=1, D=0', res)
        self.assertIn('A=1, B=1, C=1, D=1', res)

    def test_all_symbols_constrained_yields_sat_solution(self):
        """Test constraining all symbols, resulting in a valid solution."""
        b = be('(A <-> B) and (C or D)')
        with b.constrain(A=1, B=1, C=1, D=0):
            res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(1, len(res))
        self.assertIn('A=1, B=1, C=1, D=0', res)

    def test_all_symbols_constrained_yields_no_solutions(self):
        """Test constraining all symbols, resulting in no valid solutions."""
        with be('A or B or C or D').constrain(A=0, B=0, C=0, D=0) as b:
            res = list(str(sol) for sol in b.sat_all())
        self.assertEqual(0, len(res))
