"""Tests for __str__ and __repr__ methods of operators."""

import unittest

from tt.definitions import TT_AND_OP, TT_IMPL_OP


class TestOperatorToString(unittest.TestCase):

    def test_str(self):
        """Simple test of __str__ for a few operators."""
        self.assertEqual('and', str(TT_AND_OP))
        self.assertEqual('impl', str(TT_IMPL_OP))

    def test_repr(self):
        """Simple test of __repr__ for a few operators."""
        self.assertEqual('<BooleanOperator "and">', repr(TT_AND_OP))
        self.assertEqual('<BooleanOperator "impl">', repr(TT_IMPL_OP))
