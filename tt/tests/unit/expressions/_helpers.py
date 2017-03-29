import traceback
import unittest

from ....expressions import BooleanExpression


class ExpressionTestCase(unittest.TestCase):

    """An extended TestCase with helpers for testing expressions."""

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

    def helper_test_tokenization(self, expr, expected_tokens=None,
                                 expected_postfix_tokens=None,
                                 expected_symbols=None,
                                 expected_tree_str=None):
        """Helper for testing tokenization on valid expressions.

        :param expr: The expression for which to create a new
            ``BooleanExpression`` object, which should be of a valid form.
        :type expr: BooleanExpression

        :param expected_tokens: The list of expected tokens for the passed
            expression.
        :type expected_tokens: List[str]

        :param expected_postfix_tokens: The list of expected postfix tokens for
            the passed expression.
        :type expected_postfix_tokens: List[str]

        :param expected_symbols: The list of expected symbols for the passed
            expression.
        :type expected_symbols: List[str]

        :param expected_tree_str: The expected string representation of the
            constructed expression tree.
        :type expected_tree_str: str

        """
        b = BooleanExpression(expr)
        self.assertEqual(expected_tokens, b.tokens)
        self.assertEqual(expected_postfix_tokens, b.postfix_tokens)
        self.assertEqual(expected_symbols, b.symbols)
        self.assertEqual(expected_tree_str, str(b.tree))

    def helper_test_tokenization_raises(self, expr,
                                        expected_exc_type=None,
                                        expected_error_pos=None):
        """Helper for testing tokenization on invalid expressions.

        :param expr: The expression for which to create a new
            ``BooleanExpression`` object, which should be of a valid form.
        :type expr: str

        :param expected_exc_type: The type of exception expected to be thrown
            during processing of the expression.
        :type expected_exc_type: Exception

        :param expected_error_pos: The position within the expression where the
            troublesome area began; if omitted, this optional argument will not
            be checked on the caught exception.
        :type expected_error_pos: int, optional

        """
        did_catch = False

        try:
            BooleanExpression(expr)
        except expected_exc_type as e:
            if expected_error_pos is not None:
                self.assertEqual(expected_error_pos, e.error_pos)
            did_catch = True
        except Exception as e:
            traceback.print_exc()
            self.fail('Received exception of type ' + type(e).__name__ +
                      ' but was expecting type ' + expected_exc_type.__name__ +
                      '.')
            did_catch = True

        if not did_catch:
            self.fail('No exception thrown.')
