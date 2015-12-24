from tt.tests.utils import FunctionalTestCase


class TestTruthTableGeneration(FunctionalTestCase):

# === No Error Tests ==========================================================
    def test_simple(self):
        self.functional_test_helper(
            cl_args=[''],
            expected_stdout='',
            expected_stderr='ERROR: Equation did not contain equals sign.\n')
