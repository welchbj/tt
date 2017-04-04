"""Tests for filling truth tables that cause exceptions."""

from ._helpers import TruthTableTestCase
from ....errors import (AlreadyFullTableError, ExtraSymbolError,
                        InvalidBooleanValueError)
from ....tables import TruthTable


class TestTruthTableFillExceptions(TruthTableTestCase):

    def test_fill_invalid_symbol(self):
        """Test passing an non-existent symbol in the fill method."""
        self.helper_test_truth_table_fill_raises(
            '(op1 xor op2) and op3',
            op4=True,
            expected_exc_type=ExtraSymbolError)

    def test_fill_invalid_boolean_value(self):
        """Test passing an invalid Boolean value to the fill method."""
        self.helper_test_truth_table_fill_raises(
            'A or B',
            A=-1,
            expected_exc_type=InvalidBooleanValueError)

    def test_attempt_to_fill_table_already_filled_from_values(self):
        """Ensure that we cannot fill() a table built from specified values."""
        t = TruthTable(from_values='xxxx', ordering=['A', 'B'])
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=1)

    def test_attempt_to_fill_table_already_filled_on_init_from_expr(self):
        """Ensure that we cannot fill a table already filled from an expr."""
        t = TruthTable('A or B')
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=0)

    def test_attempt_to_fill_table_already_iteratively_filled(self):
        """Ensure that we cannot fill a table already iteratively filled."""
        t = TruthTable('A nand B', fill_all=False)
        t.fill(A=0)
        t.fill(A=1)
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=0)
