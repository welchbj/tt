"""Exception type definitions related to expression evaluation."""

from .base import TtError


class EvaluationError(TtError):
    """An exception type for errors occurring in expression evaluation.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class InvalidBooleanValueError(EvaluationError):
    """An exception for an invalid truth or don't care value passed.

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
