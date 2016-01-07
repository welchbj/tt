import unittest

from tt.result_analysis import to_sop_form


class TestGetSopForm(unittest.TestCase):

    def helper_test_get_sop_form(self, high_indices=[], symbol_list=[],
                                 expected_sop_expr=''):
        actual_sop_expr = to_sop_form(high_indices, symbol_list)
        self.assertEqual(expected_sop_expr, actual_sop_expr)

    """
    test template:

    def test_(self):
        self.helper_test_get_sop_form(
            high_indices=[],
            symbol_list=[],
            expected_sop_expr='')
    """
