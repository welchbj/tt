"""Tests for CNF detection in expression trees."""

import unittest

from tt.trees import BooleanExpressionTree as bet


class TestExpressionTreeIsCnf(unittest.TestCase):

    def test_is_cnf_single_operand(self):
        """Test cnf determination for single operand trees."""
        for postfix_tokens in (['0'], ['1'], ['token']):
            self.assertTrue(bet(postfix_tokens).is_cnf)

    def test_is_cnf_only_unary_operators(self):
        """Test cnf determination for trees with only unary operators."""
        self.assertTrue(bet(['A', 'not']).is_cnf)
        self.assertFalse(bet(['A', 'not', 'not']).is_cnf)
        self.assertFalse(bet(['A', 'not', 'not', 'not']).is_cnf)

    def test_is_cnf_single_clause(self):
        """Test that a single clause of ORed operands is in cnf form."""
        self.assertTrue(bet(['op1', 'op2', 'or']).is_cnf)
        self.assertTrue(bet(['A', 'B', 'C', 'D', 'or', 'or', 'or']).is_cnf)
        self.assertTrue(bet(['A', '~', 'B', 'C', '~', 'or', 'or']).is_cnf)

    def test_is_cnf_clauses_of_single_operands(self):
        """Test several ANDed clauses of single operands is in cnf form."""
        self.assertTrue(bet(['op1', 'op2', 'and']).is_cnf)
        self.assertTrue(bet(['A', 'B', 'C', 'D', 'and', 'and', 'and']).is_cnf)
        self.assertTrue(bet(['A', 'B', 'not', 'C', 'and', 'and']).is_cnf)

    def test_is_cnf_contains_non_primitive_operator_in_clause(self):
        """Test cases where non-primitive operator is in a clause."""
        self.assertFalse(bet(['A', 'B', 'or',
                              'C', 'D', 'or',
                              'D', 'E', 'nand',
                              'and', 'and']).is_cnf)
        self.assertFalse(bet(['A', 'B', 'C', 'xor', 'or',
                              'A', 'B', 'or',
                              'and']).is_cnf)

    def test_is_cnf_contains_non_primitive_operator_joining_clauses(self):
        """Test cases where non-primitive operator joins clauses."""
        self.assertFalse(bet(['A', 'B', '<->']).is_cnf)
        self.assertFalse(bet(['A', 'B', 'or',
                              'B', 'C', 'or',
                              'C', 'E', 'or',
                              '->', 'and']).is_cnf)

    def test_is_cnf_contains_notted_clause(self):
        """Test cases where an entire clause is notted."""
        self.assertFalse(bet(['A', 'B', 'or', 'not',
                              'C', 'D', 'or',
                              'and']).is_cnf)

    def test_is_cnf_multiple_clauses(self):
        """Test cnf determination for mulitple clauses."""
        self.assertTrue(bet(['A', 'C', 'or',
                             'B', 'C', 'or',
                             'E', 'F', 'G', 'or', 'or',
                             'and', 'and']).is_cnf)
