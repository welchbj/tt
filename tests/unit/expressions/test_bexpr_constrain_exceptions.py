"""Tests for exceptions caused in the usage of constrain context manager."""

from tt.errors import (
    AlreadyConstrainedSymbolError,
    ExtraSymbolError,
    InvalidArgumentValueError,
    InvalidBooleanValueError)
from tt.expressions import (
    BooleanExpression)

from ._helpers import ExpressionTestCase


class TestExpressionConstrainExceptions(ExpressionTestCase):

    def test_empty_constraints(self):
        """Test passing no constraints through kwargs."""
        b = BooleanExpression('A or B')
        with self.assertRaises(InvalidArgumentValueError):
            with b.constrain():
                pass

    def test_single_conflicting_nested_constraint(self):
        """Test single conflicting constraint in nested constrain()'s."""
        b = BooleanExpression('A or B')
        with self.assertRaises(AlreadyConstrainedSymbolError) as cm:
            with b.constrain(A=1):
                with b.constrain(A=1):
                    pass

        self.assertIn('Symbol "A"', str(cm.exception))

    def test_multiple_conflicting_constraints(self):
        """Test multiple conflicting constraint in nested constrain()'s."""
        b = BooleanExpression('A xor B xor C')
        with self.assertRaises(AlreadyConstrainedSymbolError) as cm:
            with b.constrain(A=1, B=0, C=1):
                with b.constrain(B=0, A=1):
                    pass

        self.assertIn('Symbols "A", "B"', str(cm.exception))

    def test_deep_conflicting_nested_constraint(self):
        """Test a conflict that occurs in a deeply nested context manager."""
        b = BooleanExpression('A and B and C and D and E')
        with self.assertRaises(AlreadyConstrainedSymbolError) as cm:
            with b.constrain(A=0):
                with b.constrain(B=0):
                    with b.constrain(C=0):
                        with b.constrain(D=0):
                            with b.constrain(E=0):
                                with b.constrain(B=0, D=0, E=1):
                                    pass
        self.assertIn('Symbols "B", "D", "E"', str(cm.exception))

    def test_invalid_symbol(self):
        """Test passing a symbol not present in the expression."""
        b = BooleanExpression('A or B')
        with self.assertRaises(ExtraSymbolError):
            with b.constrain(C=0):
                pass

    def test_invalid_boolean_value(self):
        """Test passing an invalid Boolean value for a constraint."""
        b = BooleanExpression('A or B')
        with self.assertRaises(InvalidBooleanValueError):
            with b.constrain(B='a string'):
                pass
