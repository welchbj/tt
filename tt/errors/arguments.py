"""Generic exception types."""

from .base import TtError


class ArgumentError(TtError):
    """An exception type for invalid arguments.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class ConflictingArgumentsError(ArgumentError):
    """An exception type for two or more conflicting arguments.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('A or B', from_values='1111')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.arguments.ConflictingArgumentsError'>

    """


class InvalidArgumentTypeError(ArgumentError):
    """An exception type for invalid argument types.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable(7)
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.arguments.InvalidArgumentTypeError'>

    """


class InvalidArgumentValueError(ArgumentError):
    """An exception type for invalid argument values.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable(from_values='01x')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.arguments.InvalidArgumentValueError'>

    """


class RequiredArgumentError(ArgumentError):
    """An exception for when a required argument is missing.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable()
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.arguments.RequiredArgumentError'>

    """
