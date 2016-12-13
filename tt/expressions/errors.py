"""Error definitions related to parsing expressions."""


class GrammarError(Exception):

    """Base error for errors that occur in the handling of expression.

    Attributes:
        message (str): An additional helpful message that could be displayed
            to the user to better explain the error.
        expr_str (str): The expression in which the grammar error occured.
        error_pos (int): The index indicating at which position in ``expr_str``
            the troublesome spot began.

    Notes:
        This error should be sub-classed, and is not meant to be raised
        directly.

    """

    def __init__(self, message, expr_str, error_pos, *args):
        self.message = message
        self.expr_str = expr_str
        self.error_pos = error_pos
        super(GrammarError, self).__init__(self.message, *args)


class ExpressionOrderError(GrammarError):

    """An exception for unexpected operands or operators."""

    pass


class BadParenPositionError(GrammarError):

    """An exception for unexpected parentheses."""

    pass


class UnbalancedParenError(GrammarError):

    """An exception for unbalanced parentheses."""

    pass
