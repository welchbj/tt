"""Tests for expression evaluation exceptions."""

from tt.errors import (
    ExtraSymbolError,
    InvalidBooleanValueError,
    MissingSymbolError)

from ._helpers import ExpressionTestCase


class TestBooleanExpressionEvaluationExceptions(ExpressionTestCase):

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
