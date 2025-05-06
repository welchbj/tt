"""Tests for truth table magic access methods (__getitem__, __iter__, etc.)."""

from tt.tables import TruthTable

from ._helpers import TruthTableTestCase


class TestTruthTableMagicAccessMethods(TruthTableTestCase):

    def test_table_iter_unfilled(self):
        """Test iterating through a table that has not been filled."""
        t = TruthTable('A or B', fill_all=False)
        count = 0

        for inputs, result in t:
            count += 1

        self.assertEqual(count, 0)

    def test_table_iter_partially_filled(self):
        """Test iterating through a table that is partially filled."""
        t = TruthTable('A xor C', fill_all=False)
        t.fill(C=1)
        count = 0

        for inputs, result in t:
            if count == 0:
                self.assertEqual(inputs.A, False)
                self.assertEqual(inputs.C, True)
                self.assertEqual(result, True)
            elif count == 1:
                self.assertEqual(inputs.A, True)
                self.assertEqual(inputs.C, True)
                self.assertEqual(result, False)

            count += 1

        self.assertEqual(count, 2)

    def test_table_iter_completely_filled(self):
        """Test iterating through a table that is completely full."""
        t = TruthTable('B nand D')
        count = 0

        for inputs, result in t:
            if count == 0:
                self.assertEqual(inputs.B, False)
                self.assertEqual(inputs.D, False)
                self.assertEqual(result, True)
            elif count == 1:
                self.assertEqual(inputs.B, False)
                self.assertEqual(inputs.D, True)
                self.assertEqual(result, True)
            elif count == 2:
                self.assertEqual(inputs.B, True)
                self.assertEqual(inputs.D, False)
                self.assertEqual(result, True)
            elif count == 3:
                self.assertEqual(inputs.B, True)
                self.assertEqual(inputs.D, True)
                self.assertEqual(result, False)

            count += 1

        self.assertEqual(count, 4)

    def test_table_getitem(self):
        """Test indexing the table to get its results."""
        t = TruthTable('A or B', fill_all=False)
        for i in range(4):
            self.assertEqual(None, t[i])

        t.fill(A=0)
        self.assertEqual(t[0], False)
        self.assertEqual(t[1], True)

        t.fill()
        self.assertEqual(t[0b00], False)
        self.assertEqual(t[0b01], True)
        self.assertEqual(t[0b10], True)
        self.assertEqual(t[0b11], True)

        t = TruthTable(from_values='1xx1')
        self.assertEqual(t[0b00], True)
        self.assertEqual(t[0b01], 'x')
        self.assertEqual(t[0b10], 'x')
        self.assertEqual(t[0b11], True)
