"""Tests for the evaluation of Boolean expressions."""

import traceback
import unittest

from ...definitions import BOOLEAN_VALUES
from ...errors import (ExtraSymbolError, InvalidBooleanValueError,
                       MissingSymbolError)
from ...expressions import BooleanExpression


class TestEvaluations(unittest.TestCase):

    def helper_test_evaluate(self, expr, expected_result=None, **kwargs):
        """Helper for testing the evaluation of expressions.

        :param expr: The expression to attempt to evaluate.
        :type expr: :class:`str <python:str>`

        :param expected_result: The truthy value expected to be the result of
            evaluation the expression.
        :type expected_result: :class:`bool <python:bool>` or
            :class:`int <python:int>`

        :param kwargs: The values to pass to the ``evaluate`` function.

        """
        b = BooleanExpression(expr)
        result = b.evaluate(**kwargs)
        self.assertEqual(result, expected_result)

    def helper_test_evaluate_raises(self, expr, expected_exc_type=None,
                                    **kwargs):
        """Helper for testing the improper use of the ``evaluate`` function.


        :param expr: The expression to attempt to evaluate.
        :type expr: :class:`str <python:str>`

        :param expected_exc_type: The exception type expected to be raised.
        :type expected_exc_type: Exception

        :param kwargs: The values to pass to the ``evaluate`` function.

        """
        did_catch = False

        try:
            b = BooleanExpression(expr)
            b.evaluate(**kwargs)
        except expected_exc_type as e:
            did_catch = True
        except Exception as e:
            traceback.print_exc()
            self.fail('Received exception of type ' + type(e).__name__ +
                      ' but was expecting type ' + expected_exc_type.__name__ +
                      '.')
            did_catch = True

        if not did_catch:
            self.fail('No exception thrown.')

    def test_single_operand(self):
        """Test evaluating an expression of a single operand."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'operand',
                expected_result=val,
                operand=val)

    def test_negated_single_operand(self):
        """Test evaluating an expression of a single negated operand."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                '!operand',
                expected_result=int(not val),
                operand=val)

    def test_doubly_negated_single_operand(self):
        """Test evaluating an expression that is negated twice.."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'not not op',
                expected_result=val,
                op=val)

    def test_basic_xor(self):
        """Test a basic expression with the Boolean XOR operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A xor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_xnor(self):
        """Test a basic expression with the Boolean XNOR operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A xnor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_and(self):
        """Test a basic expression with the Boolean AND operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A and B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_nand(self):
        """Test a basic expression with the Boolean NAND operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A nand B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_or(self):
        """Test a basic expression with the Boolean OR operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A or B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_nor(self):
        """Test a basic expression with the Boolean NOR operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A nor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_single_constant_value(self):
        """Test an expression of only a single constant value."""
        self.helper_test_evaluate(
            '0',
            expected_result=0)

        self.helper_test_evaluate(
            '1',
            expected_result=1)

    def test_several_constant_values(self):
        """Test an expression of several constant values."""
        self.helper_test_evaluate(
            '(1 xor (0 or 1)) and 1',
            expected_result=0)

    def test_simple_mixed_constant_variable(self):
        """Test a simple expression mixing constant values and variables."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'operand xnor 1',
                expected_result=int(val == 1),
                operand=val)

            self.helper_test_evaluate(
                'operand xnor 0',
                expected_result=int(val == 0),
                operand=val)

    def test_mixed_constant_variable(self):
        """Test a non-trivial mix of constant values and variables."""
        self.helper_test_evaluate(
            '(A or (not(A and B) nand C)) and 1',
            expected_result=1,
            A=0,
            B=1,
            C=0)

    def test_missing_single_token(self):
        """Test attempting to evaluate without passing a token value."""
        self.helper_test_evaluate_raises(
            'A or (B and (C and not D))',
            expected_exc_type=MissingSymbolError,
            A=0,
            B=1,
            D=1)

    def test_missing_multiple_tokens(self):
        """Test attempting to evaluate without passing token values."""
        self.helper_test_evaluate_raises(
            'A or (B and (C and not D))',
            expected_exc_type=MissingSymbolError,
            A=0,
            D=1)

    def test_missing_all_tokens(self):
        """Test attempting to evaluate without passing any token values."""
        self.helper_test_evaluate_raises(
            '(A nand B) and not D',
            expected_exc_type=MissingSymbolError)

    def test_single_extra_token(self):
        """Test attempting to pass a single token not in the expression."""
        self.helper_test_evaluate_raises(
            'A and not B',
            expected_exc_type=ExtraSymbolError,
            A=1,
            B=1,
            C=0)

    def test_several_extra_tokens(self):
        """Test attempting to pass several tokens not in the expression."""
        self.helper_test_evaluate_raises(
            'A or B or C',
            expected_exc_type=ExtraSymbolError,
            A=0,
            B=0,
            C=0,
            D=0,
            E=0)

    def test_all_extra_tokens(self):
        """Test attempting to pass all tokens not in the expression."""
        self.helper_test_evaluate_raises(
            '1 or 0',
            expected_exc_type=ExtraSymbolError,
            A=1,
            B=1,
            C=1)

    def test_invalid_boolean_value(self):
        """Test passing an invalid Boolean value."""
        self.helper_test_evaluate_raises(
            'A or B',
            expected_exc_type=InvalidBooleanValueError,
            A=1,
            B=2)
