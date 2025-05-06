"""Test __str__ and __repr__ for expressions."""

import unittest

from tt.expressions import BooleanExpression


class TestExpressiontoString(unittest.TestCase):

    def test_str(self):
        """Test the expression __str__ implementation."""
        b = BooleanExpression('(A or B) nand C')
        self.assertEqual(str(b), '(A or B) nand C')

    def test_repr(self):
        """Test the expression __repr__ implementation."""
        b = BooleanExpression('A -> B -> C -> D')
        self.assertEqual(repr(b), '<BooleanExpression "A -> B -> C -> D">')
