"""Exception type definitions related to expression evaluation."""

from .base import TtError


class EvaluationError(TtError):
    """An exception type for errors occurring in expression evaluation. This
    exception type should be sub-classed and is not meant to be raised
    explicitly.

    """


class InvalidBooleanValueError(EvaluationError):
    """An exception for when an invalid truth or don't care value is passed.

    Here's an example where we attempt to evaluate a \
    :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` with
    an invalid value passed through ``kwargs``::

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A or B')
        >>> b.evaluate(A=1, B='brian')
        Traceback (most recent call last):
            ...
        tt.errors.evaluation.InvalidBooleanValueError: "brian" passed as \
value for "B" is not a valid Boolean value

    """


class NoEvaluationVariationError(EvaluationError):
    """An exception type for when evaluation of an expression will not vary.

    Let's see an example where we attempt to make a :class:`TruthTable \
    <tt.tables.truth_table.TruthTable>` from an expression that has no
    symbols nor variation in its results::

        >>> from tt import TruthTable
        >>> t = TruthTable('1 or 0')
        Traceback (most recent call last):
            ...
        tt.errors.evaluation.NoEvaluationVariationError: This expression is \
composed only of constant values

    """
