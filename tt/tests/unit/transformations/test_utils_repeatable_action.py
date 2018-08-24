"""Tests for the RepeatableAction class."""

import unittest

from tt.errors import (
    InvalidArgumentValueError)
from tt.transformations import (
    forever,
    RepeatableAction)


class TestUtilsRepeatableAction(unittest.TestCase):

    def test_invalid_times(self):
        """Test attempting to init with an invalid number of times."""
        with self.assertRaises(InvalidArgumentValueError):
            RepeatableAction(0)

        class _AlwaysLessThan(object):
            def __lt__(self, other):
                return True

        with self.assertRaises(InvalidArgumentValueError):
            RepeatableAction(_AlwaysLessThan())

    def test_comparing_objects(self):
        """Test comparing two instances."""
        r1 = RepeatableAction(1)
        r2 = RepeatableAction(50)
        r3 = forever
        self.assertTrue(r1 < r2 < r3)
        self.assertTrue(r1 <= r2 <= r3)
        self.assertTrue(r3 > r2 > r1)
        self.assertTrue(r3 >= r2 >= r1)

    def test_str_methods(self):
        """Test the __str__ and __repr__ magic methods."""
        r = RepeatableAction(44)
        self.assertEqual(str(r), '44 times')
        self.assertEqual(repr(r), '<RepeatableAction [44 times]>')

        r = RepeatableAction(1)
        self.assertEqual(str(r), '1 time')
        self.assertEqual(repr(r), '<RepeatableAction [1 time]>')

        f = forever
        self.assertEqual(str(f), 'inf times')
        self.assertEqual(repr(f), '<RepeatableAction [inf times]>')

    def test_equivalent_objects(self):
        """Test that immutable equivalent objects are indeed equivalent."""
        f1 = forever
        f2 = RepeatableAction(float('inf'))

        self.assertEqual(f1, f2)
        self.assertEqual(hash(f1), hash(f2))
