import unittest

from tt.eqtools import replace_inputs


class TestReplaceInputs(unittest.TestCase):
    """This is a fairly simple function to test, because all input is assumed
    to be well-formed.
    """

    # === Helper Methods ======================================================
    def helper_test_replace_inputs(self, postfix_expr='', inputs=[],
                                   input_vals=[], expected_result=''):
        self.assertEqual(expected_result,
                         replace_inputs(postfix_expr, inputs, input_vals))

    # === Test Methods ========================================================
    def test_two_symbols(self):
        self.helper_test_replace_inputs(
            postfix_expr='AB|',
            inputs=['A', 'B'],
            input_vals=['1', '0'],
            expected_result='10|')

    def test_two_symbols_repeated(self):
        self.helper_test_replace_inputs(
            postfix_expr='AA&',
            inputs=['A'],
            input_vals=['0'],
            expected_result='00&')

    def test_three_symbols(self):
        self.helper_test_replace_inputs(
            postfix_expr='ABC+&',
            inputs=['A', 'B', 'C'],
            input_vals=['0', '1', '0'],
            expected_result='010+&')

    def test_three_symbols_repeated(self):
        self.helper_test_replace_inputs(
            postfix_expr='CCC+&',
            inputs=['C'],
            input_vals=['0'],
            expected_result='000+&')
