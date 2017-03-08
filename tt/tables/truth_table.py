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

    :param expr: The expression with which to populate this truth table.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression\
        <tt.expressions.bexpr.BooleanExpression>`

    :param fill_all: A flag indicating whether the entirety of the table should
        be filled on initialization; defaults to ``True``.
    :type fill_all: :class:`bool <python:bool>`, optional

    :param ordering: An input that maps to this class's :attr:`ordering`
        property. If omitted, the ordering of symbols in the table will match
        that of the symbols' appearance in the original expression.
    :type ordering: List[:class:`str <python:str>`], optional

    :raises DuplicateSymbolError: If multiple symbols of the same name are
        passed into the ``ordering`` list.
    :raises ExtraSymbolError: If a symbol not present in the expression is
        passed into the ``ordering`` list.
    :raises MissingSymbolError: If a symbol present in the expression is
        omitted from the ``ordering`` list.
    :raises InvalidArgumentTypeError: If an unexpected parameter type is
        encountered.
    :raises NoEvaluationVariationError: If an expression without any unqiue
        symbols (i.e., one merely composed of constant operators) is specified.

    .. note::

        See :func:`assert_iterable_contains_all_expr_symbols\
        <tt.utils.assertions.assert_iterable_contains_all_expr_symbols>`
        for more information about the exceptions raised by this class's
        initializer.

    """

    def __init__(self, expr, fill_all=True, ordering=None):
        if isinstance(expr, str):
            self._expr = BooleanExpression(expr)
        elif isinstance(expr, BooleanExpression):
            self._expr = expr
        else:
            raise InvalidArgumentTypeError(
                'Arg `expr` must be of type `str` or `BooleanExpression`')

        if ordering is None:
            self._ordering = self._expr.symbols
        else:
            assert_iterable_contains_all_expr_symbols(ordering,
                                                      set(self._expr.symbols))
            self._ordering = ordering

        if not self._ordering:
            raise NoEvaluationVariationError(
                'This expression is composed only of constant values')

        self._symbol_position_dict = {symbol: i for i, symbol in
                                      enumerate(self._ordering)}
        self._results = [None for _ in range(2**len(self._ordering))]

        if fill_all:
            self.fill()

    @property
    def expr(self):
        """The ``BooleanExpression`` object represented by this table.

        :type: :class:`BooleanExpression\
                       <tt.expressions.bexpr.BooleanExpression>`

        """
        return self._expr

    @property
    def ordering(self):
        """The order in which the symbols should appear in the truth table.

        :type: List[:class:`str <python:str>`]

        Here's a short example of alternative orderings of a partially-filled,
        three-symbol table::

            >>> from tt import TruthTable
            >>> t = TruthTable('(A or B) and C', fill_all=False)
            >>> t.fill(A=0, B=0)
            >>> print(t)
            +---+---+---+---+
            | A | B | C |   |
            +---+---+---+---+
            | 0 | 0 | 0 | 0 |
            +---+---+---+---+
            | 0 | 0 | 1 | 0 |
            +---+---+---+---+
            >>> t = TruthTable('(A or B) and C',
            ...                fill_all=False, ordering=['C', 'B', 'A'])
            >>> t.fill(A=0, B=0)
            >>> print(t)
            +---+---+---+---+
            | C | B | A |   |
            +---+---+---+---+
            | 0 | 0 | 0 | 0 |
            +---+---+---+---+
            | 1 | 0 | 0 | 0 |
            +---+---+---+---+

        """
        return self._ordering

    @property
    def results(self):
        """A list containing the results of each possible set of inputs.

        :type: List[:class:`bool <python:bool>`]

        In the case that the table is not completely filled, spots in this list
        that do not yet have a computed result will hold the ``None`` value.

        Regardless of the filled status of this table, all
        positions in the ``results`` list are allocated at initialization and
        subsequently filled as computed. This is illustrated in the below
        example::

            >>> from tt import TruthTable
            >>> t = TruthTable('A or B', fill_all=False)
            >>> t.results
            [None, None, None, None]
            >>> t.fill(A=0)
            >>> t.results
            [False, True, None, None]
            >>> t.fill()
            >>> t.results
            [False, True, True, True]

        """
        return self._results

    def __str__(self):
        col_widths = self._get_col_widths()
        row_sep = self._get_row_sep(col_widths)

        filled_row_count = 0
        rows = []
        rows.append(row_sep)
        rows.append(self._get_as_table_row(self._ordering + [' '], col_widths))
        rows.append(row_sep)

        for i, inputs in enumerate(self.input_combos()):
            result = self._results[i]
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

        :param kwargs: Filter which entries in the table are filled by
            specifying symbol values through the keyword args.

        :raises ExtraSymbolError: If a symbol not in the expression is passed
            as a keyword arg.
        :raises InvalidBooleanValueError: If a non-Boolean value is passed
            as a value for one of the keyword args.

        .. note::

            See :func:`assert_all_valid_keys\
            <tt.utils.assertions.assert_all_valid_keys>`
            for more information about the exceptions raised by this method.

        An example of iteratively filling a table::

            >>> from tt import TruthTable
            >>> t = TruthTable('A or B', fill_all=False)
            >>> print(t)
            Empty!
            >>> t.fill(A=0)
            >>> print(t)
            +---+---+---+
            | A | B |   |
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+
            | 0 | 1 | 1 |
            +---+---+---+
            >>> t.fill(A=1)
            >>> print(t)
            +---+---+---+
            | A | B |   |
            +---+---+---+
            | 0 | 0 | 0 |
            +---+---+---+
            | 0 | 1 | 1 |
            +---+---+---+
            | 1 | 0 | 1 |
            +---+---+---+
            | 1 | 1 | 1 |
            +---+---+---+

        """
        assert_all_valid_keys(kwargs, set(self._ordering))

        # convert all kwarg values to bools
        restrictions = {k: bool(v) for k, v in kwargs.items()}

        # I think the restriction of inputs can be greatly optimized by
        # pre-computing the ranges of indices for which the inputs will
        # be valid
        for i, input_combo in enumerate(self.input_combos()):
            input_dict = {symbol: input_combo[j] for j, symbol in
                          enumerate(self._ordering)}

            skip = False
            for k, v in restrictions.items():
                if input_dict[k] != v:
                    skip = True
                    break

            if not skip:
                self._results[i] = self._expr.evaluate_unchecked(**input_dict)

    def input_combos(self, combo_len=None):
        """Get an iterator of Boolean input combinations for this expression.

        :param combo_len: The length of each combination in the returned
            iterator. If omitted, this defaults to the number of symbols in the
            expression.
        :type combo_len: :class:`int <python:int>`, optional

        :returns: An iterator of tuples containing permutations of Boolean
            inputs.
        :rtype: :func:`itertools.product <python:itertools.product>`

        The length of each tuple of combinations is the same as the number of
        symbols in this expression if no ``combo_len`` value is specified;
        otherwise, the specified value is used.

        Iterating through the returned value, without fiddling with the
        ``combo_len`` input, will yield every combination of inputs for this
        expression.

        A simple example::

            >>> from tt import TruthTable
            >>> t = TruthTable('A and B')
            >>> for tup in t.input_combos():
            ...     print(tup)
            ...
            (False, False)
            (False, True)
            (True, False)
            (True, True)

        """
        repeat = len(self._ordering) if combo_len is None else combo_len
        return itertools.product((False, True), repeat=repeat)

    def _get_as_table_row(self, items, col_widths):
        """Convert an iterable to a row in the table ``__str__``.

        :param items: The items to convert to a table row.
        :type items: Iterable[:class:`str <python:str>`]

        :param col_widths: A list of integers specifying the column widths for
            each column of the table.
        :type col_widths: List[:class:`int <python:int>`]

        :returns: The string representation of the table row.
        :rtype: :class:`str <python:str>`

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

        :param padding: The additional padding to add to both the left and
            right of the contents of each cell.
        :type padding: :class:`int <python:int>`

        :returns: A list of ints representing the width of each column of the
            table.
        :rtype: List[:class:`int <python:int>`]

        """
        tot_padding = 2 * padding
        symbol_widths = [tot_padding + len(symbol) for
                         symbol in self._ordering]
        return symbol_widths + [tot_padding + 1]

    def _get_row_sep(self, col_widths):
        """Get the string separator for truth table rows.

        :param col_widths: A list of integers representing the width of each
            column in the table.
        :type col_widths: List[:class:`int <python:int>`]

        :returns: The row separator, of the style ``+---+---+---+``.
        :rtype: :class:`str <python:str>`

        """
        return '+' + '+'.join('-' * i for i in col_widths) + '+'
