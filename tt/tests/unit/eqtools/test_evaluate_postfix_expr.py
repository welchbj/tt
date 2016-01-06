import unittest

from tt.eqtools import eval_postfix_expr
from tt.schema_provider import (SYM_XOR, SYM_XNOR, SYM_AND, SYM_NAND, SYM_NOR,
                                SYM_OR)


class TestEvaluatePostfixExpr(unittest.TestCase):

    """Testing for this function is fairly simple because we are using a proven
    algorithm and all input is assumed to be well-formed.
    """

    # === Helper Methods ======================================================
    def helper_test_postfix_expr(self, expr_to_eval='', expected_result=-1):
        self.assertEqual(expected_result, eval_postfix_expr(expr_to_eval))

    # === Test Methods ========================================================
    def test_two_operands_xor(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [0, 1, 1, 0]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_XOR,
                expected_result=expected_result)

    def test_two_operands_xnor(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [1, 0, 0, 1]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_XNOR,
                expected_result=expected_result)

    def test_two_operands_and(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [0, 0, 0, 1]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_AND,
                expected_result=expected_result)

    def test_two_operands_nand(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [1, 1, 1, 0]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_NAND,
                expected_result=expected_result)

    def test_two_operands_or(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [0, 1, 1, 1]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_OR,
                expected_result=expected_result)

    def test_two_operands_nor(self):
        input_pairs = ['00', '01', '10', '11']
        expected_results = [1, 0, 0, 0]
        for input_pair, expected_result in zip(input_pairs, expected_results):
            self.helper_test_postfix_expr(
                expr_to_eval=input_pair+SYM_NOR,
                expected_result=expected_result)
