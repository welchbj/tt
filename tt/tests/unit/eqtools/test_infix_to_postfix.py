import unittest

from eqtools import infix_to_postfix


class TestInfixToPostfix(unittest.TestCase):

    # === Helper methods ===============================================================================================
    def helper_infix_to_postfix(self, infix_expr="", symbol_list=[], expected_postfix_expr=""):
        self.assertEqual(expected_postfix_expr, infix_to_postfix(infix_expr, symbol_list))

    # === Tests ========================================================================================================
    def test_one_operand_symbolic(self):
        self.helper_infix_to_postfix(
            infix_expr="A",
            symbol_list=["A"],
            expected_postfix_expr="A"
        )

    def test_one_operand_constant(self):
        self.helper_infix_to_postfix(
            infix_expr="1",
            symbol_list=[],
            expected_postfix_expr="1"
        )

    def test_two_operands_symbolic(self):
        self.helper_infix_to_postfix(
            infix_expr="A&B",
            symbol_list=["A", "B"],
            expected_postfix_expr="AB&"
        )

    def test_two_operands_constants(self):
        self.helper_infix_to_postfix(
            infix_expr="1+1",
            symbol_list=[],
            expected_postfix_expr="11+"
        )

    def test_two_operands_one_symbolic_one_constant(self):
        self.helper_infix_to_postfix(
            infix_expr="A&0",
            symbol_list=["A"],
            expected_postfix_expr="A0&"
        )

    def test_two_operands_single_set_of_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="(A&B)",
            symbol_list=["A", "B"],
            expected_postfix_expr="AB&"
        )

    def test_two_operands_excessive_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="(((((A&B)))))",
            symbol_list=["A", "B"],
            expected_postfix_expr="AB&"
        )

    def test_three_operands_first_precedence_higher(self):
        self.helper_infix_to_postfix(
            infix_expr="A&B|C",
            symbol_list=["A", "B", "C"],
            expected_postfix_expr="AB&C|"
        )

    def test_three_operands_second_precedence_higher(self):
        self.helper_infix_to_postfix(
            infix_expr="A|B&C",
            symbol_list=["A", "B", "C"],
            expected_postfix_expr="ABC&|"
        )

    def test_three_operands_override_higher_first_precedence_with_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="A&(B|C)",
            symbol_list=["A", "B", "C"],
            expected_postfix_expr="ABC|&"
        )

    def test_three_operands_override_higher_second_precedence_with_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="(A|B)&C",
            symbol_list=["A", "B", "C"],
            expected_postfix_expr="AB|C&"
        )

    def test_four_operands_equal_precedence(self):
        self.helper_infix_to_postfix(
            infix_expr="A|B|C|D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="ABCD|||"
        )

    def test_four_operands_ascending_precedence(self):
        self.helper_infix_to_postfix(
            infix_expr="A|B&C+D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="ABCD+&|"
        )

    def test_four_operands_descending_precedence(self):
        self.helper_infix_to_postfix(
            infix_expr="A+B&C|D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="AB+C&D|"
        )

    def test_four_operands_two_clauses_joined_by_lower_precedence(self):
        self.helper_infix_to_postfix(
            infix_expr="A&B|C&D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="AB&CD&|"
        )

    def test_four_operands_two_clauses_joined_by_higher_precedence(self):
        self.helper_infix_to_postfix(
            infix_expr="A&B+C&D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="ABC+D&&"
        )

    def test_four_operands_two_clauses_joined_by_higher_precedence_overidden_by_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="(A|B)&(C|D)",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="AB|CD|&"
        )

    def test_four_operands_two_clauses_joined_by_lower_precedence_overidden_by_parens(self):
        self.helper_infix_to_postfix(
            infix_expr="A&(B|C)&D",
            symbol_list=["A", "B", "C", "D"],
            expected_postfix_expr="ABC|D&&"
        )