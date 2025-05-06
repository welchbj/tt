"""Tests for valid use of the tt_compose function."""

import unittest

from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)
from tt.transformations import (
    apply_de_morgans,
    apply_idempotent_law,
    coalesce_negations,
    forever,
    repeat,
    tt_compose,
    twice)


class TestUtilsTtCompose(unittest.TestCase):

    def _custom_trans_func(self, expr):
        """Dummy custom transformation that causes no change."""
        return expr

    def test_only_existing_transformations(self):
        """Test a composition of only existing transformations."""
        f = tt_compose(apply_de_morgans, coalesce_negations)
        self.assertEqual(
            str(f),
            'apply_de_morgans -> coalesce_negations')

    def test_only_callable_functions(self):
        """Test a composition of callable functions (not transformations)."""
        f = tt_compose(self._custom_trans_func, self._custom_trans_func)
        self.assertEqual(
            str(f),
            '_custom_trans_func -> _custom_trans_func')
        self.assertEqual(
            str(f('A or B')),
            'A or B')

    def test_mixed_callables_and_transformations(self):
        """Test a composition of mixed transformations and callables."""
        f = tt_compose(self._custom_trans_func, apply_de_morgans)
        self.assertEqual(
            str(f),
            '_custom_trans_func -> apply_de_morgans')
        self.assertEqual(
            str(f('not (A or B)')),
            'not A and not B')

        def _another_custom_trans_func(expr):
            return expr

        f = tt_compose(
            self._custom_trans_func,
            _another_custom_trans_func,
            coalesce_negations)
        self.assertEqual(
            str(f),
            '_custom_trans_func -> _another_custom_trans_func -> '
            'coalesce_negations')
        self.assertEqual(
            str(f('!!!A')),
            '!A')

    def test_modifiers_on_transformations(self):
        """Test applying modifiers on existing transformations."""
        de_morgan_izable_expr = 'not (not (not (A or B)))'

        f = tt_compose(apply_de_morgans, twice)
        self.assertEqual(
            str(f),
            'apply_de_morgans (2 times)')
        self.assertEqual(
            str(f(de_morgan_izable_expr)),
            'not (not not A or not not B)')

        f = tt_compose(apply_de_morgans, forever, coalesce_negations)
        self.assertEqual(
            str(f),
            'apply_de_morgans (inf times) -> coalesce_negations')
        self.assertEqual(
            str(f(de_morgan_izable_expr)),
            'not A and not B')

    def test_modifiers_on_callables(self):
        """Test applying modifiers to callable functions."""
        f = tt_compose(self._custom_trans_func, twice)
        self.assertEqual(
            str(f),
            '_custom_trans_func (2 times)')
        self.assertEqual(
            str(f('A -> B')),
            'A -> B')

    def test_nested_compositions(self):
        """Test nesting multiple tt_compose compositions."""
        f = tt_compose(
                tt_compose(apply_de_morgans, twice, coalesce_negations),
                tt_compose(apply_idempotent_law, forever),
                self._custom_trans_func)
        self.assertEqual(
            str(f),
            'apply_de_morgans (2 times) -> coalesce_negations -> '
            'apply_idempotent_law (inf times) -> '
            '_custom_trans_func')
        self.assertEqual(
            str(f('not (not (A or A))')),
            'A')

    def test_consecutive_modifiers(self):
        """Test a sequence with multiple consecutive modifiers."""
        f = tt_compose(
            apply_de_morgans, twice, twice, repeat(3))
        self.assertEqual(
            str(f),
            'apply_de_morgans (12 times)')

        f = tt_compose(
                coalesce_negations,
                twice, repeat(3), repeat(4), forever)
        self.assertEqual(
            str(f),
            'coalesce_negations (inf times)')

    def test_invalid_number_of_args(self):
        """Test an invalid number of arguments."""
        with self.assertRaises(InvalidArgumentValueError):
            tt_compose()

    def test_begin_with_modifier(self):
        """Test beginning the sequence with a transformation modifier."""
        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(forever, forever)

        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(repeat(3), repeat(2), repeat(1))

        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(twice, apply_de_morgans)

    def test_begin_with_non_callable(self):
        """Test beginning the sequence with a non-callable object."""
        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(1, apply_de_morgans)

    def test_sequence_contains_non_callable(self):
        """Test inserting non-callables within the sequence."""
        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(apply_de_morgans, 2)

        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(apply_de_morgans, 'bad', twice)

        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(apply_de_morgans, 'not good', apply_de_morgans)

        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(apply_de_morgans, twice, 2)

    def test_sequence_contains_nested_error(self):
        """Test an error bubbling from a level deeper."""
        with self.assertRaises(InvalidArgumentTypeError):
            tt_compose(
                tt_compose(apply_de_morgans, 'string'),
                twice)
