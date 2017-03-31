from ._helpers import TruthTableTestCase
from ....errors import (AlreadyFullTableError, ConflictingArgumentsError,
                        DuplicateSymbolError, ExtraSymbolError,
                        InvalidArgumentValueError, InvalidBooleanValueError,
                        InvalidArgumentTypeError, MissingSymbolError,
                        NoEvaluationVariationError, RequiredArgumentError)
from ....tables import TruthTable


class TestInvalidTruthTables(TruthTableTestCase):

    def test_invalid_expr_type(self):
        """Test passing an invalid expression type to TruthTable."""
        self.helper_test_truth_table_raises(
            float(),
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

    def test_specify_both_expr_and_from_values(self):
        """Test specifying both an expression and starting values."""
        self.helper_test_truth_table_raises(
            'A or B',
            from_values='001x',
            expected_exc_type=ConflictingArgumentsError)

    def test_specify_neither_expr_or_from_values(self):
        """Test specifying neither the expression or starting values."""
        self.helper_test_truth_table_raises(
            None,
            from_values=None,
            expected_exc_type=RequiredArgumentError)

    def test_from_values_invalid_type(self):
        """Test passing an invalid type for the from_values argument."""
        self.helper_test_truth_table_raises(
            float(),
            expected_exc_type=InvalidArgumentTypeError)

    def test_from_values_invalid_str_value(self):
        """Test passing an invalid Boolean/don't care within from_values."""
        self.helper_test_truth_table_raises(
            None,
            from_values='00_0',
            expected_exc_type=InvalidBooleanValueError)

    def test_from_values_ordering_not_list(self):
        """Test passing a non-list as the ordering argument."""
        self.helper_test_truth_table_raises(
            None,
            from_values='1110',
            ordering=3,
            expected_exc_type=InvalidArgumentTypeError)

    def test_from_values_list_non_string(self):
        """Test passing a list of non-strings as the ordering argument."""
        self.helper_test_truth_table_raises(
            None,
            from_values='0000',
            ordering=[1, 2],
            expected_exc_type=InvalidArgumentTypeError)

    def test_from_values_empty_ordering(self):
        """Test passing an empty ordering list."""
        self.helper_test_truth_table_raises(
            None,
            from_values='0000',
            ordering=[],
            expected_exc_type=InvalidArgumentValueError)

    def test_empty_str_from_values(self):
        """Test an empty string for from_values."""
        self.helper_test_truth_table_raises(
            None,
            from_values='',
            expected_exc_type=InvalidArgumentValueError)

    def test_non_pow_2_from_values(self):
        """Test passing a non-power-of-2 number of input values."""
        self.helper_test_truth_table_raises(
            None,
            from_values='01x',
            expected_exc_type=InvalidArgumentValueError)

    def test_too_few_symbols_provided_from_values(self):
        """Test passing in too few symbols for the specified from_values."""
        self.helper_test_truth_table_raises(
            None,
            from_values='1010',
            ordering=['A'],
            expected_exc_type=MissingSymbolError)

    def test_too_many_symbols_provided_from_values(self):
        """Test passing in too few symbols for the specified from_values."""
        self.helper_test_truth_table_raises(
            None,
            from_values='1010',
            ordering=['A', 'B', 'C'],
            expected_exc_type=ExtraSymbolError)

    def test_attempt_to_fill_table_already_filled_from_values(self):
        """Ensure that we cannot fill() a table built from specified values."""
        t = TruthTable(from_values='xxxx', ordering=['A', 'B'])
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=1)

    def test_attempt_to_fill_table_already_filled_on_init_from_expr(self):
        """Ensure that we cannot fill a table already filled from an expr."""
        t = TruthTable('A or B')
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=0)

    def test_attempt_to_fill_table_already_iteratively_filled(self):
        """Ensure that we cannot fill a table already iteratively filled."""
        t = TruthTable('A nand B', fill_all=False)
        t.fill(A=0)
        t.fill(A=1)
        with self.assertRaises(AlreadyFullTableError):
            t.fill(A=0)
