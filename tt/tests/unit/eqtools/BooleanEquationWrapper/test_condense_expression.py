import unittest

from eqtools import BooleanEquationWrapper, \
                    UnbalancedParenException, \
                    EmptyScopeException, \
                    GrammarException


class TestCondenseExpression(unittest.TestCase):
    """
    Areas that still need increased test coverage:
        .
    """

    # === Helper methods ===============================================================================================
    def helper_no_throw_test_condense_expression(self, raw_expr="", expected_expr="", expected_symbol_mapping={}):
        bool_expr_wrapper = BooleanEquationWrapper("F = " + raw_expr)
        condensed_expr = bool_expr_wrapper.condensed_infix_expr
        symbol_mapping = bool_expr_wrapper.unique_symbol_to_var_name_dict

        self.assertEqual(expected_expr, condensed_expr)
        self.assertDictEqual(expected_symbol_mapping, symbol_mapping)

    def helper_does_throw_test_condense_expression(self, exception_class=None, bad_expr=""):
        self.assertRaises(exception_class, BooleanEquationWrapper, "F = " + bad_expr)

    # === No-throw tests ===============================================================================================
    def test_simple_and(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="operand1 and operand2",
            expected_expr="A&B",
            expected_symbol_mapping={
                "A": "operand1",
                "B": "operand2"
            }
        )

    def test_repeated_operands(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="operand1 and operand2 or operand1 and operand3 xor operand2",
            expected_expr="A&B|A&C+B",
            expected_symbol_mapping={
                "A": "operand1",
                "B": "operand2",
                "C": "operand3"
            }
        )

    def test_chained_ands(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="op1 and op2 and op3 and op4 and op5 and op6",
            expected_expr="A&B&C&D&E&F",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3",
                "D": "op4",
                "E": "op5",
                "F": "op6"
            }
        )

    def test_operands_with_underscores(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="op_1 and op_2 or op_3 or op_______4",
            expected_expr="A&B|C|D",
            expected_symbol_mapping={
                "A": "op_1",
                "B": "op_2",
                "C": "op_3",
                "D": "op_______4"
            }
        )

    def test_leading_whitespace(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="      op1      or op2",
            expected_expr="A|B",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2"
            }
        )

    def test_trailing_whitespace(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="op1 or          op2             ",
            expected_expr="A|B",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2"
            }
        )

    def test_varied_whitespace(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="op1      or op2           and op3&&op4       or op1",
            expected_expr="A|B&C&D|A",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3",
                "D": "op4"
            }
        )

    def test_no_whitespace(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="op1||op2&&op3",
            expected_expr="A|B&C",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3"
            }
        )

    def test_chained_enclosed_expressions(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="(op1 and op2) or (op3 and op4) or (op5 and op6)",
            expected_expr="(A&B)|(C&D)|(E&F)",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3",
                "D": "op4",
                "E": "op5",
                "F": "op6"
            }
        )

    def test_no_white_space_plain_english_operations_enclosed_expressions(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="(op1 and op2)or(op3 and op4)or(op5 and op6)",
            expected_expr="(A&B)|(C&D)|(E&F)",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3",
                "D": "op4",
                "E": "op5",
                "F": "op6"
            }
        )

    def test_no_white_space_symbolic_operations_enclosed_expressions(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="(op1&&op2)||(op3&&op4)||(op5&&op6)",
            expected_expr="(A&B)|(C&D)|(E&F)",
            expected_symbol_mapping={
                "A": "op1",
                "B": "op2",
                "C": "op3",
                "D": "op4",
                "E": "op5",
                "F": "op6"
            }
        )

    def test_operands_with_names_similar_to_symbol_mappings(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="A and AA or AB or BB or C or DD or D and FFF",
            expected_expr="A&B|C|D|E|F|G&H",
            expected_symbol_mapping={
                "A": "A",
                "B": "AA",
                "C": "AB",
                "D": "BB",
                "E": "C",
                "F": "DD",
                "G": "D",
                "H": "FFF"
            }
        )

    def test_operations_with_similar_symbols_or(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="AN and ND nand NAN and a_and and ANDAND",
            expected_expr="A&B$C&D&E",
            expected_symbol_mapping={
                "A": "AN",
                "B": "ND",
                "C": "NAN",
                "D": "a_and",
                "E": "ANDAND"
            }
        )

    def test_operations_with_similar_symbols_and(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="O or o or OR_OR xor oo nor or_ xnor o",
            expected_expr="A|B|C+D%E@B",
            expected_symbol_mapping={
                "A": "O",
                "B": "o",
                "C": "OR_OR",
                "D": "oo",
                "E": "or_",
            }
        )

    def test_only_0(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="0",
            expected_expr="0",
            expected_symbol_mapping={
                # empty
            }
        )

    def test_only_1(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="1",
            expected_expr="1",
            expected_symbol_mapping={
                # empty
            }
        )

    def test_only_0s_and_1s(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="1 and 0 or 1 or 0 xor 1 nand 1",
            expected_expr="1&0|1|0+1$1",
            expected_symbol_mapping={
                # empty
            }
        )

    def test_not_one_operand(self):
        self.helper_no_throw_test_condense_expression(
            raw_expr="not operand",
            expected_expr="1+A",
            expected_symbol_mapping={
                "A": "operand"
            }
        )

    # === Expect-throws tests ==========================================================================================

    def test_only_two_operands(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="operand1 operand2"
        )

    def test_only_one_operation(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="or"
        )

    def test_only_two_operations(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="or and"
        )

    def test_only_three_operations(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="and or and"
        )

    def test_operation_with_only_leading_operand(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="operand or"
        )

    def test_operation_with_only_trailing_operand(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="or operand"
        )

    def test_chained_unbalanced_operations(self):
        self.helper_does_throw_test_condense_expression(
            exception_class=GrammarException,
            bad_expr="op1 and op2 and op3 and op4 and"
        )
