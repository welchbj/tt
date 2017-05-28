"""Test node transformation to condense negations."""

from tt.definitions import BINARY_OPERATORS

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeToPrimitives(ExpressionTreeAndNodeTestCase):

    def test_non_negated_operand(self):
        """Test that no change occurs for a non-negated operand."""
        root = self.get_tree_root_from_expr_str('A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced is not root)
        self.assertEqual(
            str(coalesced),
            'A')

    def test_no_change_to_binary_operators(self):
        """Test that no change occurs for any binary operators."""
        for op in BINARY_OPERATORS:
            expr_str = 'A {} B'.format(op.default_plain_english_str)
            root = self.get_tree_root_from_expr_str(expr_str)
            coalesced = root.coalesce_negations()
            self.assertTrue(coalesced is not root)
            self.assertTrue(coalesced.l_child is not root.l_child)
            self.assertTrue(coalesced.r_child is not root.r_child)
            self.assertEqual(
                str(coalesced),
                '\n'.join((
                    op.default_plain_english_str,
                    '`----A',
                    '`----B')))

    def test_single_negation(self):
        """Test that no change occurs for a single negation."""
        root = self.get_tree_root_from_expr_str('~A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced is not root)
        self.assertTrue(coalesced.l_child is not root.l_child)
        self.assertEqual(
            str(coalesced),
            '\n'.join((
                '~',
                '`----A')))

    def test_multiple_negations(self):
        """Test the coalescing of mutliple consecutive negations."""
        root = self.get_tree_root_from_expr_str('~~A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced is not root.l_child.l_child)
        self.assertEqual(str(coalesced), 'A')

        root = self.get_tree_root_from_expr_str('~~~A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced.l_child is not root.l_child.l_child.l_child)
        self.assertEqual(
            str(coalesced),
            '\n'.join((
                '~',
                '`----A')))

        root = self.get_tree_root_from_expr_str('~~~~A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced is not root.l_child.l_child.l_child.l_child)
        self.assertEqual(str(coalesced), 'A')

        root = self.get_tree_root_from_expr_str('~~~~~A')
        coalesced = root.coalesce_negations()
        self.assertTrue(coalesced.l_child is not
                        root.l_child.l_child.l_child.l_child.l_child)
        self.assertEqual(
            str(coalesced),
            '\n'.join((
                '~',
                '`----A')))
