"""Tests for non-grammar exceptions on expression initialization."""

from ._helpers import ExpressionTestCase

from tt.errors import InvalidArgumentTypeError


class TestBooleanExpressionInitExceptions(ExpressionTestCase):

    def test_invalid_expr_type(self):
        """Test passing an invalid type to __init__"""
        self.helper_test_tokenization_raises(
            float(),
            expected_exc_type=InvalidArgumentTypeError)
