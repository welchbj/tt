"""Tests for different expression forms."""

from ._helpers import ExpressionTestCase


class TestBooleanExpressionForms(ExpressionTestCase):

    def test_is_cnf(self):
        """Test CNF detection."""
        self.assert_is_cnf('A or B or not C or D or not E')
        self.assert_is_cnf('!A and B and !C and D and E')
        self.assert_is_cnf('(A or B) and C')
        self.assert_is_cnf('A and B and (C or D)')
        self.assert_is_cnf('(A or B or C or D) and (E or F) and G')
        self.assert_is_cnf('(~A or ~B) and (C or D) and (E or F)')
        self.assert_is_cnf('((A) or B) and (C)')

        self.assert_not_cnf('~~A')
        self.assert_not_cnf('A xor B')
        self.assert_not_cnf('~(A or B) and (C or D)')
        self.assert_not_cnf('(A or B) and (C or D) and (C or (B and D))')

    def test_is_dnf(self):
        """Test DNF detection."""
        self.assert_is_dnf('A and B and !C and D')
        self.assert_is_dnf('op1 or op2 or ~op3 or op4 or ~op5')
        self.assert_is_dnf('A or (A and B)')
        self.assert_is_dnf('(A and B) or C')
        self.assert_is_dnf('(A and B and C) or (A and B) or A')
        self.assert_is_dnf('(~A and ~B) or (C and D) or ((E and F))')
        self.assert_is_dnf('(A and B and C and D and E) or (F and G)')
        self.assert_is_dnf('(A & B) or (C & !D & E) or (F & G) or (H & I)')

        self.assert_not_dnf('~~A')
        self.assert_not_dnf('~~~A')
        self.assert_not_dnf('A nand B')
        self.assert_not_dnf('(A and B) -> C')
        self.assert_not_dnf('~(A and B) or (C and D)')
        self.assert_not_dnf('(A and B) or ~(C and D)')
        self.assert_not_dnf('(A and B) or (A and (B or C))')
