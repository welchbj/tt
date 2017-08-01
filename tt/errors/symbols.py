"""Exception types related to symbol processing."""

from .base import TtError


class SymbolError(TtError):
    """An exception for errors occurring in symbol processing. This exception
    type should be sub-classed and is not meant to be raised explicitly.

    """


class DuplicateSymbolError(SymbolError):
    """An exception type for user-specified duplicate symbols.

    Here's an example where we try to pass duplicate symbols to the
    ``ordering`` property of the :class:`TruthTable \
    <tt.tables.truth_table.TruthTable>` class::

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', ordering=['A', 'A', 'B'])
        Traceback (most recent call last):
            ...
        tt.errors.symbols.DuplicateSymbolError: Received duplicate symbols

    """


class ExtraSymbolError(SymbolError):
    """An exception for a passed token that is not a parsed symbol.

    Here's a quick table example::

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', ordering=['A', 'B', 'C'])
        Traceback (most recent call last):
            ...
        tt.errors.symbols.ExtraSymbolError: Received unexpected symbols: "C"

    """


class MissingSymbolError(SymbolError):
    """An exception type for a missing token value in evaluation.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A and B')
        >>> b.evaluate(A=1)
        Traceback (most recent call last):
            ...
        tt.errors.symbols.MissingSymbolError: Did not receive value for the \
following symbols: "B"

    """
