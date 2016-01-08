from tt.tests.utils import FunctionalTestCase


class TestInvalidArgs(FunctionalTestCase):

    def test_no_args(self):
        # python -m tt
        self.functional_test_helper(
            cl_args=[],
            expected_stdout='',
            expected_stderr='ERROR: A non-empty equation is required.\n')

    def test_empty_str_equation(self):
        # python -m tt --table ""
        self.functional_test_helper(
            cl_args=['--table', ''],
            expected_stdout='',
            expected_stderr='ERROR: A non-empty equation is required.\n')

    def test_empty_str_equation_no_opts(self):
        # python -m tt ""
        self.functional_test_helper(
            cl_args=[''],
            expected_stdout='',
            expected_stderr='ERROR: A non-empty equation is required.\n')
