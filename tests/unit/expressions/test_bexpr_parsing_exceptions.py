"""Tests for handling malformed expressions on initialization."""

from tt.errors import (
    BadParenPositionError,
    EmptyExpressionError,
    ExpressionOrderError,
    InvalidIdentifierError,
    UnbalancedParenError)

from ._helpers import ExpressionTestCase


class TestBooleanExpressionParsingExceptions(ExpressionTestCase):

    def test_empty(self):
        """Test an empty expression."""
        self.helper_test_tokenization_raises(
            '',
            expected_exc_type=EmptyExpressionError)

    def test_all_spaces(self):
        """Test an expression of all spaces."""
        self.helper_test_tokenization_raises(
            '              ',
            expected_exc_type=EmptyExpressionError)

    def test_all_whitespace(self):
        """Test an expression of all whitespace."""
        self.helper_test_tokenization_raises(
            '   \t \t     \t \t     \t',
            expected_exc_type=EmptyExpressionError)

    def test_leading_symbolic_operators(self):
        """Test beginning an expression with a symbolic operator."""
        self.helper_test_tokenization_raises(
            '&&A && B',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=0)

    def test_consecutive_middle_symbolic_operators(self):
        """Test two consecutive binary operators within an expression."""
        self.helper_test_tokenization_raises(
            'A & (| B)',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=5)

    def test_consecutive_trailing_symbolic_operators(self):
        """Test two consecutive binary operators trailing an expression."""
        self.helper_test_tokenization_raises(
            '(A || B) /\\ \\/',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=12)

    def test_leading_plain_english_operators(self):
        """Test beginning an expression with a plain English operator."""
        self.helper_test_tokenization_raises(
            'and and B',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=0)

    def test_consecutive_middle_plain_english_operators(self):
        """Test two consecutive binary operators within an expression."""
        self.helper_test_tokenization_raises(
            '(A or or B)',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=6)

    def test_consecutive_trailing_plain_english_operators(self):
        """Test two consecutive binary operators trailing an expression."""
        self.helper_test_tokenization_raises(
            '((A or B) or C) nand xor',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=21)

    def test_trailing_operator_with_whitespace(self):
        """Test a trailing operator with whitespace trailing it."""
        self.helper_test_tokenization_raises(
            '(A or B) and ',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=9)

    def test_trailing_unary_plain_english_operator(self):
        """Test trailing unary plain English operator."""
        self.helper_test_tokenization_raises(
            'A or B or not C or not',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=19)

    def test_trailing_unary_symbolic_operator(self):
        """Test trailing unary symbolic operator."""
        self.helper_test_tokenization_raises(
            'A NAND B !',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=9)

    def test_single_plain_english_operator(self):
        """Test a single plain English operator."""
        self.helper_test_tokenization_raises(
            'NOT',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=0)

    def test_single_symbolic_operator(self):
        """Test a single symbolic operator."""
        self.helper_test_tokenization_raises(
            '&',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=0)

    def test_consecutive_leading_operands(self):
        """Test consecutive leading operands."""
        self.helper_test_tokenization_raises(
            'operand operand and operand2 or operand3',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=8)

    def test_consecutive_middle_operands(self):
        """Test consecutive operands in the middle of the expression."""
        self.helper_test_tokenization_raises(
            'operand1 or (operand2 operand3) and operand4',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=22)

    def test_consecutive_trailing_operands(self):
        """Test consecutive operands at the end of the expression."""
        self.helper_test_tokenization_raises(
            'op1 or (op2) and op3 op4',
            expected_exc_type=ExpressionOrderError,
            expected_error_pos=21)

    def test_unexpected_left_paren(self):
        """Test an expected left parenthesis."""
        self.helper_test_tokenization_raises(
            'A or (B) ( and C',
            expected_exc_type=BadParenPositionError,
            expected_error_pos=9)

    def test_unexpected_right_paren(self):
        """Test an unexpected right parenthesis."""
        self.helper_test_tokenization_raises(
            'A or B or ) xor C',
            expected_exc_type=BadParenPositionError,
            expected_error_pos=10)

    def test_single_unbalanced_right_paren(self):
        """Test an unbalanced right parenthesis."""
        self.helper_test_tokenization_raises(
            '(A or B))',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=8)

    def test_double_unbalanced_right_paren(self):
        """Test double unbalanced right parentheses."""
        self.helper_test_tokenization_raises(
            '(op1 or op2)))',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=12)

    def test_unbalanced_right_paren_3_to_2_ratio(self):
        """Test 3 right parentheses, unbalanced to 2 left parentheses."""
        self.helper_test_tokenization_raises(
            '(A or B) and ((A or C))) or D',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=23)

    def test_single_unbalanced_left_paren(self):
        """Test an unbalanced left parenthesis."""
        self.helper_test_tokenization_raises(
            '((A or B || C)',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=0)

    def test_double_unbalanced_left_paren(self):
        """Test double unbalanced left parentheses."""
        self.helper_test_tokenization_raises(
            'A or (((B or C))',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=5)

    def test_unbalanced_left_paren_3_to_2_ratio(self):
        """Test 3 left parentheses, unbalanced to 2 right parentheses."""
        self.helper_test_tokenization_raises(
            '(((op1 or (op2 and op3)))',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=0)

    def test_several_unbalanced_left_paren_middle(self):
        """Test several unbalanced left parentheses within an expression."""
        self.helper_test_tokenization_raises(
            '(((A or (((B) or C)))',
            expected_exc_type=UnbalancedParenError,
            expected_error_pos=1)

    def test_empty_paren_scope(self):
        """Test an empty parenthesis scope."""
        self.helper_test_tokenization_raises(
            '()',
            expected_exc_type=BadParenPositionError,
            expected_error_pos=1)

    def test_invalid_symbol_names(self):
        """Test invalid symbol names (invalid chars, keywords, etc.)."""
        self.helper_test_tokenization_raises(
            '$var1 and var2',
            expected_exc_type=InvalidIdentifierError,
            expected_error_pos=0)

        self.helper_test_tokenization_raises(
            'var1 and ^var2',
            expected_exc_type=InvalidIdentifierError,
            expected_error_pos=9)

        self.helper_test_tokenization_raises(
            'for or i',
            expected_exc_type=InvalidIdentifierError,
            expected_error_pos=0)

        self.helper_test_tokenization_raises(
            'A xor (B or while)',
            expected_exc_type=InvalidIdentifierError,
            expected_error_pos=12)

        self.helper_test_tokenization_raises(
            'op1 xor op2 xor False xor 0',
            expected_exc_type=InvalidIdentifierError,
            expected_error_pos=16)
