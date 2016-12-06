"""Tools for interacting with Boolean expressions."""

import re

from ..operators import OPERATOR_MAPPING, TT_NOT_OP
from .errors import (BadParenPositionError, ExpressionOrderError,
                     UnbalancedParenError)


class BooleanExpression(object):

    """A class for parsing and holding information about a Boolean expression.

    Attributes:
        raw_expr (str): The raw string expression, to be parsed upon
            initialization.
        symbols (List[str]): The list of unique symbols present in
            this expression.
        tokens (List[str]): A list of strings, each element indicating
            a different token of the parsed expression.
        expr_tree_root (TODO): TODO

    """

    def __init__(self, raw_expr):
        self.raw_expr = raw_expr

        self.symbols = []
        self.tokens = []
        self.expr_tree_root = None  # TODO

        self._tokenize()
        self._build_expr_tree()

    def _tokenize(self):
        """Make the first pass through the expression, tokenizing it.

        This method will populate the ``symbols`` and ``tokens`` attributes,
        and is the first step in the expression-processing pipeline.

        """
        operator_strs = [k for k in OPERATOR_MAPPING.keys()]
        is_symbolic = {op: not op[0].isalpha() for op in operator_strs}
        operator_search_list = sorted(operator_strs, key=len, reverse=True)
        delimiters = {' ', '(', ')'} | set(k[0] for k, v in is_symbolic.items()
                                           if v)
        constant_values = {'0', '1'}
        parsed_operands = set()

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
                self.tokens.append(c)
                idx += 1
            elif c == ')':
                if grammar_state != EXPECTING_OPERATOR:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self.raw_expr, idx)
                elif not open_paren_count:
                    raise UnbalancedParenError('Unbalanced parenthesis',
                                               self.raw_expr, idx)

                open_paren_count -= 1
                self.tokens.append(c)
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
                        self.tokens.append(match)
                        idx += match_length

                if not is_operator:
                    if grammar_state != EXPECTING_OPERAND:
                        raise ExpressionOrderError('Unexpected operator',
                                                   self.raw_expr, idx)

                    operand_end_idx = idx + 1
                    while (operand_end_idx < num_chars and
                           self.raw_expr[operand_end_idx] not in delimiters):
                        operand_end_idx += 1

                    operand = self.raw_expr[idx:operand_end_idx]
                    self.tokens.append(operand)
                    if operand not in (parsed_operands | constant_values):
                        self.symbols.append(operand)
                        parsed_operands.add(operand)

                    idx = operand_end_idx
                    grammar_state = EXPECTING_OPERATOR

        if open_paren_count:
            left_paren_positions = [m.start() for m in
                                    re.finditer(r'\(', self.raw_expr)]
            raise UnbalancedParenError(
                'Unbalanced left parenthesis', self.raw_expr,
                left_paren_positions[open_paren_count-1])

    def _build_expr_tree(self):
        pass