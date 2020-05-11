"""Tests for the to_cnf transformation."""

import unittest

from tt.errors import InvalidArgumentTypeError
from tt.expressions import BooleanExpression
from tt.transformations import to_cnf


class TestExpressionToCnf(unittest.TestCase):

    def assert_to_cnf_transformation(self, original, expected):
        """Helper for asserting correct to_cnf transformation."""
        bexpr = to_cnf(original)
        self.assertTrue(bexpr.is_cnf)
        self.assertEqual(expected, str(bexpr))

    def test_invalid_expr_type(self):
        """Test passing an invalid type as the argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            to_cnf(None)

    def test_from_boolean_expression_object(self):
        """Test transformation when passing an expr object as the argument."""
        self.assert_to_cnf_transformation(
            BooleanExpression('A or B'),
            'A or B')

    def test_single_operand_expression(self):
        """Test expressions of single operands."""
        self.assert_to_cnf_transformation('A', 'A')
        self.assert_to_cnf_transformation('0', '0')
        self.assert_to_cnf_transformation('1', '1')

    def test_only_unary_operand_expression(self):
        """Test expressions with only unary operators."""
        self.assert_to_cnf_transformation('not A', 'not A')
        self.assert_to_cnf_transformation('~A', '~A')
        self.assert_to_cnf_transformation('~~A', 'A')
        self.assert_to_cnf_transformation('~~~A', '~A')
        self.assert_to_cnf_transformation('~~~~~~~~~~~~~~~~~~~~~~~~A', 'A')
        self.assert_to_cnf_transformation(
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~A', '~A')

    def test_simple_xor(self):
        """Test simple xor expression."""
        self.assert_to_cnf_transformation(
            'A xor B',
            '(not B or not A) and (A or B)')

    def test_negated_xor(self):
        """Test negated xor expression."""
        self.assert_to_cnf_transformation(
            'not (A xor B)',
            '(not A or B) and (A or not B)')

    def test_simple_xnor(self):
        """Test simple xnor expression."""
        self.assert_to_cnf_transformation(
            'A xnor B',
            '(B or not A) and (A or not B)')

    def test_negated_xnor(self):
        """Test negated xnor expression."""
        self.assert_to_cnf_transformation(
            '~(A xnor B)',
            r'(~A \/ ~B) /\ (A \/ B)')

    def test_simple_impl(self):
        """Test simple implies expression."""
        self.assert_to_cnf_transformation(
            'A -> B',
            r'~A \/ B')

    def test_negated_impl(self):
        """Test negated implies expression."""
        self.assert_to_cnf_transformation(
            '~(A -> B)',
            r'A /\ ~B')

    def test_simple_and(self):
        """Test simple and expression."""
        self.assert_to_cnf_transformation(
            'A and B',
            'A and B')

    def test_negated_and(self):
        """Test negated and expression."""
        self.assert_to_cnf_transformation(
            'not (A and B)',
            'not A or not B')

    def test_simple_nand(self):
        """Test simple nand expression."""
        self.assert_to_cnf_transformation(
            'A nand B',
            'not A or not B')

    def test_negated_nand(self):
        """Test negated nand expression."""
        self.assert_to_cnf_transformation(
            'not (A nand B)',
            'A and B')

    def test_simple_or(self):
        """Test simple or expression."""
        self.assert_to_cnf_transformation(
            'A or B',
            'A or B')

    def test_negated_or(self):
        """Test negated or expression."""
        self.assert_to_cnf_transformation(
            '~(A || B)',
            r'~A /\ ~B')

    def test_simple_nor(self):
        """Test simple nor expression."""
        self.assert_to_cnf_transformation(
            'A nor B',
            'not A and not B')

    def test_negated_nor(self):
        """Test negated nor expression."""
        self.assert_to_cnf_transformation(
            '~(A nor B)',
            r'A \/ B')

    def test_already_cnf_exprs(self):
        """Test expressions that are already in CNF."""
        self.assert_to_cnf_transformation(
            '(A or B) and (C or D) and E',
            '(A or B) and (C or D) and E')
        self.assert_to_cnf_transformation(
            'A or B or C or D or E',
            'A or B or C or D or E')
        self.assert_to_cnf_transformation(
            'A and 1 and B',
            'A and 1 and B')
        self.assert_to_cnf_transformation(
            '(A or B or C or D or E) and (A or B) and 0 and (A or E)',
            '(A or B or C or D or E) and (A or B) and 0 and (A or E)')

    def test_from_dnf(self):
        """Test transforming expressions in DNF."""
        self.assert_to_cnf_transformation(
            '(A and B and C) or (D and E) or (F and G and H)',
            '(A or D or F) and (A or E or F) and (A or D or G) and '
            '(A or E or G) and (A or D or H) and (A or E or H) and '
            '(B or D or F) and (C or D or F) and (B or E or F) and '
            '(C or E or F) and (B or D or G) and (C or D or G) and '
            '(B or E or G) and (C or E or G) and (B or D or H) and '
            '(C or D or H) and (B or E or H) and (C or E or H)')

    def test_mix_of_non_primitive_operators(self):
        """Test expressions combining different non-primitive operators."""
        self.assert_to_cnf_transformation(
            'A xor (B -> C -> D) nand (E iff F)',
            '(not A or ~B or ~C or D or not E or not F) and '
            '(A or B or not E or not F) and '
            '(A or C or not E or not F) and '
            '(A or not D or not E or not F) and '
            '(not A or ~B or ~C or D or E or F) and '
            '(A or B or E or F) and '
            '(A or C or E or F) and '
            '(A or not D or E or F)')
        self.assert_to_cnf_transformation(
            '(A nand B) -> (C nor D) -> (E iff F)',
            r'(A \/ C \/ D \/ F or not E) /\ (A \/ C \/ D \/ E or not F) /\ '
            r'(B \/ C \/ D \/ F or not E) /\ (B \/ C \/ D \/ E or not F)')

    def test_mix_of_primitive_operators(self):
        """Test expressions with mixed primitive operators."""
        self.assert_to_cnf_transformation(
            'A and (B or C and D) and not (C or not D and not E)',
            'A and (B or C) and (B or D) and not C and (D or E)')
        self.assert_to_cnf_transformation(
            '(A and B and C) or not (A and D) or (A and (B or C) or '
            '(D and (E or F)))',
            '(C or not A or not D or B or E or F) and '
            '(B or not A or not D or C or E or F)')

    def test_deeply_nested_mixed_operators(self):
        """Test expressions with deeply nested operators."""
        self.assert_to_cnf_transformation(
            '(A nand (B impl (D or E or F))) iff ~~~(A nor B nor C)',
            '(A or not B) and (A or not C) and '
            '(A or not B or D or E or F) and '
            r'(A \/ not C or not B or D or E or F) and '
            '(not A or B) and (not A or not D) and (not A or not E) and '
            '(not A or not F) and (not A or B or C) and '
            '(not A or not D or B or C) and (not A or not E or B or C) and '
            '(not A or not F or B or C)')
        self.assert_to_cnf_transformation(
            '(A nand ((B or C) iff (D nor E) iff (F or G or H)) nand C) nor D',
            'A and (not B or D or E or not F or not C) and '
            '(not C or D or E or not F) and '
            '(not B or D or E or not G or not C) and '
            '(not C or D or E or not G) and '
            '(not B or D or E or not H or not C) and '
            '(not C or D or E or not H) and '
            '(not B or not D or F or G or H or not C) and '
            '(not C or not D or F or G or H) and '
            '(not B or not E or F or G or H or not C) and '
            '(not C or not E or F or G or H) and not D')

    def test_deeply_nested_primitive_operators(self):
        """Test expressions with deeply nested primitive operators."""
        self.assert_to_cnf_transformation(
            '(A or (B and (C or (D and (E or (F and (G or (H and I))))))))',
            '(A or B) and (A or C or D) and (A or C or E or F) and '
            '(A or C or E or G or H) and (A or C or E or G or I)')
        self.assert_to_cnf_transformation(
            '(((((((((A or B) and C) or D) and E) or F) and G) or H) and I) '
            'or J)',
            '((((A or B or D or F or H or J) and (C or D or F or H or J)) and '
            '(E or F or H or J)) and (G or H or J)) and (I or J)')
        self.assert_to_cnf_transformation(
            '((A and (B or not (C and D)) and E) or (F and G)) and ((A or B) '
            'and (C or (D and E)))',
            '(A or F) and (B or not C or not D or F) and (E or F) and '
            '(A or G) and (B or not C or not D or G) and (E or G) and '
            '(A or B) and (C or D) and (C or E)')
