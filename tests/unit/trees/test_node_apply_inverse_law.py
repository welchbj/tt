"""Test applying the Inverse Law to tree nodes."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeApplyInverseLaw(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test expressions of single operands."""
        for symbol in ('A', 'an_operand_name', '0', '1'):
            root = self.get_tree_root_from_expr_str(symbol)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(transformed),
                symbol)

    def test_non_primitive_binary_operators(self):
        """Test binary operators where we expect no transformation."""
        exprs = [
            'A -> A',
            'A xor B',
            'C <-> D',
            'A xnor B',
            'C nor D']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_simple_AND_no_transformation(self):
        """Test expressions with binary AND with no transformation."""
        exprs = [
            'A and A',
            'A and B',
            'A and ~B',
            '~A and B',
            '~A and ~A',
            '~~A and ~~A',
            '~~~A and ~~~A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_simple_AND_transformation_expected(self):
        """Test expressions with binary AND with a transformation."""
        exprs = [
            'A and ~A',
            '~A and A',
            '~~A and ~A',
            '~A and ~~A',
            '~~~A and A',
            'A and ~~~A',
            '~A and ~~~~A',
            '~~~~A and ~A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(str(transformed), '0')

    def test_simple_OR_no_transformation(self):
        """Test expressions with binary OR with no transformation."""
        exprs = [
            'A or A',
            'A or B',
            'A or ~B',
            '~A or B',
            '~A and ~A',
            '~~B and ~~B',
            '~~~C and ~~~C']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(root is not transformed)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_simple_OR_transformation_expected(self):
        """Test expressions with binary OR with transformations."""
        exprs = [
            'A or ~A',
            '~A or A',
            '~~A or ~A',
            '~A or ~~A',
            '~~~A or ~~A',
            '~~A or ~~~A',
            'A or ~~~A',
            '~~~A or A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(str(transformed), '1')

    def test_single_clause_AND_expression(self):
        """Test a single clause ANDed expression of >2 operands."""
        exprs = [
            'A and B and C and ~A',
            '~A and A and A and ~~A',
            'A and B and C and D and ~~~D and E and ~~E',
            '~~~A and ~~A and ~A and A',
            '~A and ~B and ~C and ~D and B']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(str(transformed), '0')

    def test_single_clause_OR_expression(self):
        """Test a single clause ORed expression >2 operands."""
        exprs = [
            'A or B or C or D or ~B',
            'op1 or op2 or not op1',
            '~~~A or ~~~~~A or ~A or ~~A',
            '!A or !B or C or !D or !C or E']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_inverse_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(str(transformed), '1')

    def test_cnf_expressions(self):
        """Test cnf expressions."""
        root = self.get_tree_root_from_expr_str(
            '(A or B or ~A) and (A or ~B or ~~~B or ~~B)')
        transformed = root.apply_inverse_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(transformed.is_cnf)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----1',
                '`----1')))

        root = self.get_tree_root_from_expr_str(
            '(A or B or C or ~C) and (C or D or ~~~~~~~D) and (A or B or ~A)')
        transformed = root.apply_inverse_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(transformed.is_cnf)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'and',
                '`----1',
                '`----and',
                '     `----1',
                '     `----1')))

    def test_dnf_expressions(self):
        """Test dnf expressions."""
        root = self.get_tree_root_from_expr_str(
            '(A and ~B and ~A) or (B and C and ~~C and ~~~~C and ~~~C)')
        transformed = root.apply_inverse_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(transformed.is_dnf)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----0',
                '`----0')))

        root = self.get_tree_root_from_expr_str(
            '(A and A and A and ~A) or (A and B and ~B) or (C and ~C)')
        transformed = root.apply_inverse_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(transformed.is_dnf)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----0',
                '`----or',
                '     `----0',
                '     `----0')))

    def test_compound_expression(self):
        """Test an expression of mixed cnf, dnf, and non-normal clauses."""
        root = self.get_tree_root_from_expr_str(
            '(A xor B) or (A and ~A and B) or (~C or ~~~C or ~~C or D)')
        transformed = root.apply_inverse_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                'or',
                '`----xor',
                '|    `----A',
                '|    `----B',
                '`----or',
                '     `----0',
                '     `----1')))
