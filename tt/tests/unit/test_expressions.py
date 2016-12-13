"""Tests for tokenization/parsing of Boolean expressions."""

import unittest
import traceback

from ...expressions import (BadParenPositionError, BooleanExpression,
                            ExpressionOrderError, UnbalancedParenError)
from ...operators import OPERATOR_MAPPING, TT_NOT_OP


class TestExpressions(unittest.TestCase):

    """Tests for Boolean expressions, namely the BooleanExpression class."""

    def helper_test_tokenization(self, expr, expected_tokens=None,
                                 expected_postfix_tokens=None,
                                 expected_symbols=None):
        """Helper for testing tokenization on valid expressions.

        Args:
            expr (str): The expression for which to create a new
                ``BooleanExpression`` object, which should be of a valid
                form.
            expected_tokens (List[str]): The list of expected tokens for the
                passed expression.
            expected_symbols (List[str]): The list of expected symbols for the
                passed expression.

        """
        b = BooleanExpression(expr)
        self.assertEqual(expected_tokens, b.tokens)
        self.assertEqual(expected_postfix_tokens, b.postfix_tokens)
        self.assertEqual(expected_symbols, b.symbols)

    def helper_test_tokenization_raises(self, expr,
                                        expected_exc_type=None,
                                        expected_error_pos=None):
        """Helper for testing tokenization on invalid expressions.

        Args:
            expr (str): The expression for which to create a new
                ``BooleanExpression`` object, which should be of a valid
                form.
            expected_exc_type (Exception): The type of exception expected to be
                thrown during processing of the expression.
            expected_error_pos (int, optional): The position within the
                expression where the troublesome area began; if omitted, this
                optional argument will not be checked on the caught exception.

        """
        did_catch = False

        try:
            BooleanExpression(expr)
        except expected_exc_type as e:
            if expected_error_pos is not None:
                self.assertEqual(expected_error_pos, e.error_pos)
            did_catch = True
        except Exception as e:
            traceback.print_exception(e)
            self.fail('Received exception of type ' + type(e).__name__ +
                      ' but was expecting type ' + expected_exc_type.__name__ +
                      '.')
            did_catch = True

        if not did_catch:
            self.fail('No exception thrown.')

    def test_all_binary_operators(self):
        """Basic test for all binary operators, to ensure correct parsing."""
        binary_ops = [k for k, v in OPERATOR_MAPPING.items() if v != TT_NOT_OP]

        for op in binary_ops:
            self.helper_test_tokenization(
                '(A {0} ((B {0} C) {0} D)) {0} E'.format(op),
                expected_tokens=['(', 'A', op, '(', '(', 'B', op, 'C', ')', op, 'D',
                                 ')', ')', op, 'E'],
                expected_postfix_tokens=['A', 'B', 'C', op, 'D', op, op, 'E',
                                         op],
                expected_symbols=['A', 'B', 'C', 'D', 'E'])

    def test_empty(self):
        """Test an empty expression."""
        self.helper_test_tokenization(
            '',
            expected_tokens=[],
            expected_postfix_tokens=[],
            expected_symbols=[])

    def test_single_symbol(self):
        """Test an expression of a single variable."""
        self.helper_test_tokenization(
            'operand',
            expected_tokens=['operand'],
            expected_postfix_tokens=['operand'],
            expected_symbols=['operand'])

    def test_single_character_symbol(self):
        """Test an expression containing only an operand of one character."""
        self.helper_test_tokenization(
            'a',
            expected_tokens=['a'],
            expected_postfix_tokens=['a'],
            expected_symbols=['a'])

    def test_single_constant(self):
        """Test an expression only containing a constant."""
        self.helper_test_tokenization(
            '0',
            expected_tokens=['0'],
            expected_postfix_tokens=['0'],
            expected_symbols=[])

    def test_only_constants_symbolic_operators(self):
        """Test an expression of only constants and symbolic operators."""
        self.helper_test_tokenization(
            '(!0&&1||(~~0||~~1))&&((0\\/1)/\\!0)',
            expected_tokens=['(', '!', '0', '&&', '1', '||', '(', '~', '~',
                             '0', '||', '~', '~', '1', ')', ')', '&&', '(',
                             '(', '0', '\\/', '1', ')', '/\\', '!', '0', ')'],
            expected_postfix_tokens=['0', '!', '1', '&&', '0', '~', '~', '1',
                                     '~', '~', '||', '||', '0', '1', '\\/',
                                     '0', '!', '/\\', '&&'],
            expected_symbols=[])

    def test_only_constants_plain_english_operators(self):
        """Test an expression of only constants and plain English operators."""
        self.helper_test_tokenization(
            'not 0 and 1 or (not not 0 or not not 1) and 0 or 1 and 0',
            expected_tokens=['not', '0', 'and', '1', 'or', '(', 'not', 'not',
                             '0', 'or', 'not', 'not', '1', ')', 'and', '0',
                             'or', '1', 'and', '0'],
            expected_postfix_tokens=['0', 'not', '1', 'and', '0', 'not', 'not',
                                     '1', 'not', 'not', 'or', '0', 'and', '1',
                                     '0', 'and', 'or', 'or'],
            expected_symbols=[])

    def test_superfluous_parentheses_symbolic_operators(self):
        """Test symbolic operators with unnecessary parentheses."""
        self.helper_test_tokenization(
            '((A)||(B))&&(C)',
            expected_tokens=['(', '(', 'A', ')', '||', '(', 'B', ')', ')',
                             '&&', '(', 'C', ')'],
            expected_postfix_tokens=['A', 'B', '||', 'C', '&&'],
            expected_symbols=['A', 'B', 'C'])

    def test_superfluous_parentheses_plain_english_operators(self):
        """Test plain English operators with unnecessary parentheses."""
        self.helper_test_tokenization(
            '((A)and(B))or(C)',
            expected_tokens=['(', '(', 'A', ')', 'and', '(', 'B', ')', ')',
                             'or', '(', 'C', ')'],
            expected_postfix_tokens=['A', 'B', 'and', 'C', 'or'],
            expected_symbols=['A', 'B', 'C'])

    def test_symbolic_operators_without_spaces(self):
        """Test using symbolic operators without spaces before operands."""
        self.helper_test_tokenization(
            '(A&&B||(C&D))|(!E\\/(~F))',
            expected_tokens=['(', 'A', '&&', 'B', '||', '(', 'C', '&', 'D',
                             ')', ')', '|', '(', '!', 'E', '\\/', '(', '~',
                             'F', ')', ')'],
            expected_postfix_tokens=['A', 'B', '&&', 'C', 'D', '&', '||', 'E',
                                     '!', 'F', '~', '\\/', '|'],
            expected_symbols=['A', 'B', 'C', 'D', 'E', 'F'])

    def test_several_nots(self):
        """Test several consecutive unary not operators."""
        self.helper_test_tokenization(
            '~!~!! not not ~ !!!! operand',
            expected_tokens=['~', '!', '~', '!', '!', 'not', 'not', '~', '!',
                             '!', '!', '!', 'operand'],
            expected_postfix_tokens=['operand', '!', '!', '!', '!', '~', 'not',
                                     'not', '!', '!', '~', '!', '~'],
            expected_symbols=['operand'])

    def test_concentric_parentheses(self):
        """Test many grouped parentheses."""
        self.helper_test_tokenization(
            '(((op1)))and(((((op2)))))or(1)',
            expected_tokens=['(', '(', '(', 'op1', ')', ')', ')', 'and',
                             '(', '(', '(', '(', '(', 'op2', ')', ')', ')',
                             ')', ')', 'or', '(', '1', ')'],
            expected_postfix_tokens=['op1', 'op2', 'and', '1', 'or'],
            expected_symbols=['op1', 'op2'])

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
