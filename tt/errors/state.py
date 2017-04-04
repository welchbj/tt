"""Exception type definitions related to invalid operations based on state."""

from .base import TtError


class StateError(TtError):
    """An exception type for errors occurring in expression evaluation.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class AlreadyFullTableError(StateError):
    """An exception to be raised when attempting to fill an already-full table.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', fill_all=False)
        >>> t.fill()
        >>> try:
        ...     t.fill()
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.state.AlreadyFullTableError'>

    """


class RequiresFullTableError(StateError):
    """An exception to be raised when a full table is required.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> t = TruthTable('A or B', fill_all=False)
        >>> try:
        ...     print(t.equivalent_to('A or B'))
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.state.RequiresFullTableError'>

    """
