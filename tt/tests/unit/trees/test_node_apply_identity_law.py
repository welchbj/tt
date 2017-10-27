"""Test applying the Identity Law to tree nodes."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeApplyIdentityLaw(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test expressions of single operands."""
        for symbol in ('A', 'operand', '0', '1'):
            root = self.get_tree_root_from_expr_str(symbol)
            transformed = root.apply_identity_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(transformed),
                symbol)

    def test_simple_cases_equivalent_to_0(self):
        """Test simple binary expressions that transform to 0."""
        exprs_equivalent_to_0 = [
            '1 and 0',
            '0 and 1',
            '0 and 0',
            '1 and 1 and 1 and 0',
            '1 and 1 and 0 and 1 and 1',
            'A and 0',
            '0 and B',
            '~A and 0',
            '0 and (A xor B)',
            '(A -> B) and 0']
        for expr in exprs_equivalent_to_0:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_identity_law()
            self.assertTrue(root is not transformed)
            self.assertEqual(
                str(transformed),
                '0')

    def test_simple_cases_equivalent_to_1(self):
        """Test simple binary expressions that transform to 1."""
        exprs_equivalent_to_1 = [
            '0 or 1',
            '1 or 0',
            '1 or 1',
            '0 or 0 or 0 or 1',
            '0 or 1 or 0 or 0',
            'B or 1',
            '1 or B',
            '~~~~~~B or 1',
            '1 or (A and B and C)',
            '(A xor B) or 1']
        for expr in exprs_equivalent_to_1:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_identity_law()
            self.assertTrue(root is not transformed)
            self.assertEqual(
                str(transformed),
                '1')

    def test_simple_cases_and_identity(self):
        """Test expressions ANDed with 1, pruning the 1 sub-expression."""
        root = self.get_tree_root_from_expr_str('(A -> B) and 1')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                '->',
                '`----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('1 and (A nand B)')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'nand',
                '`----A',
                '`----B')))

    def test_simple_cases_or_identity(self):
        """Test expressions ORed with 0, pruning the 0 sub-expression."""
        root = self.get_tree_root_from_expr_str('operand or 0')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            'operand')

        root = self.get_tree_root_from_expr_str('0 or (A and B)')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----A',
                '`----B')))

    def test_chained_operators_equivalent_to_1(self):
        """Test chained AND and OR expressions yielding 1."""
        exprs_equivalent_to_1 = [
            '(1 or A or B or C)',
            'A or B or C or D or E or 1',
            'A or 1 or B or 1 or C or 1 or D',
            '(A or 1 or B or C) and (A or B or C or D or 1)']
        for expr in exprs_equivalent_to_1:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_identity_law()
            self.assertTrue(root is not transformed)
            self.assertEqual(str(transformed), '1')

    def test_chained_operators_equivalent_to_0(self):
        """Test chained AND and OR expressions yielding 0."""
        exprs_equivalent_to_0 = [
            '0 and A and B and C',
            'A and B and 0',
            'A and B and 0 and C and D and E',
            '(A and B and 0 and C) or (A and 0 and B and C and D and E)']
        for expr in exprs_equivalent_to_0:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_identity_law()
            self.assertTrue(root is not transformed)
            self.assertEqual(str(transformed), '0')

    def test_chained_operators_pruning_1(self):
        """Test chained AND operators, ensuring 1 literals are pruned."""
        root = self.get_tree_root_from_expr_str('1 and A and B and C')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----A',
                '`----and',
                '     `----B',
                '     `----C')))

        root = self.get_tree_root_from_expr_str('A and B and C and 1')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----A',
                '`----and',
                '     `----B',
                '     `----C')))

        root = self.get_tree_root_from_expr_str('(A and 1 and B) or (1 and C)')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----B',
                '`----C')))

    def test_chained_operators_pruning_0(self):
        """Test chained OR operators, ensuring 0 literals are pruned."""
        root = self.get_tree_root_from_expr_str('0 or A or B')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('A or B or 0')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----A',
                '`----B')))

        root = self.get_tree_root_from_expr_str('(A or 0 or B) and (C or 0)')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----or',
                '|    `----A',
                '|    `----B',
                '`----C')))

    def test_bubbling_up(self):
        """Test constants that bubble up the tree."""
        root = self.get_tree_root_from_expr_str('(1 and (B or 1)) xor A')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'xor',
                '`----1',
                '`----A')))

        root = self.get_tree_root_from_expr_str(
            '(B -> (C and 0)) and (1 or (A -> B -> C))')
        transformed = root.apply_identity_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                '->',
                '`----B',
                '`----0')))

    def test_unaffected_expression(self):
        """Test expressions that should not be affected."""
        root = self.get_tree_root_from_expr_str('A and B and C')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----A',
                '`----and',
                '     `----B',
                '     `----C')))

        root = self.get_tree_root_from_expr_str('0 xor 1')
        transformed = root.apply_identity_law()
        self.assertTrue(root is not transformed)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'xor',
                '`----0',
                '`----1')))
