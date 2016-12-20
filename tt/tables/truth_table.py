"""Implementation of a truth table."""

from __future__ import division

import itertools

from ..errors import InvalidArgumentTypeError, NoEvaluationVariationError
from ..expressions import BooleanExpression
from ..utils import (assert_all_valid_keys,
                     assert_iterable_contains_all_expr_symbols)


_DEFAULT_CELL_PADDING = 1


class TruthTable(object):

    """A class representing a truth table.

    Attributes:
        expr: The ``BooleanExpression`` object or a string from which to create
            the ``BooleanExpression`` object represented by this truth table.
        ordering (List[str], optional): An optional list of symbol names in the
            passed expression, specifying the order in which they should
            appear in the truth table (from left to right). If omitted, the
            ordering of the symbols will be consistent with the symbol's first
            occurrence in the passed expression.
        results (List[bool]): A list of ``int`` s representing the resultant
            evaluations for each combination of possible inputs.

    Raises:
        DuplicateSymbolError
        ExtraSymbolError
        MissingSymbolError

    """

    def __init__(self, expr, fill_all=True, ordering=None):
        if isinstance(expr, str):
            self.expr = BooleanExpression(expr)
        elif isinstance(expr, BooleanExpression):
            self.expr = expr
        else:
            raise InvalidArgumentTypeError(
                'Arg `expr` must be of type `str` or `BooleanExpression`')

        if ordering is None:
            self._ordering = self.expr.symbols
        else:
            assert_iterable_contains_all_expr_symbols(ordering,
                                                      set(self.expr.symbols))
            self._ordering = ordering

        if not self._ordering:
            raise NoEvaluationVariationError(
                'This expression is composed only of constant values')

        self._symbol_position_dict = {symbol: i for i, symbol in
                                      enumerate(self._ordering)}
        self.results = [None for _ in range(2**len(self._ordering))]

        if fill_all:
            self.fill()

    def __str__(self):
        col_widths = self._get_col_widths()
        row_sep = self._get_row_sep(col_widths)

        filled_row_count = 0
        rows = []
        rows.append(row_sep)
        rows.append(self._get_as_table_row(self._ordering + [' '], col_widths))
        rows.append(row_sep)

        for i, inputs in enumerate(self._input_combos()):
            result = self.results[i]
            if result is None:
                continue

            item_strs = [str(int(val)) for val in inputs]
            item_strs.append(str(int(result)))
            rows.append(self._get_as_table_row(item_strs, col_widths))
            rows.append(row_sep)
            filled_row_count += 1

        if not filled_row_count:
            return 'Empty!'
        else:
            return '\n'.join(rows)

    def fill(self, **kwargs):
        """Fill the table with results, based on values specified by kwargs.

        Args:
            **kwargs: Filter which entries in the table are filled by
                specifying symbol values through the keyword args.

        Raises:
            ExtraSymbolError
            InvalidBooleanValueError
            MissingSymbolError

        """
        assert_all_valid_keys(kwargs, set(self._ordering))

        # convert all kwarg values to bools
        restrictions = {k: bool(v) for k, v in kwargs.items()}

        # I think the restriction of inputs can be greatly optimized by
        # pre-computing the ranges of indices for which the inputs will
        # be valid
        for i, input_combo in enumerate(self._input_combos()):
            input_dict = {symbol: input_combo[j] for j, symbol in
                          enumerate(self._ordering)}

            skip = False
            for k, v in restrictions.items():
                if input_dict[k] != v:
                    skip = True
                    break

            if not skip:
                self.results[i] = self.expr.evaluate_unchecked(**input_dict)

    def _get_as_table_row(self, items, col_widths):
        """Convert an iterable to a row in the table ``__str__``.

        Args:
            items (Iterable[str]): The items to convert to a table row.
            col_widths (List[int]): A list of integers specifying the column
                widths for each column of the table.

        Returns:
            str: The string representation of the table row.

        """
        row = '|'
        for item, col_width in zip(items, col_widths):
            total_pad_len = col_width - len(item)
            left_pad_len = total_pad_len // 2
            right_pad_len = total_pad_len - left_pad_len
            row += (left_pad_len * ' ' +
                    item +
                    right_pad_len * ' '
                    + '|')

        return row

    def _get_col_widths(self, padding=_DEFAULT_CELL_PADDING):
        """Get a list of integers, representing the column widths of the table.

        Args:
            padding (int): The additional padding to add to both the left and
                right of the contents of each cell.

        Returns:
            List[int]: A list of integers representing the width of each
                column of the table.

        """
        tot_padding = 2 * padding
        symbol_widths = [tot_padding + len(symbol) for
                         symbol in self._ordering]
        return symbol_widths + [tot_padding + 1]

    def _get_row_sep(self, col_widths):
        """Get the string separator for truth table rows.

        Args:
            col_widths (List[int]): A list of integers representing the width
                of each column in the table.

        Returns:
            str: The row separator, of the style ``+---+---+---+``.

        """
        return '+' + '+'.join('-' * i for i in col_widths) + '+'

    def _input_combos(self, combo_len=None):
        """Get a generator of Boolean input combinations.

        Note:
            This function expects the ``_ordering`` attribute to be non-empty.

        Args:
            combo_len (int, optional): The number of values required in each
                set of combinations; by default, the number of symbols in this
                expression will be used.

        Returns:
            A generator of lists holding permutations of Boolean inputs.

        """
        repeat = len(self._ordering) if combo_len is None else combo_len
        return itertools.product((False, True), repeat=repeat)
