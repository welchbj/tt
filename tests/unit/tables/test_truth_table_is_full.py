"""Tests for checking if a truth table is full."""

from tt.tables import TruthTable

from ._helpers import TruthTableTestCase


class TestTruthTableIsFull(TruthTableTestCase):

    def test_is_full_from_expr_in_init(self):
        """Test is_full attr when filled from an expr in __init__."""
        t = TruthTable('A or B')
        self.assertTrue(t.is_full)

    def test_is_full_from_values_in_init(self):
        """Test is_full attr when filled via from_values in __init__."""
        sixteen_dont_cares = 'x' * 16
        t = TruthTable(from_values=sixteen_dont_cares)
        self.assertTrue(t.is_full)

    def test_is_full_from_single_fill_call(self):
        """Test is_full attr when filled via one fill() call."""
        t = TruthTable('A nand B xor C', fill_all=False)
        self.assertFalse(t.is_full)
        t.fill()
        self.assertTrue(t.is_full)

    def test_is_full_iterative(self):
        """Test is_full attr when table is iteratively filled."""
        t = TruthTable('A nand B xor C', fill_all=False)
        self.assertFalse(t.is_full)
        t.fill(A=0)
        self.assertFalse(t.is_full)
        t.fill(B=1)
        self.assertFalse(t.is_full)
        t.fill(C=0)
        self.assertFalse(t.is_full)
        t.fill(B=0)
        self.assertTrue(t.is_full)
