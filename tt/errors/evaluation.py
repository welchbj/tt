"""Exception type definitions related to expression evaluation."""


class EvaluationError(Exception):

    """Base type for errors that occur in the evaluation of an expression.

    Attributes:
        message (str): An additional helpful message that could be displayed
            to the user to better explain the error.

    Notes:
        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    def __init__(self, message, *args):
        self.message = message
        super(EvaluationError, self).__init__(self.message, *args)


class ExtraSymbolError(EvaluationError):

    """Exception for a passed token that is not a symbol in the expression."""

    pass


class InvalidBooleanValueError(EvaluationError):

    """Exception for an invalid truth value passed in evaluation."""

    pass


class MissingSymbolError(EvaluationError):

    """An exception type for a missing token value in evaluation."""

    pass
