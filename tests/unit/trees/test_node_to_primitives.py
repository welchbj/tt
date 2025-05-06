"""Test node transformation to primitive operators."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeToPrimitives(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test that no change occurs for single operand."""
        root = self.get_tree_root_from_expr_str('A')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertEqual(
            str(prim),
            'A')

    def test_only_unary_operators(self):
        """Test no change occurs for expression of only unary NOTs."""
        root = self.get_tree_root_from_expr_str('~A')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertEqual(
            str(prim),
            '\n'.join((
                '~',
                '`----A')))

        root = self.get_tree_root_from_expr_str('~~A')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child is not root.l_child)
        self.assertTrue(prim.l_child.l_child is not root.l_child.l_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                '~',
                '`----~',
                '     `----A')))

    def test_simple_and(self):
        """Test that no semantic change occurs for a simple AND expression."""
        root = self.get_tree_root_from_expr_str('A and B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'and',
                '`----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('A && B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                '/\\',
                '`----A',
                '`----B')))

    def test_simple_impl(self):
        """Test transformation from IMPLIES operator to OR form."""
        root = self.get_tree_root_from_expr_str('A impl B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'or',
                '`----not',
                '|    `----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('A -> B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                '\\/',
                '`----~',
                '|    `----A',
                '`----B')))

    def test_simple_nand(self):
        """Test transformation of a simple NAND expression."""
        root = self.get_tree_root_from_expr_str('A nand B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'or',
                '`----not',
                '|    `----A',
                '`----not',
                '     `----B')))

    def test_simple_nor(self):
        """Test transformation of a simple NOR expression."""
        root = self.get_tree_root_from_expr_str('A nor B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'and',
                '`----not',
                '|    `----A',
                '`----not',
                '     `----B')))

    def test_simple_or(self):
        """Test that no semantic change occurs for a simple OR expression."""
        root = self.get_tree_root_from_expr_str('A or B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'or',
                '`----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('A || B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child is not root.l_child)
        self.assertTrue(prim.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                '\\/',
                '`----A',
                '`----B')))

    def test_simple_xor(self):
        """Test transformation of a simple XOR expresson."""
        root = self.get_tree_root_from_expr_str('A xor B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.r_child is not root.r_child)
        self.assertTrue(prim.l_child.r_child.l_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----not',
                '|         `----B',
                '`----and',
                '     `----not',
                '     |    `----A',
                '     `----B')))

    def test_simple_xnor(self):
        """Test transformation of a single XNOR expression."""
        root = self.get_tree_root_from_expr_str('A xnor B')
        prim = root.to_primitives()
        self.assertTrue(prim is not root)
        self.assertTrue(prim.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.r_child is not root.r_child)
        self.assertTrue(prim.r_child.l_child.l_child is not root.l_child)
        self.assertTrue(prim.r_child.l_child.r_child is not root.r_child)
        self.assertEqual(
            str(prim),
            '\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----B',
                '`----and',
                '     `----not',
                '     |    `----A',
                '     `----not',
                '          `----B')))
