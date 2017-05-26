"""Implementation of a truth table."""

from __future__ import division

import itertools

from math import log
from string import ascii_uppercase as ALPHABET

from tt._assertions import (
    assert_all_valid_keys,
    assert_iterable_contains_all_expr_symbols)
from tt.definitions import (
    boolean_variables_factory,
    DONT_CARE_VALUE,
    is_valid_identifier)
from tt.errors import (
    AlreadyFullTableError,
    ConflictingArgumentsError,
    ExtraSymbolError,
    InvalidArgumentTypeError,
    InvalidArgumentValueError,
    InvalidBooleanValueError,
    InvalidIdentifierError,
    MissingSymbolError,
    NoEvaluationVariationError,
    RequiredArgumentError,
    RequiresFullTableError)
from tt.expressions import BooleanExpression


_DEFAULT_CELL_PADDING = 1


class TruthTable(object):

    """A class representing a truth table.

    There are two ways to fill a table: either populated from an expression or
    by specifying the values yourself.

    An existing :class:`BooleanExpression <tt.expressions.BooleanExpression>`
    expression can be used, or you can just pass in a string::

        >>> from tt import TruthTable
        >>> t = TruthTable('A xor B')
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
        | 1 | 1 | 0 |
        +---+---+---+

    When manually specifying the values tt can generate the symbols for you::

        >>> from tt import TruthTable
        >>> t = TruthTable(from_values='0110')
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
        | 1 | 1 | 0 |
        +---+---+---+

    You can also specify the symbol names yourself, if you'd like::

        >>> from tt import TruthTable
        >>> t = TruthTable(from_values='0110', ordering=['tt', 'rocks'])
        >>> print(t)
        +----+-------+---+
        | tt | rocks |   |
        +----+-------+---+
        | 0  |   0   | 0 |
        +----+-------+---+
        | 0  |   1   | 1 |
        +----+-------+---+
        | 1  |   0   | 1 |
        +----+-------+---+
        | 1  |   1   | 0 |
        +----+-------+---+

    :param expr: The expression with which to populate this truth table. If
        this argument is omitted, then the ``from_values`` argument must be
        properly set.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression\
        <tt.expressions.bexpr.BooleanExpression>`

    :param from_values: A string of 1's, 0's, and x's representing the values
        to be stored in the table; the length of this string must be a power
        of 2 and is the complete set of values (in sequential order) to be
        stored in table.
    :type from_values: :class:`str <python:str>`

    :param fill_all: A flag indicating whether the entirety of the table should
        be filled on initialization; defaults to ``True``.
    :type fill_all: :class:`bool <python:bool>`, optional

    :param ordering: An input that maps to this class's :attr:`ordering`
        property. If omitted, the ordering of symbols in the table will match
        that of the symbols' appearance in the original expression.
    :type ordering: List[:class:`str <python:str>`], optional

    :raises ConflictingArgumentsError: If both ``expr`` and ``from_values`` are
        specified in the initalization; a table can only be instantiated from
        one or the other.
    :raises DuplicateSymbolError: If multiple symbols of the same name are
        passed into the ``ordering`` list.
    :raises ExtraSymbolError: If a symbol not present in the expression is
        passed into the ``ordering`` list.
    :raises MissingSymbolError: If a symbol present in the expression is
        omitted from the ``ordering`` list.
    :raises InvalidArgumentTypeError: If an unexpected parameter type is
        encountered.
    :raises InvalidArgumentValueError: If the number of values specified via
        ``from_values`` is not a power of 2 or the ``ordering`` list (when
        filling the table using ``from_values``) is empty.
    :raises InvalidIdentifierError: If any symbol names specified in
        ``ordering`` are not valid identifiers.
    :raises NoEvaluationVariationError: If an expression without any unqiue
        symbols (i.e., one merely composed of constant operands) is specified.
    :raises RequiredArgumentError: If neither the ``expr`` or ``from_values``
        arguments are specified.

    """

    def __init__(self, expr=None, from_values=None, fill_all=True,
                 ordering=None):
        if expr is not None and from_values is not None:
            raise ConflictingArgumentsError(
                '`expr` and `from_values` are mutually exclusive arguments')
        elif expr is None and from_values is None:
            raise RequiredArgumentError(
                'Must specify either `expr` or `from_values`')

        self._num_filled_slots = 0

        if expr is not None:
            self._init_from_expression(expr, fill_all, ordering)
        else:
            self._init_from_values(from_values, ordering)

        self._symbol_vals_factory = boolean_variables_factory(self._ordering)

    def _init_from_expression(self, expr, fill_all, ordering):
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
            assert_iterable_contains_all_expr_symbols(
                ordering, set(self._expr.symbols))
            self._ordering = ordering

        if not self._ordering:
            raise NoEvaluationVariationError(
                'This expression is composed only of constant values')

        self._results = [None for _ in range(2**len(self._ordering))]
        if fill_all:
            self.fill()

    def _init_from_values(self, from_values, ordering):
        if isinstance(from_values, str):
            valid = {'0', '1', DONT_CARE_VALUE}
            if not from_values:
                raise InvalidArgumentValueError(
                    'Cannot specify an empty string')
            elif not all(value in valid for value in from_values):
                raise InvalidBooleanValueError(
                    'Invalid Boolean/don\'t care value specified')
        else:
            raise InvalidArgumentTypeError(
                '`from_values` must either be a string or list of strings')

        num_values = len(from_values)
        if (num_values & (num_values - 1)) != 0:
            # assert that number of input values is a power of 2
            raise InvalidArgumentValueError(
                'Must specify a number of input values that is a power of 2')

        user_gave_symbols = ordering is not None
        if not user_gave_symbols:
            # user left it up to us to generate symbols
            num_required_symbols = int(log(num_values, 2))
            self._ordering = TruthTable.generate_symbols(num_required_symbols)
        elif not isinstance(ordering, list):
            raise InvalidArgumentTypeError('`ordering` must be a list')
        elif not all(isinstance(elt, str) for elt in ordering):
            raise InvalidArgumentTypeError(
                '`ordering` must only contain strings')
        else:
            # validate user-provided ordering/symbols
            num_symbols = len(ordering)
            if not num_symbols:
                raise InvalidArgumentValueError(
                    'If specifying `ordering`, it must be non-empty')

            num_expected_values = 2**num_symbols
            if num_values < num_expected_values:
                raise ExtraSymbolError(
                    'Too many symbols provided for the specified values')
            elif num_values > num_expected_values:
                raise MissingSymbolError(
                    'Too few symbols provided for the specified values')

            # verify all symbols are valid identifiers
            for symbol_name in ordering:
                if not is_valid_identifier(symbol_name):
                    raise InvalidIdentifierError(
                        '"{}" in ordering is not a valid symbol name'.format(
                            symbol_name),
                        None, None)

            self._ordering = ordering

        self._expr = None

        bool_dict = {'0': False, '1': True, DONT_CARE_VALUE: DONT_CARE_VALUE}
        self._results = [bool_dict[v] for v in from_values]
        self._num_filled_slots = len(self._results)

    @property
    def expr(self):
        """The ``BooleanExpression`` object represented by this table.

        This attribute will be ``None`` if this table was not derived from
        an expression (i.e., the user provided the values).

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
    def is_full(self):
        """A Boolean flag indicating whether this table is full or not.

        :type: :class:`bool <python:bool>`

        Attempting to further fill an already-full table will raise an
        :exc:`AlreadyFullTableError\
        <tt.errors.state.AlreadyFullTableError>`::

            >>> from tt import TruthTable
            >>> t = TruthTable('A or B', fill_all=False)
            >>> t.is_full
            False
            >>> t.fill()
            >>> t.is_full
            True
            >>> try:
            ...     t.fill()
            ... except Exception as e:
            ...     print(type(e))
            ...
            <class 'tt.errors.state.AlreadyFullTableError'>

        """
        return self._num_filled_slots == len(self._results)

    @property
    def results(self):
        """A list containing the results of each possible set of inputs.

        :type: List[:class:`bool <python:bool>`, :class:`str <python:str>`]

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

        If the table is filled upon initialization via the ``from_values``
        parameter, don't care strings could be present in the result list::

            >>> from tt import TruthTable
            >>> t = TruthTable(from_values='1xx0')
            >>> t.results
            [True, 'x', 'x', False]

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

        _input_combos = TruthTable.input_combos(len(self._ordering))
        for i, inputs in enumerate(_input_combos):
            result = self._results[i]
            if result is None:
                continue
            elif result == DONT_CARE_VALUE:
                result_str = result
            else:
                result_str = str(int(result))

            item_strs = [str(int(val)) for val in inputs]
            item_strs.append(result_str)
            rows.append(self._get_as_table_row(item_strs, col_widths))
            rows.append(row_sep)
            filled_row_count += 1

        if not filled_row_count:
            return 'Empty!'
        else:
            return '\n'.join(rows)

    def __iter__(self):
        _input_combos = TruthTable.input_combos(len(self._ordering))
        for i, combo in enumerate(_input_combos):
            result = self._results[i]
            if result is not None:
                yield self._symbol_vals_factory._make(combo), result

    def __getitem__(self, i):
        return self._results[i]

    def equivalent_to(self, other):
        """Return whether this table is equivalent to another source of truth.

        :param other: The other source of truth with which to compare logical
            equivalence.
        :type other: :class:`TruthTable`, :class:`str <python:str>`, or
            :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

        :returns: True if the other expression is logically equivalent to this
            one, otherwise False.
        :rtype: :class:`bool <python:bool>`

        :raises InvalidArgumentTypeError: If the ``other`` argument is not one
            of the acceptable types.
        :raises RequiresFullTableError: If either the calling table or other
            source of truth represents an unfilled table.

        It is important to note that the concept of equivalence employed here
        is only concerned with the corresponding outputs between this table
        and the other provided source of truth. For example, the ordering of
        symbols is not taken into consideration when computing equivalence::

            >>> from tt import TruthTable
            >>> t1 = TruthTable('op1 or op2')
            >>> t2 = TruthTable('A or B')
            >>> t1.equivalent_to(t2)
            True
            >>> t2.equivalent_to(t1)
            True

        Another area of possible ambiguity here is the role of the don't care
        value in equivalence. When comparing tables, don't cares in the caller
        will allow for any corresponding value in ``other``, but the reverse is
        not true. For example::

            >>> from tt import TruthTable
            >>> t1 = TruthTable(from_values='0x11')
            >>> t2 = TruthTable(from_values='0011')
            >>> t1.equivalent_to(t2)
            True
            >>> t2.equivalent_to(t1)
            False

        Additionally, only full tables are valid for equivalence checks. The
        appropriate error will be raised if you attempt to check the
        equivalence of partially filled tables::

            >>> from tt import TruthTable
            >>> t = TruthTable('A or B', fill_all=False)
            >>> t.fill(A=0)
            >>> try:
            ...     t.equivalent_to('A or B')
            ... except Exception as e:
            ...     print(type(e))
            ...
            <class 'tt.errors.state.RequiresFullTableError'>

        """
        if isinstance(other, TruthTable):
            other_table = other
        elif isinstance(other, (str, BooleanExpression)):
            other_table = TruthTable(other)
        else:
            raise InvalidArgumentTypeError(
                'other must be a BooleanExpression, TruthTable, or str')

        if not self.is_full or not other_table.is_full:
            raise RequiresFullTableError(
                'Equivalence can only be checked on full truth tables')

        if other is self:
            return True
        elif len(other_table.results) != len(self._results):
            return False

        for i, result in enumerate(self._results):
            if result == DONT_CARE_VALUE:
                continue
            elif other_table[i] != result:
                return False

        return True

    def fill(self, **kwargs):
        """Fill the table with results, based on values specified by kwargs.

        :param kwargs: Filter which entries in the table are filled by
            specifying symbol values through the keyword args.

        :raises AlreadyFullTableError: If the table is already full when this
            method is called.
        :raises ExtraSymbolError: If a symbol not in the expression is passed
            as a keyword arg.
        :raises InvalidBooleanValueError: If a non-Boolean value is passed
            as a value for one of the keyword args.

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
        if self.is_full:
            raise AlreadyFullTableError('Cannot fill an already-full table')

        assert_all_valid_keys(kwargs, set(self._ordering))

        # convert all kwarg values to bools
        restrictions = {k: bool(v) for k, v in kwargs.items()}

        # I think the restriction of inputs can be greatly optimized by
        # pre-computing the ranges of indices for which the inputs will
        # be valid
        _input_combos = TruthTable.input_combos(len(self._ordering))
        for i, input_combo in enumerate(_input_combos):
            input_dict = {symbol: input_combo[j] for j, symbol in
                          enumerate(self._ordering)}

            skip = False
            for k, v in restrictions.items():
                if input_dict[k] != v:
                    skip = True
                    break

            if not skip and self._results[i] is None:
                self._results[i] = self._expr.evaluate_unchecked(**input_dict)
                self._num_filled_slots += 1

    @staticmethod
    def input_combos(combo_len):
        """Get an iterator of Boolean input combinations for this expression.

        :param combo_len: The length of each combination in the returned
            iterator.
        :type combo_len: :class:`int <python:int>`, optional

        :returns: An iterator of tuples containing permutations of Boolean
            inputs.
        :rtype: :func:`itertools.product <python:itertools.product>`

        A simple example::

            >>> from tt import TruthTable
            >>> for tup in TruthTable.input_combos(2):
            ...     print(tup)
            ...
            (False, False)
            (False, True)
            (True, False)
            (True, True)

        """
        return itertools.product((False, True), repeat=combo_len)

    @staticmethod
    def generate_symbols(num_symbols):
        """Generate a list of symbols for a specified number of symbols.

        Generated symbol names are permutations of a properly-sized number
        of uppercase alphabet letters.

        :param num_symbols: The number of symbols to generate.
        :type num_symbols: :class:`int <python:int>`

        :returns: A list of strings of length ``num_symbols``, containing
            auto-generated symbols.
        :rtype: List[:class:`str <python:str>`]

        A simple example::

            >>> from tt import TruthTable
            >>> TruthTable.generate_symbols(3)
            ['A', 'B', 'C']
            >>> TruthTable.generate_symbols(7)
            ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        """
        num_repeats = 1

        while num_symbols > len(ALPHABET)**num_repeats:
            num_repeats += 1

        # generate symbols for the user based on the uppercase alphabet
        symbol_product = itertools.product(ALPHABET, repeat=num_repeats)
        symbol_pool = (''.join(elts) for elts in symbol_product)
        return list(itertools.islice(symbol_pool, num_symbols))

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
