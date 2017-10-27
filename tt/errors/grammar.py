"""Exception type definitions related to expression grammar and parsing."""

from .base import TtError


class GrammarError(TtError):

    """Base type for errors that occur in the handling of expression. This
    exception type should be sub-classed and is not meant to be raised
    explicitly.

    """

    def __init__(self, message, expr_str=None, error_pos=None, *args):
        self._expr_str = expr_str
        self._error_pos = error_pos
        super(GrammarError, self).__init__(message, *args)

    @property
    def expr_str(self):
        """The expression in which the exception occurred.

        If this property is left as ``None``, the expression will not be
        propagated with the exception.

        :type: :class:`str <python:str>`

        """
        return self._expr_str

    @property
    def error_pos(self):
        """The position in the expression where the error occurred.

        If this property is left as ``None``, it can be assumed that there is
        no specific location in the expression causing the exception.

        :type: :class:`int <python:int>`

        """
        return self._error_pos


class BadParenPositionError(GrammarError):
    """An exception type for unexpected parentheses.

    Here's a quick and dirty example::

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A or B (')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.BadParenPositionError: Unexpected parenthesis

    """


class EmptyExpressionError(GrammarError):
    """An exception type for when an empty expression is received.

    Let's take a brief look::

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.EmptyExpressionError: Empty expression is invalid

    """


class ExpressionOrderError(GrammarError):
    """An exception type for unexpected operands or operators.

    Here's an example with an unexpected operator::

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A or or B')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.ExpressionOrderError: Unexpected binary operator "or"

    """


class InvalidIdentifierError(GrammarError):
    """An exception type for invalid operand names. Invalid operand names are
    determined via the :func:`is_valid_identifier \
    <tt.definitions.operands.is_valid_identifier>` function.

    Here are a couple of examples, for both expressions and tables::

        >>> from tt import BooleanExpression, TruthTable
        >>> b = BooleanExpression('__A xor B')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.InvalidIdentifierError: Invalid operand name "__A"
        >>> t = TruthTable(from_values='0x11', ordering=['for', 'operand'])
        Traceback (most recent call last):
            ...
        tt.errors.grammar.InvalidIdentifierError: "for" in ordering is not a \
    valid symbol name

    """


class UnbalancedParenError(GrammarError):
    """An exception type for unbalanced parentheses.

    Here's a short example::

        >>> from tt import BooleanExpression
        >>> b = BooleanExpression('A or B or C)')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.UnbalancedParenError: Unbalanced parenthesis

    """
