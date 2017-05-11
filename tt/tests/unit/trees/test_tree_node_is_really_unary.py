"""Test the is_really_unary attribute on tree nodes."""

import unittest

from tt.trees import BooleanExpressionTree as bet


class TestTreeNodeIsReallyUnary(unittest.TestCase):

    def test_single_operand(self):
        """Test unary detection of single operand."""
        for token in ('0', '1', 'token'):
            t = bet([token])
            self.assertTrue(t.root.is_really_unary)

    def test_chained_unary_operators_ending_in_operand(self):
        """Test unary operators chained ending in an operand."""
        t = bet(['A', '~'])
        self.assertTrue(t.root.is_really_unary)

        t = bet(['A', '~', '~'])
        self.assertTrue(t.root.is_really_unary)

        t = bet(['A', '~', '~', '~'])
        self.assertTrue(t.root.is_really_unary)

    def test_chained_unary_operators_with_binary_operator(self):
        """Test a chain of unary operators containing a binary operator."""
        t = bet(['A', 'B', 'and', 'not'])
        self.assertFalse(t.root.is_really_unary)

        t = bet(['A', 'B', 'or',
                 'C', 'D', 'E', 'not', 'and', 'and', 'not',
                 'xor'])
        self.assertFalse(t.root.is_really_unary)
        self.assertFalse(t.root.l_child.is_really_unary)
        self.assertFalse(t.root.r_child.is_really_unary)
        self.assertTrue(t.root.r_child.l_child.r_child.l_child.is_really_unary)

    def test_binary_operator(self):
        """Test an tree containing a binary operator."""
        t = bet(['A', 'B', 'or'])
        self.assertFalse(t.root.is_really_unary)
