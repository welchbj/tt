"""Tests for truth table magic access methods (__getitem__, __iter__, etc.)."""

from ._helpers import TruthTableTestCase
from ....tables import TruthTable


class TestTruthTableAccessMethods(TruthTableTestCase):

    def test_table_iter(self):
        """Test iterating through a table's rows."""
        t = TruthTable('A or B', fill_all=False)

        count = 0
        for inputs, result in t:
            count += 1
        self.assertEqual(count, 0)

        t.fill()
        expected = [
            ((False, False,), False),
            ((False, True,), True),
            ((True, False,), True),
            ((True, True,), True),
        ]

        count = 0
        for inputs, result in t:
            expected_inputs, expected_result = expected[count]
            self.assertEqual(expected_inputs, inputs)
            self.assertEqual(expected_result, result)
            count += 1

        self.assertEqual(len(expected), count)

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
