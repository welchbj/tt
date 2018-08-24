"""Tests for the ComposedTransformation class."""

import unittest

from tt.errors import (
    InvalidArgumentTypeError)
from tt.transformations import (
    apply_de_morgans,
    apply_inverse_law,
    coalesce_negations,
    ComposedTransformation)


class TestUtilsComposedTransformation(unittest.TestCase):

    def test_init_without_callable(self):
        """Test initializing when passing an invalid fn parameter."""
        ComposedTransformation(apply_de_morgans)
        with self.assertRaises(InvalidArgumentTypeError):
            ComposedTransformation(1)

    def test_init_improper_next_transformation(self):
        """Test setting the next_transformation field with a bad type."""
        with self.assertRaises(InvalidArgumentTypeError):
            ComposedTransformation(apply_de_morgans, next_transformation=1)

    def test_init_with_function(self):
        """Test initializing with a transformation function."""
        def sample_fn(expr):
            return expr

        ct = ComposedTransformation(sample_fn)
        self.assertEqual(ct.fn, sample_fn)
        self.assertEqual(
            str(ct),
            'sample_fn')

    def test_init_with_composed_transformation(self):
        """Test initializing with an existing ComposedTransformation object."""
        ct = ComposedTransformation(
                ComposedTransformation(
                    ComposedTransformation(coalesce_negations)))
        self.assertEqual(
            str(ct),
            'coalesce_negations')

    def test_init_with_existing_next_transformation(self):
        """Test initializing with an existing next_transformation field."""
        next_ct = ComposedTransformation(apply_de_morgans)
        first_ct = ComposedTransformation(
                        lambda e: e,
                        next_transformation=next_ct)
        self.assertEqual(first_ct.next_transformation, next_ct)
        self.assertEqual(
            str(first_ct),
            '<lambda> -> apply_de_morgans')

    def test_hash_equivalence(self):
        """Test the equivalence of two logically equivalent objects."""
        ct1 = ComposedTransformation(
                apply_de_morgans,
                next_transformation=ComposedTransformation(coalesce_negations),
                times=5)
        ct2 = ComposedTransformation(
                apply_de_morgans,
                next_transformation=ComposedTransformation(coalesce_negations),
                times=5)
        ct3 = ComposedTransformation(apply_de_morgans)

        self.assertNotEqual(ct1, ct3)
        self.assertNotEqual(ct2, ct3)
        self.assertEqual(ct1, ct2)

    def test_shift_operators(self):
        """Test the >> and << operators."""
        ct1 = ComposedTransformation(apply_de_morgans)
        ct2 = ComposedTransformation(coalesce_negations)
        self.assertEqual(ct1 >> ct2, ct2 << ct1)
        self.assertEqual(ct2 >> ct1, ct1 << ct2)

    def test_str_methods(self):
        """Test the __str__ and __repr__ magic methods."""
        ct = ComposedTransformation(apply_inverse_law)
        self.assertEqual(
            str(ct),
            'apply_inverse_law')
        self.assertEqual(
            repr(ct),
            '<ComposedTransformation [apply_inverse_law]>')

    def test_compose_with_invalid_type(self):
        """Test composing a valid object with an invalid type."""
        ct = ComposedTransformation(apply_de_morgans)
        with self.assertRaises(InvalidArgumentTypeError):
            ct.compose(None)
