"""Tests for valid truth table filling."""

from ._helpers import TruthTableTestCase


class TestTruthTableFill(TruthTableTestCase):

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
