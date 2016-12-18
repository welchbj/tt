"""Tests for TruthTable."""

import unittest
import traceback

from ...errors import (DuplicateSymbolError, ExtraSymbolError,
                       InvalidBooleanValueError, InvalidArgumentTypeError,
                       MissingSymbolError, NoEvaluationVariationError)
from ...expressions import BooleanExpression
from ...tables import TruthTable


class TestTruthTable(unittest.TestCase):

    def helper_test_truth_table(self, expr, expected_table_str=None, **kwargs):
        """Helper to test the creation of truth tables.

        This helper will fill up a table completely and compare its ``__str__``
        representation with the passed expected string.

        Args:
            expr: The value to pass to the ``TruthTable`` constructor.
            expected_table_str (str): The expected string representation of the
                table.
            **kwargs: Keyword args to pass to the ``TruthTable`` constructor.

        """
        t = TruthTable(expr, **kwargs)
        self.assertEqual(expected_table_str, str(t))

    def helper_test_truth_table_fill(self, expr, expected_table_str=None,
                                     init_kwargs={}, **kwargs):
        """Helper to test filling a truth table.

        Args:
            expr: The value to pass to the ``TruthTable`` constructor.
            expected_table_str (str): The expected string representation of the
                table.
            init_kwargs (dict): A dict to pass as the kwargs to the
                ``TruthTable`` constructor.
            **kwargs: Keyword args to pass to the fill method.

        """
        t = TruthTable(expr, fill_all=False, **init_kwargs)
        t.fill(**kwargs)
        self.assertEqual(expected_table_str, str(t))

    def helper_test_truth_table_raises(self, expr, expected_exc_type=None,
                                       **kwargs):
        """Helper for testing exception conditions for TruthTable.

        Args:
            expr: The value to pass to the ``TruthTable`` constructor.
            expected_exc_type (Exception): The exception type expected to be
                raised.
            **kwargs: Keyword args to pass to the ``TruthTable`` constructor.

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

        Args:
            expr: The value to pass to the ``TruthTable`` constructor.
            expected_exc_type (Exception): The exception type expected to be
                raised.
            **kwargs: Keyword args to pass to the ``TruthTable`` constructor.

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

    def test_single_operand_single_char(self):
        """Test an expression of a single operand of one character."""
        self.helper_test_truth_table(
            'A',
            expected_table_str='\n'.join((
                '+---+---+',
                '| A |   |',
                '+---+---+',
                '| 0 | 0 |',
                '+---+---+',
                '| 1 | 1 |',
                '+---+---+'
            )))

    def test_from_expression_object(self):
        """Test creating a truth table from an existing expression object."""
        self.helper_test_truth_table(
            BooleanExpression('A'),
            expected_table_str='\n'.join((
                '+---+---+',
                '| A |   |',
                '+---+---+',
                '| 0 | 0 |',
                '+---+---+',
                '| 1 | 1 |',
                '+---+---+'
            )))

    def test_single_operand_multiple_chars(self):
        """Test an expression of a single operand of several characters."""
        self.helper_test_truth_table(
            'operand',
            expected_table_str='\n'.join((
                '+---------+---+',
                '| operand |   |',
                '+---------+---+',
                '|    0    | 0 |',
                '+---------+---+',
                '|    1    | 1 |',
                '+---------+---+'
            )))

    def test_simple_expression_varying_operand_lengths(self):
        """Test a simple expression with varying operand lengths."""
        self.helper_test_truth_table(
            'operand and not another_operand',
            expected_table_str='\n'.join((
                '+---------+-----------------+---+',
                '| operand | another_operand |   |',
                '+---------+-----------------+---+',
                '|    0    |        0        | 0 |',
                '+---------+-----------------+---+',
                '|    0    |        1        | 0 |',
                '+---------+-----------------+---+',
                '|    1    |        0        | 1 |',
                '+---------+-----------------+---+',
                '|    1    |        1        | 0 |',
                '+---------+-----------------+---+'
            )))

    def test_simple_three_operand(self):
        """Test a simple expression of three operands."""
        self.helper_test_truth_table(
            'A or (AB xor ABC)',
            expected_table_str='\n'.join((
                '+---+----+-----+---+',
                '| A | AB | ABC |   |',
                '+---+----+-----+---+',
                '| 0 | 0  |  0  | 0 |',
                '+---+----+-----+---+',
                '| 0 | 0  |  1  | 1 |',
                '+---+----+-----+---+',
                '| 0 | 1  |  0  | 1 |',
                '+---+----+-----+---+',
                '| 0 | 1  |  1  | 0 |',
                '+---+----+-----+---+',
                '| 1 | 0  |  0  | 1 |',
                '+---+----+-----+---+',
                '| 1 | 0  |  1  | 1 |',
                '+---+----+-----+---+',
                '| 1 | 1  |  0  | 1 |',
                '+---+----+-----+---+',
                '| 1 | 1  |  1  | 1 |',
                '+---+----+-----+---+'
            )))

    def test_ordering_single_operand(self):
        """Test specifying the ordering for a single operand."""
        self.helper_test_truth_table(
            'operand',
            ordering=['operand'],
            expected_table_str='\n'.join((
                '+---------+---+',
                '| operand |   |',
                '+---------+---+',
                '|    0    | 0 |',
                '+---------+---+',
                '|    1    | 1 |',
                '+---------+---+'
            )))

    def test_ordering_two_operands(self):
        """Test specifying the ordering for two operands."""
        base = '\n'.join((
            '+---+---+---+',
            '| {} | {} |   |',
            '+---+---+---+',
            '| 0 | 0 | 1 |',
            '+---+---+---+',
            '| 0 | 1 | 1 |',
            '+---+---+---+',
            '| 1 | 0 | 1 |',
            '+---+---+---+',
            '| 1 | 1 | 0 |',
            '+---+---+---+'
        ))

        self.helper_test_truth_table(
            'A nand B',
            ordering=['A', 'B'],
            expected_table_str=base.format('A', 'B'))

        self.helper_test_truth_table(
            'A nand B',
            ordering=['B', 'A'],
            expected_table_str=base.format('B', 'A'))

    def test_ordering_three_operands(self):
        """Test specifying the ordering for three operands."""
        base = '\n'.join((
            '+---+---+---+---+',
            '| {} | {} | {} |   |',
            '+---+---+---+---+',
            '| 0 | 0 | 0 | 0 |',
            '+---+---+---+---+',
            '| 0 | 0 | 1 | 1 |',
            '+---+---+---+---+',
            '| 0 | 1 | 0 | 1 |',
            '+---+---+---+---+',
            '| 0 | 1 | 1 | 1 |',
            '+---+---+---+---+',
            '| 1 | 0 | 0 | 1 |',
            '+---+---+---+---+',
            '| 1 | 0 | 1 | 1 |',
            '+---+---+---+---+',
            '| 1 | 1 | 0 | 1 |',
            '+---+---+---+---+',
            '| 1 | 1 | 1 | 1 |',
            '+---+---+---+---+'
        ))

        self.helper_test_truth_table(
            'A or B or C',
            ordering=['A', 'B', 'C'],
            expected_table_str=base.format('A', 'B', 'C'))

        self.helper_test_truth_table(
            'A or B or C',
            ordering=['C', 'B', 'A'],
            expected_table_str=base.format('C', 'B', 'A'))

        self.helper_test_truth_table(
            'A or B or C',
            ordering=['B', 'C', 'A'],
            expected_table_str=base.format('B', 'C', 'A'))

    def test_fill_single_operand(self):
        """Test fill with only a single operand."""
        self.helper_test_truth_table_fill(
            'A',
            A=0,
            expected_table_str='\n'.join((
                '+---+---+',
                '| A |   |',
                '+---+---+',
                '| 0 | 0 |',
                '+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A',
            A=1,
            expected_table_str='\n'.join((
                '+---+---+',
                '| A |   |',
                '+---+---+',
                '| 1 | 1 |',
                '+---+---+'
            )))

    def test_fill_two_operands(self):
        """Test fill with two operands."""
        self.helper_test_truth_table_fill(
            'A xor B',
            A=1,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 1 | 0 | 1 |',
                '+---+---+---+',
                '| 1 | 1 | 0 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            init_kwargs={'ordering': ['B', 'A']},
            A=1,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| B | A |   |',
                '+---+---+---+',
                '| 0 | 1 | 1 |',
                '+---+---+---+',
                '| 1 | 1 | 0 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            A=0,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 0 | 0 | 0 |',
                '+---+---+---+',
                '| 0 | 1 | 1 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            init_kwargs={'ordering': ['B', 'A']},
            A=0,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| B | A |   |',
                '+---+---+---+',
                '| 0 | 0 | 0 |',
                '+---+---+---+',
                '| 1 | 0 | 1 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            B=0,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 0 | 0 | 0 |',
                '+---+---+---+',
                '| 1 | 0 | 1 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            B=1,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 0 | 1 | 1 |',
                '+---+---+---+',
                '| 1 | 1 | 0 |',
                '+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            A=0,
            B=1,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 0 | 1 | 1 |',
                '+---+---+---+',
            )))

        self.helper_test_truth_table_fill(
            'A xor B',
            init_kwargs={'ordering': ['B', 'A']},
            A=0,
            B=1,
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| B | A |   |',
                '+---+---+---+',
                '| 1 | 0 | 1 |',
                '+---+---+---+',
            )))

    def test_fill_three_operands(self):
        """Test fill with three operands."""
        self.helper_test_truth_table_fill(
            'A and (B or C)',
            A=0,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 0 | 0 | 0 | 0 |',
                '+---+---+---+---+',
                '| 0 | 0 | 1 | 0 |',
                '+---+---+---+---+',
                '| 0 | 1 | 0 | 0 |',
                '+---+---+---+---+',
                '| 0 | 1 | 1 | 0 |',
                '+---+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A and (B or C)',
            A=1,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 1 | 0 | 0 | 0 |',
                '+---+---+---+---+',
                '| 1 | 0 | 1 | 1 |',
                '+---+---+---+---+',
                '| 1 | 1 | 0 | 1 |',
                '+---+---+---+---+',
                '| 1 | 1 | 1 | 1 |',
                '+---+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A and (B or C)',
            B=1,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 0 | 1 | 0 | 0 |',
                '+---+---+---+---+',
                '| 0 | 1 | 1 | 0 |',
                '+---+---+---+---+',
                '| 1 | 1 | 0 | 1 |',
                '+---+---+---+---+',
                '| 1 | 1 | 1 | 1 |',
                '+---+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A and (B or C)',
            C=0,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 0 | 0 | 0 | 0 |',
                '+---+---+---+---+',
                '| 0 | 1 | 0 | 0 |',
                '+---+---+---+---+',
                '| 1 | 0 | 0 | 0 |',
                '+---+---+---+---+',
                '| 1 | 1 | 0 | 1 |',
                '+---+---+---+---+',
            )))

        self.helper_test_truth_table_fill(
            'A and (B or C)',
            A=1,
            B=1,
            C=1,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 1 | 1 | 1 | 1 |',
                '+---+---+---+---+'
            )))

        self.helper_test_truth_table_fill(
            'A and (B or C)',
            init_kwargs={'ordering': ['B', 'C', 'A']},
            A=0,
            B=1,
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| B | C | A |   |',
                '+---+---+---+---+',
                '| 1 | 0 | 0 | 0 |',
                '+---+---+---+---+',
                '| 1 | 1 | 0 | 0 |',
                '+---+---+---+---+',
            )))

    def test_invalid_expr_type(self):
        """Test passing an invalid expression type to TruthTable."""
        self.helper_test_truth_table_raises(
            None,
            expected_exc_type=InvalidArgumentTypeError)

    def test_only_constant_values(self):
        """Test an expression of only constant values."""
        self.helper_test_truth_table_raises(
            '0 nand (1 or 0)',
            expected_exc_type=NoEvaluationVariationError)

    def test_ordering_missing_symbols(self):
        """Test passing too few symbols in the symbol ordering."""
        self.helper_test_truth_table_raises(
            'A or B or C',
            ordering=['A', 'C'],
            expected_exc_type=MissingSymbolError)

    def test_ordering_extra_symbols(self):
        """Test passing extra symbols in the symbol ordering."""
        self.helper_test_truth_table_raises(
            'A nand (B or D)',
            ordering=['A', 'B', 'C', 'D'],
            expected_exc_type=ExtraSymbolError)

    def test_ordering_duplicate_symbols(self):
        """Test passing duplicate symbols in the symbol ordernig."""
        self.helper_test_truth_table_raises(
            '(A nand B) or C',
            ordering=['A', 'B', 'B', 'C'],
            expected_exc_type=DuplicateSymbolError)

    def test_fill_invalid_symbol(self):
        """Test passing an non-existent symbol in the fill method."""
        self.helper_test_truth_table_fill_raises(
            '(op1 xor op2) and op3',
            op4=True,
            expected_exc_type=ExtraSymbolError)

    def test_fill_invalid_boolean_value(self):
        """Test passing an invalid Boolean value to the fill method."""
        self.helper_test_truth_table_fill_raises(
            'A or B',
            A=-1,
            expected_exc_type=InvalidBooleanValueError)
