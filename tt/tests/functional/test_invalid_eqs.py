from tt.tests.utils import FunctionalTestCase


class TestInvalidEqs(FunctionalTestCase):

    def test_multiple_equals_signs(self):
        # python -m tt --table F = = A or B
        self.functional_test_helper(
            cl_args=['--table', 'F = = A or B'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unexpected equals sign.\n'
                'ERROR: F = = A or B\n'
                'ERROR:     ^\n'))

    def test_no_equals_sign(self):
        # python -m tt --table A or B
        self.functional_test_helper(
            cl_args=['--table', 'A or B'],
            expected_stdout='',
            expected_stderr='ERROR: Equation did not contain equals sign.\n')

    def test_output_symbol_used_in_expr(self):
        # python -m tt --table out = operand1 or out xor operand2
        self.functional_test_helper(
            cl_args=['--table', 'out = operand1 or out xor operand2'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Output symbol used as an input variable in your '
                'expression.\n'
                'ERROR: operand1 or out xor operand2\n'
                'ERROR:             ^\n'))

    def test_invalid_operand_pos(self):
        # python -m tt --table out = op1 and op2 op3 or op4
        self.functional_test_helper(
            cl_args=['--table', 'out = op1 and op2 op3 or op4'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unexpected operand.\n'
                'ERROR: op1 and op2 op3 or op4\n'
                'ERROR:             ^\n'))

    def test_invalid_operation_pos(self):
        # python -m tt --table out = op1 and op2 or or op3
        self.functional_test_helper(
            cl_args=['--table', 'out = op1 and op2 or or op3'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unexpected operation.\n'
                'ERROR: op1 and op2 or or op3\n'
                'ERROR:                ^\n'))

    def test_unbalanced_left_paren(self):
        # python -m tt --table F = A xor ((B or C or D)
        self.functional_test_helper(
            cl_args=['--table', 'F = A xor ((B or C or D)'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unbalanced left parenthesis.\n'
                'ERROR: A xor ((B or C or D)\n'
                'ERROR:       ^\n'))

    def test_unbalanced_right_paren(self):
        # python -m tt --table F = A or (B and C)) or D
        self.functional_test_helper(
            cl_args=['--table', 'F = A or (B and C)) or D'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unbalanced right parenthesis.\n'
                'ERROR: A or (B and C)) or D\n'
                'ERROR:               ^\n'))

    def test_unexpected_paren(self):
        # python -m tt --table F = ()
        self.functional_test_helper(
            cl_args=['--table', 'F = ()'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Unexpected parenthesis.\n'
                'ERROR: ()\n'
                'ERROR:  ^\n'
                ))

    def test_bad_symbol(self):
        # python -m tt --table F = op_*1
        self.functional_test_helper(
            cl_args=['--table', 'F = op_*1'],
            expected_stdout='',
            expected_stderr=(
                'ERROR: Invalid symbol.\n'
                'ERROR: op_*1\n'
                'ERROR:    ^\n'))
