"""Test truth table equivalence exceptions."""

from tt.errors import (
    InvalidArgumentTypeError,
    RequiresFullTableError)
from tt.tables import TruthTable

from ._helpers import TruthTableTestCase


class TestTruthTableEquivalenceExceptions(TruthTableTestCase):

    def test_invalid_argument_type(self):
        """Test passing an invalid argument type to equivalent_to."""
        t = TruthTable('A or B')

        with self.assertRaises(InvalidArgumentTypeError):
            t.equivalent_to(float())

        with self.assertRaises(InvalidArgumentTypeError):
            t.equivalent_to(None)

    def test_caller_is_not_full(self):
        """Test checking equivalence when the caller is not full."""
        partially_filled = TruthTable('A xor B', fill_all=False)
        partially_filled.fill(A=0)

        with self.assertRaises(RequiresFullTableError):
            partially_filled.equivalent_to('B xor A')

    def test_other_is_not_full(self):
        """Test checking equivalence when the argument table is not full."""
        full_table = TruthTable('A or B')
        partially_filled = TruthTable('A or B', fill_all=False)
        partially_filled.fill(B=1)

        with self.assertRaises(RequiresFullTableError):
            full_table.equivalent_to(partially_filled)
