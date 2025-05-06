"""Test iterating through clauses via nodes."""

from tt.errors import RequiresNormalFormError

from ._helpers import ExpressionTreeAndNodeTestCase


class TestNodeIterClauses(ExpressionTreeAndNodeTestCase):

    def test_not_normal_form(self):
        """Test trying to iter clauses on an expression not in normal form."""
        with self.assertRaises(RequiresNormalFormError):
            root = self.get_tree_root_from_expr_str('~(A or B)')
            for node in root.iter_clauses():
                pass

    def test_iter_clauses_defaults_to_cnf(self):
        """Test iterating over an ambiguous expression, ensuring CNF order."""
        root = self.get_tree_root_from_expr_str('A and B and C and D')
        self.assertTrue(root.is_cnf)
        self.assertTrue(root.is_dnf)

        # DNF would recognize this as 1 clause
        clauses = list(root.iter_clauses())
        self.assertEqual(4, len(clauses))

    def test_iter_clauses_falls_back_to_dnf(self):
        """Test iterating over a DNF expression, ensuring DNF order."""
        root = self.get_tree_root_from_expr_str(
            '(A and ~B) or (~C and D) or (~E and ~F)')
        self.assertFalse(root.is_cnf)
        self.assertTrue(root.is_dnf)

        clauses = list(root.iter_clauses())
        self.assertEqual(3, len(clauses))

    def test_cnf_when_not_cnf(self):
        """Test that an exc is raised when invalid attempt at iter cnf."""
        root = self.get_tree_root_from_expr_str('A xor B')
        self.assertFalse(root.is_cnf)

        with self.assertRaises(RequiresNormalFormError):
            for node in root.iter_cnf_clauses():
                pass

    def test_iter_cnf_single_operand_clauses(self):
        """Test iterating over a CNF expression of single operand clauses."""
        root = self.get_tree_root_from_expr_str('A and B and C and D')

        clauses = root.iter_cnf_clauses()
        self.assertEqual(next(clauses).symbol_name, 'A')
        self.assertEqual(next(clauses).symbol_name, 'B')
        self.assertEqual(next(clauses).symbol_name, 'C')
        self.assertEqual(next(clauses).symbol_name, 'D')

        with self.assertRaises(StopIteration):
            next(clauses)

    def test_iter_cnf_one_multi_operand_clause(self):
        """Test iterating over a single-clause CNF expression."""
        root = self.get_tree_root_from_expr_str('A or B or C')

        clauses = root.iter_cnf_clauses()
        node = next(clauses)
        with self.assertRaises(StopIteration):
            next(clauses)

        self.assertEqual(node.symbol_name, 'or')
        self.assertEqual(node.l_child.symbol_name, 'A')
        self.assertEqual(node.r_child.symbol_name, 'or')
        self.assertEqual(node.r_child.l_child.symbol_name, 'B')
        self.assertEqual(node.r_child.r_child.symbol_name, 'C')

    def test_iter_cnf_multi_clauses(self):
        """Test iterating over CNF expressions with multiple clauses."""
        root = self.get_tree_root_from_expr_str(
            '(A or B or C) and (D or E or F)')

        clauses = root.iter_cnf_clauses()
        first_clause = next(clauses)
        second_clause = next(clauses)
        with self.assertRaises(StopIteration):
            next(clauses)

        self.assertEqual(first_clause.symbol_name, 'or')
        self.assertEqual(first_clause.l_child.symbol_name, 'A')
        self.assertEqual(first_clause.r_child.symbol_name, 'or')
        self.assertEqual(first_clause.r_child.l_child.symbol_name, 'B')
        self.assertEqual(first_clause.r_child.r_child.symbol_name, 'C')

        self.assertEqual(second_clause.symbol_name, 'or')
        self.assertEqual(second_clause.l_child.symbol_name, 'D')
        self.assertEqual(second_clause.r_child.symbol_name, 'or')
        self.assertEqual(second_clause.r_child.l_child.symbol_name, 'E')
        self.assertEqual(second_clause.r_child.r_child.symbol_name, 'F')

    def test_dnf_when_not_dnf(self):
        """Test that an exc is raised when invalid attempt at iter dnf."""
        root = self.get_tree_root_from_expr_str(
            '(A or B) and (C or D) and (E or F)')
        self.assertFalse(root.is_dnf)

        with self.assertRaises(RequiresNormalFormError):
            for node in root.iter_dnf_clauses():
                pass

    def test_iter_dnf_single_operand_clauses(self):
        """Test iterating over a DNF expression of single operand clauses."""
        root = self.get_tree_root_from_expr_str('A or B or C or D')

        clauses = root.iter_dnf_clauses()
        self.assertEqual(next(clauses).symbol_name, 'A')
        self.assertEqual(next(clauses).symbol_name, 'B')
        self.assertEqual(next(clauses).symbol_name, 'C')
        self.assertEqual(next(clauses).symbol_name, 'D')

        with self.assertRaises(StopIteration):
            next(clauses)

    def test_iter_dnf_one_multi_operand_clause(self):
        """Test iterating over a single-clause DNF expression."""
        root = self.get_tree_root_from_expr_str('A and B and C')

        clauses = root.iter_dnf_clauses()
        node = next(clauses)
        with self.assertRaises(StopIteration):
            next(clauses)

        self.assertEqual(node.symbol_name, 'and')
        self.assertEqual(node.l_child.symbol_name, 'A')
        self.assertEqual(node.r_child.symbol_name, 'and')
        self.assertEqual(node.r_child.l_child.symbol_name, 'B')
        self.assertEqual(node.r_child.r_child.symbol_name, 'C')

    def test_iter_dnf_multi_clauses(self):
        """Test iterating over DNF expressions with multiple clauses."""
        root = self.get_tree_root_from_expr_str(
            '(A and B and C) or (D and E and F)')

        clauses = root.iter_dnf_clauses()
        first_clause = next(clauses)
        second_clause = next(clauses)
        with self.assertRaises(StopIteration):
            next(clauses)

        self.assertEqual(first_clause.symbol_name, 'and')
        self.assertEqual(first_clause.l_child.symbol_name, 'A')
        self.assertEqual(first_clause.r_child.symbol_name, 'and')
        self.assertEqual(first_clause.r_child.l_child.symbol_name, 'B')
        self.assertEqual(first_clause.r_child.r_child.symbol_name, 'C')

        self.assertEqual(second_clause.symbol_name, 'and')
        self.assertEqual(second_clause.l_child.symbol_name, 'D')
        self.assertEqual(second_clause.r_child.symbol_name, 'and')
        self.assertEqual(second_clause.r_child.l_child.symbol_name, 'E')
        self.assertEqual(second_clause.r_child.r_child.symbol_name, 'F')
