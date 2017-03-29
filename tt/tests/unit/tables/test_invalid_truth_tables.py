from ._helpers import TruthTableTestCase
from ....errors import (DuplicateSymbolError, ExtraSymbolError,
                        InvalidBooleanValueError, InvalidArgumentTypeError,
                        MissingSymbolError, NoEvaluationVariationError)


class TestInvalidTruthTables(TruthTableTestCase):

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
