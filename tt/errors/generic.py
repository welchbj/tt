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


class InvalidArgumentValueError(TtError):
    """An exception type for invalid argument values.

    .. code-block:: python

        TODO

    """


class ConflictingArgumentsError(TtError):
    """An exception type for two or more conflicting arguments.

    .. code-block:: python

        TODO

    """


class RequiredArgumentError(TtError):
    """An exception for when a required argument is missing.

    .. code-block:: python

        TODO

    """
