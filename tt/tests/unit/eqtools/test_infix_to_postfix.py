import unittest
from eqtools import infix_to_postfix

class TestInfixToPostfix (unittest.TestCase):

    def infix_to_postfix_test_helper(self, infix_expr="", expected_postfix="", expect_throws=False):
        if expect_throws:
            self.assertRaises(RuntimeError, infix_to_postfix, infix_expr)
        else:
            result_postfix = infix_to_postfix(infix_expr)
            self.assertEqual(result_postfix, expected_postfix)

    def test_simple_two_syms(self):
        self.infix_to_postfix_test_helper(
            infix_expr="A&B",
            expected_postfix="AB&"
        )

    def test_simple_parens(self):
        self.infix_to_postfix_test_helper(
            infix_expr="(A&B)",
            expected_postfix="AB&"
        )

    def test_simple_lots_of_parens(self):
        self.infix_to_postfix_test_helper(
            infix_expr="((((((((((A&B))))))))))",
            expected_postfix="AB&"
        )

    def test_distr_parens(self):
        self.infix_to_postfix_test_helper(
            infix_expr="A&(B&C)",
            expected_postfix="ABC&&"
        )

    def DISABLED_test_simple_uneven_parens(self):
        self.infix_to_postfix_test_helper(
            infix_expr="((A&B)",
            expected_postfix="AB&",
            expect_throws=True
        )

    def test_simple_three_operands(self):
        self.infix_to_postfix_test_helper(
            infix_expr="A|B|C",
            expected_postfix="AB|C|"
        )