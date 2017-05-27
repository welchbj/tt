"""Tests for the to_primitives transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import to_primitives


class TestToPrimitives(unittest.TestCase):

    def assert_to_primitives_tranformation(self, original, expected):
        """Helper for asserting correct to_primitives transformation."""
        self.assertEqual(expected, str(to_primitives(original)))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as the argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            to_primitives(None)

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_to_primitives_tranformation(
            BooleanExpression('A and B'),
            'A and B')

    def test_compound_plain_english_expression(self):
        """Test a compound expression of only plain English operators."""
        self.assert_to_primitives_tranformation(
            '((A impl B) iff (C nand D)) or not not not (E xor F)',
            '(((not A or B) and (not C or not D)) or (not (not A or B) and '
            'not (not C or not D))) or not not not ((E and not F) or '
            '(not E and F))')

    def test_compound_symbolic_expression(self):
        """Test a compound expression of only symbolic operators."""
        self.assert_to_primitives_tranformation(
            '(A <-> B) -> C -> ~~~(A && !D) <-> ~!~(((E)))',
            '~((A & B) | (~A & ~B)) | (~C | (~~~(A & !D) & ~!~E) | '
            '(~~~~(A & !D) & ~~!~E))')

    def test_compound_mixed_expression(self):
        """Test an expression of mixed symbolic and plain English operators."""
        self.assert_to_primitives_tranformation(
            '~(A and B) -> (C or D || (E /\\ F)) nor (G xor H)',
            'not (~~(A and B) | (C or D | (E & F))) and not ((G and not H) or '
            '(not G and H))')
