"""Test applying the Idempotent Law to tree nodes."""

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeApplyIdempotentLaw(ExpressionTreeAndNodeTestCase):

    def test_single_operand(self):
        """Test expressions of a single operand."""
        for symbol in ('A', 'an_operand_name', '0', '1'):
            root = self.get_tree_root_from_expr_str(symbol)
            transformed = root.apply_idempotent_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(transformed),
                symbol)

    def test_non_primitive_binary_operators(self):
        """Test non AND and OR operators, ensuring no transformation occurs."""
        exprs = [
            'A xor A',
            'A nand A',
            'operand <-> operand',
            '~A -> ~A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_idempotent_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_binary_AND_no_transformation(self):
        """Test binary AND expression where no transformation is applied."""
        exprs = [
            '~A and A',
            'A and ~A',
            'A and B',
            'A and ~B',
            '~A and B',
            '~~A and ~A',
            '~A and ~~A',
            '~~A and ~~~A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_idempotent_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_binary_OR_no_transformation(self):
        """Test binary OR expressions where no transformation is applied."""
        exprs = [
            '~A or A',
            'A or ~A',
            'A or B',
            'A or ~B',
            '~A or B',
            '~~A or ~A',
            '~A or ~~A',
            '~~~A or ~~A',
            '~~A or ~~~A']

        for expr in exprs:
            root = self.get_tree_root_from_expr_str(expr)
            transformed = root.apply_idempotent_law()
            self.assertTrue(transformed is not root)
            self.assertEqual(
                str(root),
                str(transformed))

    def test_simple_binary_cases(self):
        """Test binary AND/OR expressions where a transformation occurs."""
        exprs_resolving_to_A = [
            'A {} A',
            '~~A {} ~~A',
            '~~A {} A',
            'A {} ~~A']
        for expr in exprs_resolving_to_A:
            for op in ('and', 'or',):
                root = self.get_tree_root_from_expr_str(expr.format(op))
                transformed = root.apply_idempotent_law()
                self.assertTrue(transformed is not root)
                self.assertEqual(
                    str(transformed),
                    'A')

        exprs_resolving_to_not_A = [
            '~A {} ~A',
            '~~~A {} ~~~A',
            '~~~A {} ~A',
            '~A {} ~~~A']
        for expr in exprs_resolving_to_not_A:
            for op in ('and', 'or',):
                root = self.get_tree_root_from_expr_str(expr.format(op))
                transformed = root.apply_idempotent_law()
                self.assertTrue(transformed is not root)
                self.assertEqual(
                    str(transformed),
                    '\n'.join((
                        '~',
                        '`----A')))

    def test_single_clause_cnf_expression(self):
        """Test single cnf clause."""
        root = self.get_tree_root_from_expr_str(
            'A and B and A and ~~A and ~A')
        transformed = root.apply_idempotent_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(
            str(transformed),
            '\n'.join((
                'and',
                '`----and',
                '|    `----A',
                '|    `----B',
                '`----~',
                '     `----A')))

    def test_single_clause_dnf_expression(self):
        """Test single dnf clause."""
        root = self.get_tree_root_from_expr_str(
            'B or A or ~~B or ~C or ~C or ~~~C or A')
        transformed = root.apply_idempotent_law()
        self.assertTrue(transformed is not root)
        self.assertTrue(
            str(transformed),
            '\n'.join((
                'or',
                '`----or',
                '|    `----B',
                '|    `----A',
                '`----~',
                '     `----C')))

    def test_compound_expression(self):
        """Test an expression of mixed cnf, dnf, and non-normal clauses."""
        root = self.get_tree_root_from_expr_str(
            '(A or B or A or ~B or ~~B) -> (~A and A) -> (A xor D) -> '
            '(~C and ~~~~~C and ~~C)')
        transformed = root.apply_idempotent_law()
        self.assertTrue(transformed is not root)
        self.assertEqual(
            str(transformed),
            '\n'.join((
                '->',
                '`----or',
                '|    `----or',
                '|    |    `----A',
                '|    |    `----B',
                '|    `----~',
                '|         `----B',
                '`----->',
                '     `----and',
                '     |    `----~',
                '     |    |    `----A',
                '     |    `----A',
                '     `----->',
                '          `----xor',
                '          |    `----A',
                '          |    `----D',
                '          `----and',
                '               `----~',
                '               |    `----C',
                '               `----C')))
