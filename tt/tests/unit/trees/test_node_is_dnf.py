"""Tests for DNF detection in tree nodes."""

import unittest

from tt.trees import ExpressionTreeNode


class TestTreeNodeIsDnf(unittest.TestCase):

    def assert_is_dnf(self, postfix_tokens):
        """Assert the passed tokens are in disjunctive normal form."""
        self.assertTrue(ExpressionTreeNode.build_tree(postfix_tokens).is_dnf)

    def assert_not_dnf(self, postfix_tokens):
        """Assert the passed tokens are not in disjunctive normal form."""
        self.assertFalse(ExpressionTreeNode.build_tree(postfix_tokens).is_dnf)

    def test_is_dnf_single_operand(self):
        """Test that a single operand is recognized as in DNF."""
        for postfix_tokens in (['0'], ['1'], ['token']):
            self.assert_is_dnf(postfix_tokens)

    def test_is_dnf_only_unary_operators(self):
        """Test DNF detection for expressions composed of unary operators."""
        self.assert_is_dnf(['A', 'not'])
        self.assert_not_dnf(['A', 'not', 'not'])
        self.assert_not_dnf(['A', 'not', 'not', 'not'])

    def test_is_dnf_single_clause(self):
        """Test that a single clause of ANDed operands is in DNF."""
        self.assert_is_dnf(['op1', 'op2', 'and'])
        self.assert_is_dnf(['A', 'B', 'C', 'D', 'and', 'and', 'and'])
        self.assert_is_dnf(['A', 'B', 'not', 'C', 'and', 'and'])

    def test_is_dnf_clauses_of_single_operands(self):
        """Test several ORed clauses of single operands is in DNF."""
        self.assert_is_dnf(['op1', 'op2', 'or'])
        self.assert_is_dnf(['A', 'B', 'C', 'D', 'or', 'or', 'or'])
        self.assert_is_dnf(['A', '~', 'B', 'C', '~', 'or', 'or'])

    def test_is_dnf_contains_non_primitive_operator_in_clause(self):
        """Test cases where a non-primitive operator is in a clause."""
        self.assert_not_dnf(['A', 'B', 'and',
                             'C', 'D', 'xor',
                             'or'])
        self.assert_not_dnf(['A', 'B', 'C', 'and', 'and',
                             'A', 'not', 'B', 'and',
                             'D', 'E', 'F', 'iff', 'and',
                             'or', 'or'])

    def test_is_dnf_contains_non_primitive_operator_joining_clauses(self):
        """Test cases where a non-primitive operator joins clauses."""
        self.assert_not_dnf(['A', 'B', '->'])
        self.assert_not_dnf(['A', 'B', 'and',
                             'C', 'D', 'and',
                             'xnor'])

    def test_is_dnf_contains_notted_clause(self):
        """Test cases where an entire clause is notted."""
        self.assert_not_dnf(['A', 'B', 'and', 'not'])
        self.assert_not_dnf(['A', 'B', 'and', 'not',
                             'C', 'D', 'and',
                             'or'])

    def test_is_dnf_multiple_clauses(self):
        """Test DNF determination for multiple clauses."""
        self.assert_is_dnf(['A', 'B', 'C', 'and', 'and',
                            'D', 'E', 'F', 'G', 'and', 'and', 'and',
                            'H', 'I', 'and',
                            'or', 'or'])

    def test_is_dnf_for_cnf_expression(self):
        """Test DNF determination for an expression in CNF."""
        self.assert_not_dnf(['A', 'B', 'or',
                             'C', 'D', 'E', 'or', 'or',
                             'F',
                             'and', 'and'])
