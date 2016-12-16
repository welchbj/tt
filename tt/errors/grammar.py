"""Exception type definitions related to expression grammar and parsing."""

from .base import TtError


class GrammarError(TtError):

    """Base type for errors that occur in the handling of expression.

    Attributes:
        message (str): An additional helpful message that could be displayed
            to the user to better explain the error.
        expr_str (str, optional): The expression in which the grammar error
            occured; can be left as ``None`` if the error position will not
            be specified.
        error_pos (int, optional): The index indicating at which position int
            ``expr_str`` the troublesome spot began; can be left as ``None``
            for errors without a specific troublesome position.

    Notes:
        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    def __init__(self, message, expr_str=None, error_pos=None, *args):
        self.message = message
        self.expr_str = expr_str
        self.error_pos = error_pos
        super(GrammarError, self).__init__(self.message, *args)


class BadParenPositionError(GrammarError):

    """An exception type for unexpected parentheses."""

    pass


class EmptyExpressionError(GrammarError):

    """An exception type for when an empty expression is received."""

    pass


class ExpressionOrderError(GrammarError):

    """An exception type for unexpected operands or operators."""

    pass


class UnbalancedParenError(GrammarError):

    """An exception type for unbalanced parentheses."""

    pass
