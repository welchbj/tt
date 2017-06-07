"""Tests for expression sat_one functionality."""

from tt.errors import NoEvaluationVariationError
from tt.expressions import BooleanExpression as be

from ._helpers import ExpressionTestCase


class TestExpressionSatOne(ExpressionTestCase):

    def test_only_constants_exprs_cause_exception(self):
        """Test that expressions of only constants cause exceptions."""
        with self.assertRaises(NoEvaluationVariationError):
            be('0').sat_one()

        with self.assertRaises(NoEvaluationVariationError):
            be('1').sat_one()

        with self.assertRaises(NoEvaluationVariationError):
            be('(0 or (1 xor 0)) nand 0').sat_one()

    def test_single_operand_expr(self):
        """Test satisfying a single-operand expr."""
        b = be('A')
        res = b.sat_one()
        self.assertEqual('A=1', str(res))

    def test_cnf_expr(self):
        """Test satisfying an expr already in CNF."""
        b = be('(A or B or C) and (D or E) or F or (G or H or I)')
        with b.constrain(A=0, B=0, D=0, H=0, I=0):
            res = b.sat_one()
            self.assertEqual(
                'A=0, B=0, C=1, D=0, E=1, F=1, G=1, H=0, I=0', str(res))

    def test_dnf_expr(self):
        """Test satisfying an expr in DNF."""
        b = be('(A and B) or (C and D and E and F) or G')
        with b.constrain(A=1, B=0, C=0, D=0, E=0, F=0):
            res = b.sat_one()
            self.assertEqual(
                'A=1, B=0, C=0, D=0, E=0, F=0, G=1', str(res))

    def test_expr_with_some_constant_only_clauses(self):
        """Test satisfying an expr with some clauses of only constants."""
        b = be(r'A <-> (1 \/ (1 /\ 0)) <-> 1')
        res = b.sat_one()
        self.assertEqual('A=1', str(res))

    def test_naturally_unsat_without_constants(self):
        """Test an expr with no constants that cannot be satisfied."""
        b = be('A and ~A')
        self.assertIsNone(b.sat_one())

        b = be('A and (B xnor ~B)')
        self.assertIsNone(b.sat_one())

    def test_naturally_unsat_with_constants(self):
        """Test an expr with constants that cannot be satisfied."""
        b = be('A and 0')
        self.assertIsNone(b.sat_one())

    def test_constraint_causes_unsat(self):
        """Test adding a constraint that makes the expr unsatisfiable."""
        with be('(A and B) xor C').constrain(A=0, C=0) as b:
            self.assertIsNone(b.sat_one())

    def test_constrain_all_symbols_in_expr_causes_sat(self):
        """Test constraining all of the symbols, causing satisfiability."""
        with be('A xor (B and C)').constrain(A=0, B=1, C=1) as b:
            res = b.sat_one()
            self.assertEqual('A=0, B=1, C=1', str(res))

    def test_constrain_all_symbols_in_expr_causes_unsat(self):
        """Test constraining all of the symbols, causing unsatisfiability."""
        with be('(A or B) and (C or D)').constrain(A=0, B=0, C=0, D=0) as b:
            self.assertIsNone(b.sat_one())

    def test_nested_constrain_context_managers(self):
        """Test multiple constraints imposed with nested context managers."""
        b = be('A xor (B iff (C and D))')
        with b.constrain(A=0, D=1):
            with b.constrain(C=1):
                res = b.sat_one()
                self.assertEqual('A=0, B=1, C=1, D=1', str(res))
