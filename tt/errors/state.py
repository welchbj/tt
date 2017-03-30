"""Exception type definitions related to invalid operations based on state."""

from .base import TtError


class StateError(TtError):
    """An exception type for errors occurring in expression evaluation.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class AlreadyFullTableException(StateError):
    """An exception to be raised when attempting to fill an already-full table.

    .. code-block:: python

        TODO

    """
