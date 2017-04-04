"""Tests for valid truth table initializaton."""

from ._helpers import TruthTableTestCase
from ....expressions import BooleanExpression


class TestTruthTableInit(TruthTableTestCase):

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

    def test_truth_table_from_values_with_specified_ordering(self):
        """Test creating a truth table with specified values and ordering."""
        self.helper_test_truth_table(
            None,
            from_values='x1',
            ordering=['H'],
            expected_table_str='\n'.join((
                '+---+---+',
                '| H |   |',
                '+---+---+',
                '| 0 | x |',
                '+---+---+',
                '| 1 | 1 |',
                '+---+---+',
            )))

        self.helper_test_truth_table(
            None,
            from_values='0xx1',
            ordering=['C', 'B'],
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| C | B |   |',
                '+---+---+---+',
                '| 0 | 0 | 0 |',
                '+---+---+---+',
                '| 0 | 1 | x |',
                '+---+---+---+',
                '| 1 | 0 | x |',
                '+---+---+---+',
                '| 1 | 1 | 1 |',
                '+---+---+---+',
            )))

    def test_auto_gen_of_symbols_from_values_small_tables(self):
        """Test auto-generation of symbols when using from_values."""
        self.helper_test_truth_table(
            None,
            from_values='10',
            expected_table_str='\n'.join((
                '+---+---+',
                '| A |   |',
                '+---+---+',
                '| 0 | 1 |',
                '+---+---+',
                '| 1 | 0 |',
                '+---+---+',
            )))

        self.helper_test_truth_table(
            None,
            from_values='10x1',
            expected_table_str='\n'.join((
                '+---+---+---+',
                '| A | B |   |',
                '+---+---+---+',
                '| 0 | 0 | 1 |',
                '+---+---+---+',
                '| 0 | 1 | 0 |',
                '+---+---+---+',
                '| 1 | 0 | x |',
                '+---+---+---+',
                '| 1 | 1 | 1 |',
                '+---+---+---+',
            )))

        self.helper_test_truth_table(
            None,
            from_values='xx10xx00',
            expected_table_str='\n'.join((
                '+---+---+---+---+',
                '| A | B | C |   |',
                '+---+---+---+---+',
                '| 0 | 0 | 0 | x |',
                '+---+---+---+---+',
                '| 0 | 0 | 1 | x |',
                '+---+---+---+---+',
                '| 0 | 1 | 0 | 1 |',
                '+---+---+---+---+',
                '| 0 | 1 | 1 | 0 |',
                '+---+---+---+---+',
                '| 1 | 0 | 0 | x |',
                '+---+---+---+---+',
                '| 1 | 0 | 1 | x |',
                '+---+---+---+---+',
                '| 1 | 1 | 0 | 0 |',
                '+---+---+---+---+',
                '| 1 | 1 | 1 | 0 |',
                '+---+---+---+---+',
            )))
