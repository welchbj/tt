"""Tools for interacting with Boolean expressions."""

import re

from ..definitions import (CONSTANT_VALUES, DELIMITERS, is_valid_identifier,
                           OPERATOR_MAPPING, TT_NOT_OP)
from ..errors import (BadParenPositionError, EmptyExpressionError,
                      ExpressionOrderError, InvalidArgumentTypeError,
                      InvalidIdentifierError, UnbalancedParenError)
from ..trees import BooleanExpressionTree
from ..utils import (assert_all_valid_keys,
                     assert_iterable_contains_all_expr_symbols)


class BooleanExpression(object):

    """An interface for interacting with a Boolean expression.

    Instances of ``BooleanExpression`` are meant to be immutable.

    """

    def __init__(self, raw_expr):
        if not isinstance(raw_expr, str):
            raise InvalidArgumentTypeError('raw_expr must be of type str')

        self._raw_expr = raw_expr

        self._symbols = []
        self._symbol_set = set()

        self._tokens = []
        self._postfix_tokens = []

        self._tokenize()
        self._to_postfix()

        self._tree = BooleanExpressionTree(self._postfix_tokens)

    @property
    def raw_expr(self):
        """The raw string expression, parsed upon initialization.

        This is what you pass into the ``BooleanExpression`` constructor; it is
        kept on the object as an attribute for convenience.

        :type: :class:`str <python:str>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A nand B')
            >>> b.raw_expr
            'A nand B'

        """
        return self._raw_expr

    @property
    def symbols(self):
        """The list of unique symbols present in this expression.

        The order of the symbols in this list matches the order of symbol
        appearance in the original expression.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.symbols
            ['A', 'B', 'C']

        """
        return self._symbols

    @property
    def tokens(self):
        """The parsed, non-whitespace tokens of an expression.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.tokens
            ['A', 'xor', '(', 'B', 'or', 'C', ')']

        """
        return self._tokens

    @property
    def postfix_tokens(self):
        """Similar to the ``tokens`` attribute, but in postfix order.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.postfix_tokens
            ['A', 'B', 'C', 'or', 'xor']

        """
        return self._postfix_tokens

    @property
    def tree(self):
        """The expression tree representing this Boolean expression.

        :type: :class:`BooleanExpressionTree
                       <tt.trees.expr_tree.BooleanExpressionTree>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> print(b.tree)
            xor
            `----A
            `----or
                 `----B
                 `----C

        """
        return self._tree

    def __str__(self):
        return '<BooleanExpression "{}">'.format(self._raw_expr)

    def evaluate(self, **kwargs):
        """Evaluate the Boolean expression for the passed keyword arguments.

        This is a checked wrapper around the :func:`evaluate_unchecked`
        function.

        :param kwargs: Keys are names of symbols in this expression; the
            specified value for each of these keys will be substituted into the
            expression for evaluation.

        :returns: The result of evaluating the expression.
        :rtype: :class:`bool <python:bool>`

        :raises ExtraSymbolError: If a symbol not in this expression is passed
            through ``kwargs``.
        :raises MissingSymbolError: If any symbols in this expression are not
            passed through ``kwargs``.
        :raises InvalidBooleanValueError: If any values from ``kwargs`` are not
            valid Boolean inputs.
        :raises InvalidIdentifierError: If any symbol names are invalid
            identifier.

        .. note::

            See :func:`assert_all_valid_keys\
            <tt.utils.assertions.assert_all_valid_keys>` and
            :func:`assert_iterable_contains_all_expr_symbols\
            <tt.utils.assertions.assert_iterable_contains_all_expr_symbols>`
            for more information about the exceptions raised by this method.

        Usage::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A or B')
            >>> b.evaluate(A=0, B=0)
            False
            >>> b.evaluate(A=1, B=0)
            True

        """
        assert_all_valid_keys(kwargs, self._symbol_set)
        assert_iterable_contains_all_expr_symbols(kwargs.keys(),
                                                  self._symbol_set)

        return self.evaluate_unchecked(**kwargs)

    def evaluate_unchecked(self, **kwargs):
        """Evaluate the Boolean expression without checking the input.

        This is used for evaluation by the :func:`evaluate` method, which
        validates the input ``kwargs`` before passing them to this method.

        :param kwargs: Keys are names of symbols in this expression; the
            specified value for each of these keys will be substituted into the
            expression for evaluation.

        :returns: The Boolean result of evaluating the expression.
        :rtype: :class:`bool <python:bool>`

        """
        truthy = self._tree.evaluate(kwargs)
        return bool(truthy)

    def _tokenize(self):
        """Make the first pass through the expression, tokenizing it.

        This method will populate the ``symbols`` and ``tokens`` attributes,
        and is the first step in the expression-processing pipeline.

        :raises GrammarError: If a malformed expression is received.

        """
        operator_strs = [k for k in OPERATOR_MAPPING.keys()]
        is_symbolic = {op: not op[0].isalpha() for op in operator_strs}
        operator_search_list = sorted(operator_strs, key=len, reverse=True)
        delimiters = DELIMITERS | set(k[0] for k, v in is_symbolic.items()
                                      if v)
        EXPECTING_OPERAND = 1
        EXPECTING_OPERATOR = 2
        grammar_state = EXPECTING_OPERAND

        idx = 0
        open_paren_count = 0
        num_chars = len(self.raw_expr)

        while idx < num_chars:
            c = self.raw_expr[idx].strip()

            if not c:
                # do nothing
                idx += 1
            elif c == '(':
                if grammar_state != EXPECTING_OPERAND:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self.raw_expr, idx)

                open_paren_count += 1
                self._tokens.append(c)
                idx += 1
            elif c == ')':
                if grammar_state != EXPECTING_OPERATOR:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self.raw_expr, idx)
                elif not open_paren_count:
                    raise UnbalancedParenError('Unbalanced parenthesis',
                                               self.raw_expr, idx)

                open_paren_count -= 1
                self._tokens.append(c)
                idx += 1
            else:
                is_operator = False
                num_chars_remaining = num_chars - idx

                matching_operators = [
                    operator for operator in operator_search_list
                    if len(operator) <= num_chars_remaining and
                    self.raw_expr[idx:(idx+len(operator))] == operator]

                if matching_operators:
                    match = matching_operators[0]
                    match_length = len(match)
                    next_c_pos = idx + match_length
                    next_c = (None if next_c_pos >= num_chars else
                              self.raw_expr[idx + match_length])

                    if next_c is None:
                        # trailing operator
                        raise ExpressionOrderError(
                            'Unexpected operator "{}"'.format(match),
                            self.raw_expr, idx)

                    if next_c in delimiters or is_symbolic[match]:
                        if OPERATOR_MAPPING[match] == TT_NOT_OP:
                            if grammar_state != EXPECTING_OPERAND:
                                raise ExpressionOrderError(
                                    'Unexpected unary operator "{}"'.format(
                                        match), self.raw_expr, idx)
                        else:
                            if grammar_state != EXPECTING_OPERATOR:
                                raise ExpressionOrderError(
                                    'Unexpected binary operator "{}"'.format(
                                        match), self.raw_expr, idx)
                            grammar_state = EXPECTING_OPERAND

                        is_operator = True
                        self._tokens.append(match)
                        idx += match_length

                if not is_operator:
                    if grammar_state != EXPECTING_OPERAND:
                        raise ExpressionOrderError('Unexpected operand',
                                                   self.raw_expr, idx)

                    operand_end_idx = idx + 1
                    while (operand_end_idx < num_chars and
                           self.raw_expr[operand_end_idx] not in delimiters):
                        operand_end_idx += 1

                    operand = self.raw_expr[idx:operand_end_idx]
                    if (operand not in CONSTANT_VALUES and
                            not is_valid_identifier(operand)):
                        raise InvalidIdentifierError(
                            'Invalid operand name "{}"'.format(operand),
                            self.raw_expr, idx)

                    self._tokens.append(operand)
                    if operand not in (self._symbol_set | CONSTANT_VALUES):
                        self._symbols.append(operand)
                        self._symbol_set.add(operand)

                    idx = operand_end_idx
                    grammar_state = EXPECTING_OPERATOR

        if open_paren_count:
            left_paren_positions = [m.start() for m in
                                    re.finditer(r'\(', self.raw_expr)]
            raise UnbalancedParenError(
                'Unbalanced left parenthesis', self.raw_expr,
                left_paren_positions[open_paren_count-1])

        if not self._tokens:
            raise EmptyExpressionError('Empty expression is invalid')

    def _to_postfix(self):
        """Populate the ``postfix_tokens`` attribute."""
        operand_set = self._symbol_set | CONSTANT_VALUES
        stack = []

        for token in self._tokens:
            if token in operand_set:
                self._postfix_tokens.append(token)
            elif token == '(':
                stack.append(token)
            elif token in OPERATOR_MAPPING.keys():
                if not stack:
                    stack.append(token)
                else:
                    while (stack and stack[-1] != '(' and
                            OPERATOR_MAPPING[stack[-1]].precedence >
                            OPERATOR_MAPPING[token].precedence):
                        self._postfix_tokens.append(stack.pop())
                    stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    self._postfix_tokens.append(stack.pop())
                stack.pop()

        for token in reversed(stack):
            self._postfix_tokens.append(token)
