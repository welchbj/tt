"""Tests for iterating over expression clauses.

Since BooleanExpressions's iter_clauses variations are basically wrappers
around the functions of the same name from ExpressionTreeNode, they are not
tested in-depth here. Instead, take a look at the unit tests for
ExpressionTreeNode's implementation.

"""

import unittest

from tt.expressions import BooleanExpression


class TestExpressionIterClauses(unittest.TestCase):

    def test_simple_iter_clauses(self):
        """Test basic expression iter_clauses functionality."""
        # ensure defaults to CNF
        b = BooleanExpression('A or B or C or D')
        self.assertTrue(b.is_cnf)
        self.assertTrue(b.is_dnf)

        clauses = b.iter_clauses()
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "A or B or C or D">')
        with self.assertRaises(StopIteration):
            next(clauses)

        # ensure falls back to DNF
        b = BooleanExpression('(A and B and C) or (D and E and F)')
        self.assertFalse(b.is_cnf)
        self.assertTrue(b.is_dnf)

        clauses = b.iter_clauses()
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "A and B and C">')
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "D and E and F">')
        with self.assertRaises(StopIteration):
            next(clauses)

    def test_simple_iter_cnf(self):
        """Test basic expression iter_cnf_clauses functionality."""
        b = BooleanExpression('(A or B) and (C or D) and (E or F)')
        self.assertTrue(b.is_cnf)
        self.assertFalse(b.is_dnf)

        clauses = b.iter_cnf_clauses()
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "A or B">')
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "C or D">')
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "E or F">')
        with self.assertRaises(StopIteration):
            next(clauses)

    def test_simple_iter_dnf(self):
        """Test basic expression iter_dnf_clauses functionality."""
        b = BooleanExpression('(A and B) or (C and D) or (E and F)')
        self.assertTrue(b.is_dnf)
        self.assertFalse(b.is_cnf)

        clauses = b.iter_dnf_clauses()
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "A and B">')
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "C and D">')
        self.assertEqual(
            repr(next(clauses)),
            '<BooleanExpression "E and F">')
        with self.assertRaises(StopIteration):
            next(clauses)
