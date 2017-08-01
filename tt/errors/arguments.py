"""Generic exception types."""

from .base import TtError


class ArgumentError(TtError):
    """An exception type for invalid arguments. This exception type should be
    sub-classed and is not meant to be raised explicitly.

    """


class ConflictingArgumentsError(ArgumentError):
    """An exception type for two or more conflicting arguments.

    This error type can be seen in action by passing both an expression and a
    set of values to the :class:`TruthTable <tt.tables.truth_table.TruthTable>`
    class::

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', from_values='1111')
        Traceback (most recent call last):
            ...
        tt.errors.arguments.ConflictingArgumentsError: `expr` and \
`from_values` are mutually exclusive arguments

    """


class InvalidArgumentTypeError(ArgumentError):
    """An exception type for invalid argument types.

    To illustrate this error type, let's try passing an invalid argument when
    creating a :class:`TruthTable <tt.tables.truth_table.TruthTable>`::

        >>> from tt import TruthTable
        >>> t = TruthTable(7)
        Traceback (most recent call last):
            ...
        tt.errors.arguments.InvalidArgumentTypeError: Arg `expr` must be of \
type `str` or `BooleanExpression`

    """


class InvalidArgumentValueError(ArgumentError):
    """An exception type for invalid argument values.

    Here's an example where we pass a non-power of 2 number of values when
    attempting to create a :class:`TruthTable \
    <tt.tables.truth_table.TruthTable>`::

        >>> from tt import TruthTable
        >>> t = TruthTable(from_values='01x')
        Traceback (most recent call last):
            ...
        tt.errors.arguments.InvalidArgumentValueError: Must specify a number \
of input values that is a power of 2

    """


class RequiredArgumentError(ArgumentError):
    """An exception for when a required argument is missing.

    Let's try an example where we omit all arguments when attempting to make
    a new :class:`TruthTable <tt.tables.truth_table.TruthTable>` object::

        >>> from tt import TruthTable
        >>> t = TruthTable()
        Traceback (most recent call last):
            ...
        tt.errors.arguments.RequiredArgumentError: Must specify either `expr` \
or `from_values`

    """
