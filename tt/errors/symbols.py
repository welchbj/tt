"""Exception types related to symbol processing."""

from .base import TtError


class SymbolError(TtError):
    """An exception for errors occurring in symbol processing.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class DuplicateSymbolError(SymbolError):
    """An exception type for user-specified duplicate symbols.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('A or B', ordering=['A', 'A', 'B'])
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.symbols.DuplicateSymbolError'>

    """


class ExtraSymbolError(SymbolError):
    """An exception for a passed token that is not a parsed symbol.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('A or B', ordering=['A', 'B', 'C'])
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.symbols.ExtraSymbolError'>

    """


class MissingSymbolError(SymbolError):
    """An exception type for a missing token value in evaluation.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('A and B')
        ...     b.evaluate(A=1)
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.symbols.MissingSymbolError'>

    """
