from tt.tests.utils import FunctionalTestCase


class TestTruthTableGeneration(FunctionalTestCase):

    def test_simple_small_table(self):
        # python -m tt --table F = A or B
        self.functional_test_helper(
            cl_args=['--table', 'F = A or B'],
            expected_stdout=(
                '+---+---+---+\n'
                '| A | B | F |\n'
                '+---+---+---+\n'
                '| 0 | 0 | 0 |\n'
                '| 0 | 1 | 1 |\n'
                '| 1 | 0 | 1 |\n'
                '| 1 | 1 | 1 |\n'
                '+---+---+---+\n'
                '\n'),
            expected_stderr='')

    def test_no_opts_defaults_to_table(self):
        # python -m tt F = A or B
        self.functional_test_helper(
            cl_args=['F = A or B'],
            expected_stdout=(
                '+---+---+---+\n'
                '| A | B | F |\n'
                '+---+---+---+\n'
                '| 0 | 0 | 0 |\n'
                '| 0 | 1 | 1 |\n'
                '| 1 | 0 | 1 |\n'
                '| 1 | 1 | 1 |\n'
                '+---+---+---+\n'
                '\n'),
            expected_stderr='')

    def test_simple_big_table(self):
        self.functional_test_helper(
            # python -m tt --table f = a and b xor c nand d or e
            cl_args=['--table', 'f = a and b xor c nand d or e'],
            expected_stdout=(
                '+---+---+---+---+---+---+\n'
                '| a | b | c | d | e | f |\n'
                '+---+---+---+---+---+---+\n'
                '| 0 | 0 | 0 | 0 | 0 | 0 |\n'
                '| 0 | 0 | 0 | 0 | 1 | 1 |\n'
                '| 0 | 0 | 0 | 1 | 0 | 0 |\n'
                '| 0 | 0 | 0 | 1 | 1 | 1 |\n'
                '| 0 | 0 | 1 | 0 | 0 | 0 |\n'
                '| 0 | 0 | 1 | 0 | 1 | 1 |\n'
                '| 0 | 0 | 1 | 1 | 0 | 0 |\n'
                '| 0 | 0 | 1 | 1 | 1 | 1 |\n'
                '| 0 | 1 | 0 | 0 | 0 | 0 |\n'
                '| 0 | 1 | 0 | 0 | 1 | 1 |\n'
                '| 0 | 1 | 0 | 1 | 0 | 0 |\n'
                '| 0 | 1 | 0 | 1 | 1 | 1 |\n'
                '| 0 | 1 | 1 | 0 | 0 | 0 |\n'
                '| 0 | 1 | 1 | 0 | 1 | 1 |\n'
                '| 0 | 1 | 1 | 1 | 0 | 0 |\n'
                '| 0 | 1 | 1 | 1 | 1 | 1 |\n'
                '| 1 | 0 | 0 | 0 | 0 | 1 |\n'
                '| 1 | 0 | 0 | 0 | 1 | 1 |\n'
                '| 1 | 0 | 0 | 1 | 0 | 1 |\n'
                '| 1 | 0 | 0 | 1 | 1 | 1 |\n'
                '| 1 | 0 | 1 | 0 | 0 | 1 |\n'
                '| 1 | 0 | 1 | 0 | 1 | 1 |\n'
                '| 1 | 0 | 1 | 1 | 0 | 0 |\n'
                '| 1 | 0 | 1 | 1 | 1 | 1 |\n'
                '| 1 | 1 | 0 | 0 | 0 | 1 |\n'
                '| 1 | 1 | 0 | 0 | 1 | 1 |\n'
                '| 1 | 1 | 0 | 1 | 0 | 0 |\n'
                '| 1 | 1 | 0 | 1 | 1 | 1 |\n'
                '| 1 | 1 | 1 | 0 | 0 | 1 |\n'
                '| 1 | 1 | 1 | 0 | 1 | 1 |\n'
                '| 1 | 1 | 1 | 1 | 0 | 1 |\n'
                '| 1 | 1 | 1 | 1 | 1 | 1 |\n'
                '+---+---+---+---+---+---+\n'
                '\n'),
            expected_stderr='')

    def test_repeated_input_table(self):
        # python -m tt --table out = op1 and op1
        self.functional_test_helper(
            cl_args=['--table', 'out = op1 and op1'],
            expected_stdout=(
                '+-----+-----+\n'
                '| op1 | out |\n'
                '+-----+-----+\n'
                '|  0  |  0  |\n'
                '|  1  |  1  |\n'
                '+-----+-----+\n'
                '\n'),
            expected_stderr='')
