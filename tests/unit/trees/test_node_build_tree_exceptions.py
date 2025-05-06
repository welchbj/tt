"""Test exceptions that occur in ExpressionTreeNode.build_tree."""

import unittest

from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)
from tt.trees import ExpressionTreeNode


class TestNodeBuildTreeExceptions(unittest.TestCase):

    def test_postfix_tokens_not_a_list(self):
        """Test passing a non-list for postfix_tokens."""
        with self.assertRaises(InvalidArgumentTypeError):
            ExpressionTreeNode.build_tree('should cause an exception')

    def test_postfix_tokens_contains_non_str(self):
        """Test passing a list containing a non-str for postfix_tokens."""
        with self.assertRaises(InvalidArgumentTypeError):
            ExpressionTreeNode.build_tree(['A', 1, 'or'])

    def test_postfix_tokens_empty(self):
        """Test passing an empty list for postfix_tokens."""
        with self.assertRaises(InvalidArgumentValueError):
            ExpressionTreeNode.build_tree([])
