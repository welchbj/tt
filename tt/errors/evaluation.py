"""Exception type definitions related to expression evaluation."""

from .base import TtError


class EvaluationError(TtError):
    """An exception type for errors occurring in expression evaluation.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class DuplicateSymbolError(EvaluationError):
    """An exception type for user-specified duplicate symbols.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('A or B', ordering=['A', 'A', 'B'])
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.evaluation.DuplicateSymbolError'>

    """


class ExtraSymbolError(EvaluationError):
    """An exception for a passed token that is not a parsed symbol.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('A or B', ordering=['A', 'B', 'C'])
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.evaluation.ExtraSymbolError'>

    """


class InvalidBooleanValueError(EvaluationError):
    """An exception for an invalid truth value passed in evaluation.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('A or B')
        ...     b.evaluate(A=1, B='brian')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.evaluation.InvalidBooleanValueError'>

    """


class MissingSymbolError(EvaluationError):
    """An exception type for a missing token value in evaluation.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('A and B')
        ...     b.evaluate(A=1)
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.evaluation.MissingSymbolError'>

    """


class NoEvaluationVariationError(EvaluationError):
    """An exception type for when evaluation of an expression will not vary.

    .. code-block:: python

        >>> from tt import TruthTable
        >>> try:
        ...     t = TruthTable('1 or 0')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.evaluation.NoEvaluationVariationError'>

    """
