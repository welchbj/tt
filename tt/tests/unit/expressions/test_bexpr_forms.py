"""Tests for different expression forms."""

from ._helpers import ExpressionTestCase


class TestBooleanExpressionForms(ExpressionTestCase):

    def test_is_cnf(self):
        """Test CNF form detection."""
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
