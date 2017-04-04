"""Test truth table equivalence."""

from ._helpers import TruthTableTestCase
from ....expressions import BooleanExpression
from ....tables import TruthTable


class TestTruhtTableEquivalence(TruthTableTestCase):

    def test_equivalent_to_bexpr(self):
        """Test when the other source of truth is a BooleanExpression."""
        t = TruthTable(from_values='0111')
        b = BooleanExpression('op1 or op2')

        self.assertTrue(t.equivalent_to(b))

    def test_equivalent_to_table(self):
        """Test when the other source of truth is a TruthTable."""
        t1 = TruthTable(from_values='0001')
        t2 = TruthTable('C and D')

        self.assertTrue(t1.equivalent_to(t2))
        self.assertTrue(t2.equivalent_to(t1))

    def test_equivalent_to_str(self):
        """Test when the other source of truth is a str."""
        t = TruthTable(from_values='0110')

        self.assertTrue(t.equivalent_to('F xor E'))

    def test_equivalent_to_self(self):
        """Test that a table is equivalent to itself."""
        t = TruthTable('A nand B nor C xor D')

        self.assertTrue(t.equivalent_to(t))

    def test_unequally_sized_tables(self):
        """Test that unequally sized tables are not equivalent."""
        t1 = TruthTable(from_values='0110')
        t2 = TruthTable(from_values='0110011001100110')

        self.assertFalse(t1.equivalent_to(t2))
        self.assertFalse(t2.equivalent_to(t1))

    def test_unequivalent_tables_without_dont_cares(self):
        """Test a case where two tables w/o don't cares are not equivalent."""
        t1 = TruthTable(from_values='0001')
        t2 = TruthTable(from_values='0000')

        self.assertFalse(t1.equivalent_to(t2))
        self.assertFalse(t2.equivalent_to(t1))

    def test_equivalent_tables_with_dont_cares(self):
        """Test a case where two tables w/ don't cares are equivalent."""
        t1 = TruthTable(from_values='0x10')
        t2 = TruthTable(from_values='0x10')

        self.assertTrue(t1.equivalent_to(t2))
        self.assertTrue(t2.equivalent_to(t1))

    def test_unequivalent_caller_contains_dont_cares(self):
        """Test an unequivalent case where the caller has don't cares."""
        t1 = TruthTable(from_values='0x01')
        t2 = TruthTable(from_values='0100')

        self.assertFalse(t1.equivalent_to(t2))

    def test_equivalent_caller_contains_dont_cares(self):
        """Test an equivalent case where the caller has don't cares."""
        t1 = TruthTable(from_values='0x01')
        t2 = TruthTable(from_values='0101')

        self.assertTrue(t1.equivalent_to(t2))

    def test_unequivalent_other_contains_dont_cares(self):
        """Test an unequivalent case where the other has don't cares."""
        t1 = TruthTable(from_values='0101')
        t2 = TruthTable(from_values='1xxx')

        self.assertFalse(t1.equivalent_to(t2))
