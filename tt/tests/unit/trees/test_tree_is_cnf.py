"""Tests for CNF detection in expression trees."""

import unittest

from tt.trees import BooleanExpressionTree


class TestExpressionTreeIsCnf(unittest.TestCase):

    def assert_is_cnf(self, postfix_tokens):
        """Assert the passed tokens are in conjunctive normal form."""
        self.assertTrue(BooleanExpressionTree(postfix_tokens).is_cnf)

    def assert_not_cnf(self, postfix_tokens):
        """Assert the passed tokens are not in conjunctive normal form."""
        self.assertFalse(BooleanExpressionTree(postfix_tokens).is_cnf)

    def test_is_cnf_single_operand(self):
        """Test CNF determination for single operand trees."""
        for postfix_tokens in (['0'], ['1'], ['token']):
            self.assert_is_cnf(postfix_tokens)

    def test_is_cnf_only_unary_operators(self):
        """Test CNF determination for trees with only unary operators."""
        self.assert_is_cnf(['A', 'not'])
        self.assert_not_cnf(['A', 'not', 'not'])
        self.assert_not_cnf(['A', 'not', 'not', 'not'])

    def test_is_cnf_single_clause(self):
        """Test that a single clause of ORed operands is in CNF form."""
        self.assert_is_cnf(['op1', 'op2', 'or'])
        self.assert_is_cnf(['A', 'B', 'C', 'D', 'or', 'or', 'or'])
        self.assert_is_cnf(['A', '~', 'B', 'C', '~', 'or', 'or'])

    def test_is_cnf_clauses_of_single_operands(self):
        """Test several ANDed clauses of single operands is in CNF form."""
        self.assert_is_cnf(['op1', 'op2', 'and'])
        self.assert_is_cnf(['A', 'B', 'C', 'D', 'and', 'and', 'and'])
        self.assert_is_cnf(['A', 'B', 'not', 'C', 'and', 'and'])

    def test_is_cnf_contains_non_primitive_operator_in_clause(self):
        """Test cases where non-primitive operator is in a clause."""
        self.assert_not_cnf(['A', 'B', 'or',
                             'C', 'D', 'or',
                             'D', 'E', 'nand',
                             'and', 'and'])
        self.assert_not_cnf(['A', 'B', 'C', 'xor', 'or',
                             'A', 'B', 'or',
                             'and'])

    def test_is_cnf_contains_non_primitive_operator_joining_clauses(self):
        """Test cases where non-primitive operator joins clauses."""
        self.assert_not_cnf(['A', 'B', '<->'])
        self.assert_not_cnf(['A', 'B', 'or',
                             'B', 'C', 'or',
                             'C', 'E', 'or',
                             '->', 'and'])

    def test_is_cnf_contains_notted_clause(self):
        """Test cases where an entire clause is notted."""
        self.assert_not_cnf(['A', 'B', 'or', 'not',
                             'C', 'D', 'or',
                             'and'])

    def test_is_cnf_multiple_clauses(self):
        """Test CNF determination for multiple clauses."""
        self.assert_is_cnf(['A', 'C', 'or',
                            'B', 'C', 'or',
                            'E', 'F', 'G', 'or', 'or',
                            'and', 'and'])

    def test_is_cnf_for_dnf_expression(self):
        """Test CNF determination for an expression in DNF."""
        self.assert_not_cnf(['A', 'B', 'C', 'and', 'and',
                             'B', 'C', 'not', 'and',
                             'D', 'E', 'and',
                             'or', 'or'])
