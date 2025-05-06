"""Test the is_really_unary attribute on tree nodes."""

import unittest

from tt.trees import ExpressionTreeNode


class TestTreeNodeIsReallyUnary(unittest.TestCase):

    def test_single_operand(self):
        """Test unary detection of single operand."""
        for token in ('0', '1', 'token'):
            t = ExpressionTreeNode.build_tree([token])
            self.assertTrue(t.is_really_unary)

    def test_chained_unary_operators_ending_in_operand(self):
        """Test unary operators chained ending in an operand."""
        t = ExpressionTreeNode.build_tree(['A', '~'])
        self.assertTrue(t.is_really_unary)

        t = ExpressionTreeNode.build_tree(['A', '~', '~'])
        self.assertTrue(t.is_really_unary)

        t = ExpressionTreeNode.build_tree(['A', '~', '~', '~'])
        self.assertTrue(t.is_really_unary)

    def test_chained_unary_operators_with_binary_operator(self):
        """Test a chain of unary operators containing a binary operator."""
        t = ExpressionTreeNode.build_tree(['A', 'B', 'and', 'not'])
        self.assertFalse(t.is_really_unary)

        t = ExpressionTreeNode.build_tree(
            ['A', 'B', 'or',
             'C', 'D', 'E', 'not', 'and', 'and', 'not',
             'xor'])
        self.assertFalse(t.is_really_unary)
        self.assertFalse(t.l_child.is_really_unary)
        self.assertFalse(t.r_child.is_really_unary)
        self.assertTrue(t.r_child.l_child.r_child.l_child.is_really_unary)

    def test_binary_operator(self):
        """Test an tree containing a binary operator."""
        t = ExpressionTreeNode.build_tree(['A', 'B', 'or'])
        self.assertFalse(t.is_really_unary)
