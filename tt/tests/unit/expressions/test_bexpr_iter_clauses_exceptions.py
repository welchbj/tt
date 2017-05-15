"""Tests for exceptions raised when iterating clauses."""

import unittest

from tt.errors import RequiresNormalFormError
from tt.expressions import BooleanExpression


class TestExpressionIterClausesExceptions(unittest.TestCase):

    def test_iter_clauses_not_normal_form(self):
        """Test attempting iter_clauses when not in normal form."""
        b = BooleanExpression('A nand B')
        self.assertFalse(b.is_cnf)
        self.assertFalse(b.is_dnf)

        with self.assertRaises(RequiresNormalFormError):
            for clause in b.iter_clauses():
                pass

    def test_iter_cnf_clauses_not_cnf(self):
        """Test attempting iter_cnf_clauses when not in CNF."""
        b = BooleanExpression('A or !!B')
        self.assertFalse(b.is_cnf)

        with self.assertRaises(RequiresNormalFormError):
            for clause in b.iter_cnf_clauses():
                pass

    def test_iter_dnf_clauses_not_dnf(self):
        """Test attempting iter_dnf_clauses when not in DNF."""
        b = BooleanExpression('(A or B) and (C or D)')
        self.assertFalse(b.is_dnf)

        with self.assertRaises(RequiresNormalFormError):
            for clause in b.iter_dnf_clauses():
                pass
