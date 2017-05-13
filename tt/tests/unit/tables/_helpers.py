import traceback
import unittest

from tt.tables import TruthTable


class TruthTableTestCase(unittest.TestCase):

    """An extended TestCase with helpers for testing truth tables."""

    def helper_test_truth_table(self, expr, expected_table_str=None, **kwargs):
        """Helper to test the creation of truth tables.

        This helper will fill up a table completely and compare its ``__str__``
        representation with the passed expected string.

        :param expr: The value to pass to the ``TruthTable`` constructor.
        :type expr: BooleanExpression or str

        :param expected_table_str: The expected string representation of the
            table.
        :type expected_table_str: str

        :param kwargs: Keyword args to pass to the ``TruthTable`` constructor.

        """
        t = TruthTable(expr, **kwargs)
        self.assertEqual(expected_table_str, str(t))

    def helper_test_truth_table_fill(self, expr, expected_table_str=None,
                                     init_kwargs={}, **kwargs):
        """Helper to test filling a truth table.

        :param expr: The value to pass to the ``TruthTable`` constructor.
        :type expr: BooleanExpression or str

        :param expected_table_str: The expected string representation of the
            table.
        :type expected_table_str: str

        :param init_kwargs: A dict to pass as the kwargs to the ``TruthTable``
            constructor.
        :type init_kwargs: Dict

        :param kwargs: Keyword args to pass to the fill method.

        """
        t = TruthTable(expr, fill_all=False, **init_kwargs)
        t.fill(**kwargs)
        self.assertEqual(expected_table_str, str(t))

    def helper_test_truth_table_raises(self, expr, expected_exc_type=None,
                                       **kwargs):
        """Helper for testing exception conditions for TruthTable.

        :param expr: The value to pass to the ``TruthTable`` constructor.
        :type expr: BooleanExpression or str

        :param expected_exc_type: The exception type expected to be raised.
        :type expected_exc_type: Exception

        :param  kwargs: Keyword args to pass to the ``TruthTable`` constructor.

        """
        did_catch = False

        try:
            TruthTable(expr, **kwargs)
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

    def helper_test_truth_table_fill_raises(self, expr, expected_exc_type=None,
                                            **kwargs):
        """Helper for testing exception conditions when filling a table.

        :param expr: The value to pass to the ``TruthTable`` constructor.
        :type expr: BooleanExpression or str

        :param expected_exc_type: The exception type expected to be raised.
        :type expected_exc_type: Exception

        :param kwargs: Keyword args to pass to the ``TruthTable`` constructor.

        """
        did_catch = False

        try:
            t = TruthTable(expr, fill_all=False)
            t.fill(**kwargs)
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
