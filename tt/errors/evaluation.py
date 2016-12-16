"""Exception type definitions related to expression evaluation."""

from .base import TtError


class EvaluationError(TtError):

    """An exception type for errors occurring in expression evaluation.

    Notes:
        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    pass


class ExtraSymbolError(EvaluationError):

    """Exception for a passed token that is not a symbol in the expression."""

    pass


class InvalidBooleanValueError(EvaluationError):

    """Exception for an invalid truth value passed in evaluation."""

    pass


class MissingSymbolError(EvaluationError):

    """An exception type for a missing token value in evaluation."""

    pass
