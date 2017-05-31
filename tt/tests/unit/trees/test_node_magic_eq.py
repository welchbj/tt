"""Tests for tree node __eq__ (and __ne__) comparison."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeMagicEq(ExpressionTreeAndNodeTestCase):

    def assert_equal_trees(self, one, two):
        """Assert the trees rooted at two nodes (from strs) are equal."""
        self.assertEqual(
            self.get_tree_root_from_expr_str(one),
            self.get_tree_root_from_expr_str(two))

    def assert_not_equal_trees(self, one, two):
        """Assert the trees rooted at two nodes (from strs) are not equal."""
        self.assertNotEqual(
            self.get_tree_root_from_expr_str(one),
            self.get_tree_root_from_expr_str(two))

    def test_single_operand(self):
        """Test equality for trees of a single operand."""
        self.assert_equal_trees('A', 'A')

        self.assert_not_equal_trees('A', 'B')

    def test_only_unary_operators(self):
        """Test equality for trees composed only of unary operators."""
        self.assert_equal_trees('~~A', '~~A')
        self.assert_equal_trees('~~A', '!!A')
        self.assert_equal_trees('~(A)', '~A')

        self.assert_not_equal_trees('~A', '~B')
        self.assert_not_equal_trees('~~A', '~A')

    def test_simple_binary_operator_expressions(self):
        """Test equality for simple expressions with binary operators."""
        self.assert_equal_trees('A and B', 'A and B')
        self.assert_equal_trees('A and B', r'A /\ B')
        self.assert_equal_trees('A and B', '((A) and (B))')

        self.assert_not_equal_trees('A -> B', 'A -> C')
        self.assert_not_equal_trees('A -> B', 'C -> B')

    def test_negated_binary_operator_expressions(self):
        """Test equality of negated binary expressions."""
        self.assert_equal_trees('~(A nand B)', '~(A nand B)')
        self.assert_equal_trees('~(A nand B)', '!(A nand B)')
        self.assert_equal_trees('~(A iff B)', '~(A <-> B)')
        self.assert_equal_trees('!!(A xor B)', '!!(A xor B)')
        self.assert_equal_trees('!~~(A impl B)', 'not not ~(A impl B)')

        self.assert_not_equal_trees('~(A nand B)', '~(A nor B)')
        self.assert_not_equal_trees('~~(A nand B)', '~~(A nor B)')
        self.assert_not_equal_trees('~~~(A nand B)', '~~~(A nor B)')
        self.assert_not_equal_trees('~~(A xor B)', '~(A xor B)')
        self.assert_not_equal_trees('~(A or B)', '~(B or C)')

    def test_chained_operator_expressions(self):
        """Test equality of chained operators."""
        self.assert_equal_trees(
            'A or B or C or D',
            'A or B or C or D')
        self.assert_equal_trees(
            '(A or B or C) xor (D or E) xor (F and G and H and I)',
            '(A or B or C) xor (D or E) xor (F and G and H and I)')
        self.assert_equal_trees(
            '~(A or B or C) and (D iff E)',
            '~(A or B or C) and (D iff E)')

        self.assert_not_equal_trees(
            '(A or B or C) and D and (E or F)',
            '(A or B or C) and D and E')
        self.assert_not_equal_trees(
            'A and (B nand C nand D)',
            'A and (B nand ~C nand D)')

    def test_nested_binary_operator_expressions(self):
        """Test equality for expressions containing many levels."""
        self.assert_equal_trees(
            '(A and B) or (C and D)',
            '(A and B) or (C and D)')
        self.assert_equal_trees(
            '(A and B) or (C and D)',
            '(A and B) || (C & D)')
        self.assert_equal_trees(
            '((A -> B) and (C or D or E)) <-> A <-> (B nand C nand D)',
            '((A -> B) and (C or D or E)) <-> A <-> (B nand C nand D)')
        self.assert_equal_trees(
            '((A -> B) and (C or D or E)) <-> ~~A <-> (B nand C nand D)',
            '((A impl B) and (C or D or E)) iff not ~A iff (B nand C nand D)')

        self.assert_not_equal_trees(
            '(A and B) or (C and D)',
            '(A and B) or (D and C)')
        self.assert_not_equal_trees(
            '(A and B) or (C and D)',
            '(B and A) or (C and D)')
        self.assert_not_equal_trees(
            '((A -> B) and (D or C or E)) <-> A <-> (B nand C nand D)',
            '((A -> B) and (C or E)) <-> A <-> (B nand C nand D)')
