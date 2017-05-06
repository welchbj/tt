"""Test tree exceptions that occur during initialization."""

import unittest

from tt.errors import InvalidArgumentTypeError, InvalidArgumentValueError
from tt.trees import BooleanExpressionTree


class TestTreeInitExceptions(unittest.TestCase):

    def test_postfix_tokens_not_a_list(self):
        """Test passing a non-list for postfix_tokens."""
        with self.assertRaises(InvalidArgumentTypeError):
            BooleanExpressionTree('should cause an exception')

    def test_postfix_tokens_contains_non_str(self):
        """Test passing a list containing a non-str for postfix_tokens."""
        with self.assertRaises(InvalidArgumentTypeError):
            BooleanExpressionTree(['A', 1, 'or'])

    def test_postfix_tokens_empty(self):
        """Test passing an empty list for postfix_tokens."""
        with self.assertRaises(InvalidArgumentValueError):
            BooleanExpressionTree([])
