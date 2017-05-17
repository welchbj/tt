"""Helpers for testing expression trees and nodes."""

import unittest

from tt.expressions import BooleanExpression


class ExpressionTreeAndNodeTestCase(unittest.TestCase):

    def get_tree_root_from_expr_str(self, expr_str):
        """Get an tree root node from an expression string."""
        return BooleanExpression(expr_str).tree.root
