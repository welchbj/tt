"""Tests for ``non_negated_symbol_set`` and ``negated_symbol_set`` attrs."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeSymbolSets(ExpressionTreeAndNodeTestCase):

    def assert_symbol_sets(self, tree_root, expected_non_negated_symbol_str,
                           expected_negated_symbol_str):
        self.assertEqual(
            expected_non_negated_symbol_str,
            tree_root.non_negated_symbol_set)
        self.assertEqual(
            expected_negated_symbol_str,
            tree_root.negated_symbol_set)

    def test_single_operand(self):
        """Test single operand variations."""
        root = self.get_tree_root_from_expr_str('A')
        self.assert_symbol_sets(root, {'A'}, set())

        root = self.get_tree_root_from_expr_str('!A')
        self.assert_symbol_sets(root, set(), {'A'})

        root = self.get_tree_root_from_expr_str('~~A')
        self.assert_symbol_sets(root, {'A'}, set())

        root = self.get_tree_root_from_expr_str('~~~~~A')
        self.assert_symbol_sets(root, set(), {'A'})

    def test_multiple_operands(self):
        """Test expressions with multiple operands."""
        root = self.get_tree_root_from_expr_str('~A or B or C or D')
        self.assert_symbol_sets(root, {'B', 'C', 'D'}, {'A'})

        root = self.get_tree_root_from_expr_str('A or B or C')
        self.assert_symbol_sets(root, {'A', 'B', 'C'}, set())

        root = self.get_tree_root_from_expr_str('~A -> ~~~B -> ~~~~~C')
        self.assert_symbol_sets(root, set(), {'A', 'B', 'C'})

    def test_operand_in_both_sets(self):
        """Test operands that are in both the non-negated and negated sets."""
        root = self.get_tree_root_from_expr_str('~A -> A')
        self.assert_symbol_sets(root, {'A'}, {'A'})

        root = self.get_tree_root_from_expr_str('~~A nand B nand A nand ~~~B')
        self.assert_symbol_sets(root, {'A', 'B'}, {'B'})

        root = self.get_tree_root_from_expr_str('(A xor B xor C) -> ~A')
        self.assert_symbol_sets(root, {'A', 'B', 'C'}, {'A'})

        root = self.get_tree_root_from_expr_str(
            '(A or B) and (~A or C or ~B) and ~C')
        self.assert_symbol_sets(root, {'A', 'B', 'C'}, {'A', 'B', 'C'})

    def test_negated_binary_operators(self):
        """Test expressions with negated binary operators."""
        root = self.get_tree_root_from_expr_str('~(A or B)')
        self.assert_symbol_sets(root, {'A', 'B'}, set())

        root = self.get_tree_root_from_expr_str('not A -> ~~~(B nand C)')
        self.assert_symbol_sets(root, {'B', 'C'}, {'A'})

        root = self.get_tree_root_from_expr_str('not (A or ~B) <-> (~A -> C)')
        self.assert_symbol_sets(root, {'A', 'C'}, {'A', 'B'})

    def test_deeply_nest_negated_operands(self):
        """Test expressions where negated operands are nested in negations."""
        root = self.get_tree_root_from_expr_str(
            '~(A and ~((B xor C) -> (~~D or ~E)) and ~~~(~B xor C))')
        self.assert_symbol_sets(root, {'A', 'B', 'C', 'D'}, {'B', 'E'})
