"""Tests for the TruthTable class's static methods."""

from tt.tables import TruthTable

from ._helpers import TruthTableTestCase


class TestStaticMethodsTruthTable(TruthTableTestCase):

    def test_generate_symbols_0(self):
        """Test generating 0 symbols."""
        self.assertEqual(
            TruthTable.generate_symbols(0),
            [])

    def test_generate_symbols_lt_26(self):
        """Test generating less than 26 symbols."""
        self.assertEqual(
            TruthTable.generate_symbols(5),
            ['A', 'B', 'C', 'D', 'E'])

    def test_generate_symbols_eq_26(self):
        """Test generating exactly 26 symbols."""
        self.assertEqual(
            TruthTable.generate_symbols(26),
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

    def test_generate_symbols_gt_26(self):
        """Test generating more 26 symbols (the first boundary)."""
        self.assertEqual(
            TruthTable.generate_symbols(27),
            ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK',
             'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV',
             'AW', 'AX', 'AY', 'AZ', 'BA'])

    def test_input_combos_empty(self):
        """Test getting an empty set of input_combos."""
        self.assertEqual(
            list(TruthTable.input_combos(0)),
            [()])

    def test_input_combos_one_repeat(self):
        """Test getting input combos for 1 repeat."""
        self.assertEqual(
            list(TruthTable.input_combos(1)),
            [(False,), (True,)])

    def test_input_combos_multiple_repeats(self):
        """Test getting input combos for more than one repeats."""
        self.assertEqual(
            list(TruthTable.input_combos(2)),
            [(False, False,),
             (False, True,),
             (True, False,),
             (True, True,)])
