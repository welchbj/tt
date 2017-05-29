"""Test node transformation to apply De Morgan's Law."""

from tt.definitions import (
    BINARY_OPERATORS,
    TT_AND_OP,
    TT_OR_OP)

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeApplyDeMorgans(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test that no change occurs for a single operand."""
        root = self.get_tree_root_from_expr_str('A')
        demo = root.apply_de_morgans()
        self.assertTrue(demo is not root)
        self.assertEqual(
            str(demo),
            'A')

    def test_unaffected_binary_operators(self):
        """Test that no change occurs for non-AND and non-OR binary ops."""
        for op in (BINARY_OPERATORS - {TT_AND_OP, TT_OR_OP}):
            expr_str = 'A {} B'.format(op.default_plain_english_str)
            root = self.get_tree_root_from_expr_str(expr_str)
            demo = root.apply_de_morgans()
            self.assertTrue(demo is not root)
            self.assertTrue(demo.l_child is not root.l_child)
            self.assertTrue(demo.r_child is not root.r_child)
            self.assertEqual(
                str(demo),
                '\n'.join((
                    op.default_plain_english_str,
                    '`----A',
                    '`----B')))

    def test_simple_and(self):
        """Test transformation of AND following De Morgan's Law."""
        root = self.get_tree_root_from_expr_str('not (A and B)')
        demo = root.apply_de_morgans()
        self.assertTrue(demo is not root)
        self.assertTrue(demo.l_child.l_child is not root.l_child.l_child)
        self.assertTrue(demo.r_child.l_child is not root.l_child.r_child)
        self.assertEqual(
            str(demo),
            '\n'.join((
                'or',
                '`----not',
                '|    `----A',
                '`----not',
                '     `----B')))

        root = self.get_tree_root_from_expr_str('~(A & B)')
        demo = root.apply_de_morgans()
        self.assertTrue(demo is not root)
        self.assertTrue(demo.l_child.l_child is not root.l_child.l_child)
        self.assertTrue(demo.r_child.l_child is not root.l_child.r_child)
        self.assertEqual(
            str(demo),
            '\n'.join((
                '|',
                '`----~',
                '|    `----A',
                '`----~',
                '     `----B')))

    def test_simple_or(self):
        """Test transformation of OR following De Morgan's Law."""
        root = self.get_tree_root_from_expr_str('not (A or B)')
        demo = root.apply_de_morgans()
        self.assertTrue(demo is not root)
        self.assertTrue(demo.l_child.l_child is not root.l_child.l_child)
        self.assertTrue(demo.r_child.l_child is not root.l_child.r_child)
        self.assertEqual(
            str(demo),
            '\n'.join((
                'and',
                '`----not',
                '|    `----A',
                '`----not',
                '     `----B')))

        root = self.get_tree_root_from_expr_str('~(A || B)')
        demo = root.apply_de_morgans()
        self.assertTrue(demo is not root)
        self.assertTrue(demo.l_child.l_child is not root.l_child.l_child)
        self.assertTrue(demo.r_child.l_child is not root.l_child.r_child)
        self.assertEqual(
            str(demo),
            '\n'.join((
                '&',
                '`----~',
                '|    `----A',
                '`----~',
                '     `----B')))
