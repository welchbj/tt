"""Exception type definitions related to invalid operations based on state."""

from .base import TtError


class StateError(TtError):
    """Base exception type for errors involving invalid state."""


class AlreadyConstrainedSymbolError(StateError):
    """An exception to be raised when trying to doubly constrain a symbol.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A or B or C')
        >>> with b.constrain(C=1):
        ...     with b.constrain(C=0):
        ...         pass
        ...
        Traceback (most recent call last):
        tt.errors.state.AlreadyConstrainedSymbolError: Symbol "C" cannot be \
constrained multiple times

    """


class AlreadyFullTableError(StateError):
    """An exception to be raised when attempting to fill an already-full table.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', fill_all=False)
        >>> t.fill()
        >>> t.is_full
        True
        >>> t.fill()
        Traceback (most recent call last):
        tt.errors.state.AlreadyFullTableError: Cannot fill an already-full \
table

    """


class RequiresFullTableError(StateError):
    """An exception to be raised when a full table is required.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', fill_all=False)
        >>> t.equivalent_to('A or B')
        Traceback (most recent call last):
        tt.errors.state.RequiresFullTableError: Equivalence can only be \
checked on full truth tables

    """


class RequiresNormalFormError(StateError):
    """An exception to be raised when expression normal form is required.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A nand (B or C)')
        >>> b.is_cnf or b.is_dnf
        False
        >>> for clause in b.iter_clauses():
        ...     print(clause)
        ...
        Traceback (most recent call last):
        tt.errors.state.RequiresNormalFormError: Must be in conjunctive or \
disjunctive normal form to iterate clauses

    """
