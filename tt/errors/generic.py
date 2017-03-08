"""Generic exception types."""

from .base import TtError


class InvalidArgumentTypeError(TtError):
    """An exception type for invalid argument types.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable(7)
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.generic.InvalidArgumentTypeError'>

    """
