"""Exception type definitions related to expression grammar and parsing."""

from .base import TtError


class GrammarError(TtError):

    """Base type for errors that occur in the handling of expression.

    .. note::

        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """

    def __init__(self, message, expr_str=None, error_pos=None, *args):
        self._expr_str = expr_str
        self._error_pos = error_pos
        super(GrammarError, self).__init__(message, *args)

    @property
    def expr_str(self):
        """The expression in which the exception occurred.

        .. note::

            This may be left as ``None``, in which case the expression will not
            be propagated with the exception.

        :type: :class:`str <python:str>`

        """
        return self._expr_str

    @property
    def error_pos(self):
        """The position in the expression where the error occurred.

        .. note::

            This may be left as ``None``, in which case there is no specific
            location in the expression causing the exception.

        :type: :class:`int <python:int>`

        """
        return self._error_pos


class BadParenPositionError(GrammarError):
    """An exception type for unexpected parentheses.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression(') A or B')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.grammar.BadParenPositionError'>

    """


class EmptyExpressionError(GrammarError):
    """An exception type for when an empty expression is received.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.grammar.EmptyExpressionError'>

    """


class ExpressionOrderError(GrammarError):
    """An exception type for unexpected operands or operators.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('A or or B')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.grammar.ExpressionOrderError'>

    """


class InvalidIdentifierError(GrammarError):
    """An exception type for invalid operand names.

    .. code-block:: python

        >>> from tt import BooleanExpression, TruthTable
        >>> b = BooleanExpression('%A or B')
        Traceback (most recent call last):
            ...
        tt.errors.grammar.InvalidIdentifierError: Invalid operand name "%A"
        >>> t = TruthTable(from_values='0x11', ordering=['A', 'while'])
        Traceback (most recent call last):
            ...
        tt.errors.grammar.InvalidIdentifierError: "while" in ordering is not \
a valid symbol name

    """


class UnbalancedParenError(GrammarError):
    """An exception type for unbalanced parentheses.

    .. code-block:: python

        >>> from tt import BooleanExpression
        >>> try:
        ...     b = BooleanExpression('A or ((B)')
        ... except Exception as e:
        ...     print(type(e))
        ...
        <class 'tt.errors.grammar.UnbalancedParenError'>

    """
