"""A module for extracting and manipulating information from Boolean equations.
"""

import itertools

from tt.utils import print_err, without_spaces, matching_indices
from tt.schema_provider import (schema, schema_search_ordered_list, SYM_NOT,
                                SYM_XOR)

__all__ = ['EvaluationResultWrapper',
           'BooleanEquationWrapper',
           'infix_to_postfix',
           'eval_postfix_expr',
           'TooManySymbolsError',
           'GrammarError',
           'ExpressionOrderError',
           'BadParenPositionError',
           'BadSymbolError']


# === Wrapper Classes =========================================================
class EvaluationResultWrapper(object):

    """A simple wrapper around the evaluation results of a Boolean equation.

    Attributes:
        input_symbols (List[str]): The equation's input symbols, *not* the
            single character mappings used in``BooleanEquationWrapper``.
        output_symbol (str): The equation's output symbol.
        result_list (List[str]): The list of results of evaluations to be
            filled with ``'0'`` and ``'1'``.

    """

    def __init__(self, input_symbols, output_symbol):
        self.input_symbols = input_symbols
        self.output_symbol = output_symbol
        self.result_list = []

    def get_num_evaluations(self):
        """Determine the number of evaluations that will fill this instance.

        Returns:
            int: The number of possible input combinations. This is simply
                2 raised to the power of the number of inputs.

        """
        return 2**len(self.input_symbols)

    def get_high_indices(self):
        """Get the indices for which the result is high.

        Returns:
            List[int]: The list of indices where the result is high.

        """
        return matching_indices(self.result_list, 1)

    def get_low_indices(self):
        """Get the indices for which the result is low.

        Returns:
            List[int]: The list of indices where the result is low.

        """
        return matching_indices(self.result_list, 0)


class BooleanEquationWrapper(object):

    """A wrapper of a Boolean equation, with parsing/evaluation functionality.

    Args:
        raw_bool_eq (str): The Boolean equation to act on. Assumed to be user
            input, meaning any malformed equations are possible values.

    Attributes:
        unique_symbols_left (List[str]): The remaining single character
            symbols that variable words can be mapped to.
        unique_symbol_to_var_name_dict (dict{str:str}): The mapping of
            individual characters to equivalent variable words from
            ``raw_bool_eq``.
        pos_to_condensed_magnitude_map (dict{int:int}): The mapping of position
            in ``condensed_infix_expr`` to the number of characters that were
            condensed at that position.
        output_symbol (str): The symbol/word to the left of the equals sign in
            ``raw_bool_eq``.
        infix_expr (str): The Boolean expression to the right of the equals
            sign in ``raw_bool_eq``
        condensed_infix_expr (str): A transformation of ``infix_expr``, with
            all variable words mapped to single characters and tracked in
            ``unique_symbol_to_var_name_dict``.
        postfix_expr (str): A transformation of ``infix_expr`` to postfix form.
        eval_result (EvaluationResultWrapper): The result of evaluating this
            equation at each possible combination of its inputs.

    """

    def __init__(self, raw_bool_eq):
        self.unique_symbols_left = list(reversed('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        self.unique_symbol_to_var_name_dict = {}
        self.pos_to_condensed_magnitude_map = {}

        self.output_symbol, self.infix_expr = \
            extract_output_sym_and_expr(raw_bool_eq)
        self.condensed_infix_expr = self.condense_expression(self.infix_expr)
        self.postfix_expr = infix_to_postfix(
            self.condensed_infix_expr, self.get_unique_symbol_list())

        # right now, the only time that this class is invoked is when we need
        # the evaluation result; if this changes, the below computation should
        # not be done in __init__
        self.eval_result = self.get_evaluation_result()

    def get_input_symbol_list(self):
        """Get the list of input symbols contained within this equation.

        Returns:
            List[str]: The input symbols sorted by their appearance in the
                ``raw_bool_eq`` arg passed to ``__init__``.
        """
        return [self.unique_symbol_to_var_name_dict[key]
                for key in self.get_unique_symbol_list()]

    def get_unique_symbol_list(self):
        """Get unique symbols to which the variable words are mapped

        Returns:
            List[str]: Sorted list of the unique, single-character values to
                which the variable words in ``infix_expr`` are mapped.

        """
        return sorted(self.unique_symbol_to_var_name_dict.keys())

    def get_unique_symbol(self, var_name):
        """Get a unique symbol mapped to ``var_name``.

        If ``var_name`` has not yet been mapped to, then a new unique
        character will be popped off of ``unique_symbols_left``. Otherwise,
        the already-mapped character will be retrieved from
        ``unique_symbol_to_var_name_dict``.

        Args:
            var_name (str): The variable name to which to map.

        Returns:
            str: The unique symbol to which ``var_name`` is mapped.

        """
        if not self.unique_symbols_left:
            raise TooManySymbolsError('Cannot process equation of more than '
                                      '26 symbols.')
        elif var_name in self.unique_symbol_to_var_name_dict.values():
            # all values should be unique, so we should be safe to assume this
            # list comprehension will yield one element
            return [key for key, val
                    in self.unique_symbol_to_var_name_dict.items()
                    if val == var_name][0]
        else:
            unique_symbol = self.unique_symbols_left.pop()
            self.unique_symbol_to_var_name_dict[unique_symbol] = var_name
            return unique_symbol

    def get_evaluation_result(self):
        """Get the evaluation of this Boolean equation.

        Returns:
            ``EvaluationResultWrapper``: An instance containing the result of
                the evaluation of this Boolean equation at each combination of
                its inputs, as defined by the contents of ``input_symbols``.

        """
        eval_result_wrapper = EvaluationResultWrapper(
            self.get_input_symbol_list(), self.output_symbol)

        replaceable_expr = self.postfix_expr
        input_symbols = self.get_unique_symbol_list()

        for i, sym in enumerate(input_symbols):
            replaceable_expr = replaceable_expr.replace(sym, '{'+str(i)+'}')

        exprs_to_eval = (replaceable_expr.format(*input_row) for
                         input_row in get_symbol_input_array(input_symbols))

        for expr in exprs_to_eval:
            result = eval_postfix_expr(expr)
            eval_result_wrapper.result_list.append(result)

        return eval_result_wrapper

    def condense_expression(self, raw_infix_expr):
        """The core functionality of `BooleanEquationWrapper``.

        This function replaces all variable words in ``raw_infix_expr`` with
        single-character mappings as well as all operation words/symbols with
        the single-character equivalent defined in the tt schema.

        After this initial condensing phase, syntax checking is performed on
        the condensed expression, raising a number of possible exceptions
        descending from ``GrammarError``.

        Notes:
            This function changes the state of
            ``unique_symbol_to_var_name_dict`` and
            ``pos_to_condensed_magnitude_map``.

        Args:
            raw_infix_expr: The expression which will be condensed, in both its
                variable words and operation symbols.

        Returns:
            str: The condensed form of ``raw_infix_expr``.

        Raises:
            BadSymbolError: Raise if an invalid symbol is detected, i.e. an *
                found within a variable word.
            BadParenPositionError: Raise if a parenthesis is found somewhere
                unexpected, i.e. a left parenthesis following an operand.
            UnbalancedParenError: Raise if unbalanced parentheses are detected
                in the syntax checking phase.
            ExpressionOrderError: Raise if leading or trailing operation,
                consecutive operands, or consecutive non-NOT operations are
                detected in the syntax checking phase.

        """
        condensed_expr = raw_infix_expr
        curr_idx = 0
        left_paren_positions = []
        right_paren_positions = []

        while curr_idx < len(condensed_expr):
            c = condensed_expr[curr_idx].strip()
            if not c:
                pass
            elif c == '(':
                left_paren_positions.append(curr_idx)
            elif c == ')':
                right_paren_positions.append(curr_idx)
            else:
                is_operation = False
                for tt_operation_symbol in schema_search_ordered_list:
                    # assume this list is pre-ordered by length in
                    # schema_provider
                    equivalent_symbols = (
                        schema[tt_operation_symbol].equivalent_symbols)

                    operation_symbol_lens = [len(equivalent_symbol)
                                             for equivalent_symbol
                                             in equivalent_symbols]

                    test_idxs = [curr_idx+operation_symbol_len
                                 for operation_symbol_len
                                 in operation_symbol_lens]

                    possible_matches = [condensed_expr[curr_idx:test_idx]
                                        if test_idx <= len(condensed_expr)
                                        else ''
                                        for test_idx in test_idxs]

                    matches = [possible_match
                               for operation_symbol, possible_match
                               in zip(equivalent_symbols, possible_matches)
                               if operation_symbol == possible_match]

                    if matches:
                        match = matches[0]
                        matched_idx = possible_matches.index(match)
                        replacement_idx = test_idxs[matched_idx]

                        if (replacement_idx < len(condensed_expr) and
                                match[-1].isalpha() and
                                condensed_expr[replacement_idx] not in
                                [' ', '(']):
                            # this is just an operand that begins with one of
                            # the tt schema symbols; we can break out of this
                            # because no operation symbols for different
                            # operations start with the same character sequence
                            # as another symbol
                            break

                        self.pos_to_condensed_magnitude_map[curr_idx] = (
                            len(match) - len(tt_operation_symbol))
                        condensed_expr = (
                            condensed_expr[:curr_idx] + tt_operation_symbol +
                            condensed_expr[replacement_idx:])
                        is_operation = True
                        break

                if not is_operation:
                    if c.isalpha():  # operand names must start with letter
                        # parse the variable name
                        test_idx = curr_idx + 1
                        while (test_idx < len(condensed_expr) and
                               is_valid_operand_char_non_leading(
                               condensed_expr[test_idx])):
                            test_idx += 1

                        var_name = condensed_expr[curr_idx:test_idx]
                        if var_name == self.output_symbol:
                            raise BadSymbolError(
                                self.infix_expr,
                                self.get_expanded_position(curr_idx),
                                'Output symbol used as an input variable in '
                                'your expression.')

                        unique_symbol = self.get_unique_symbol(var_name)

                        condensed_expr = (
                            condensed_expr[:curr_idx] + unique_symbol +
                            condensed_expr[test_idx:])
                        self.pos_to_condensed_magnitude_map[curr_idx] = (
                            len(var_name) - len(unique_symbol))
                    elif c in ['0', '1']:
                        pass
                    else:
                        raise BadSymbolError(
                            self.infix_expr,
                            self.get_expanded_position(curr_idx),
                            'Invalid symbol.')
            curr_idx += 1

        # Syntax checking is done in a post-processing of the condensed
        # expression

        NEXT_STATE_OPERAND = 0
        NEXT_STATE_OPERATION = 1

        left_paren_pos_stack = []
        next_state = NEXT_STATE_OPERAND
        for pos, c in enumerate(condensed_expr):
            if not c.strip():
                continue
            elif c == '(':
                if next_state != NEXT_STATE_OPERAND:
                    raise BadParenPositionError(
                        self.infix_expr, self.get_expanded_position(pos),
                        'Unexpected parenthesis.')
                else:
                    left_paren_pos_stack.append(pos)
            elif c == ')':
                if next_state != NEXT_STATE_OPERATION:
                    raise BadParenPositionError(
                        self.infix_expr, self.get_expanded_position(pos),
                        'Unexpected parenthesis.')
                else:
                    if not left_paren_pos_stack:
                        raise UnbalancedParenError(
                            self.infix_expr, self.get_expanded_position(pos),
                            'Unbalanced right parenthesis.')
                    else:
                        left_paren_pos_stack.pop()
            elif c in self.get_unique_symbol_list() or c in ['0', '1']:
                if next_state != NEXT_STATE_OPERAND:
                    raise ExpressionOrderError(
                        self.infix_expr, self.get_expanded_position(pos),
                        'Unexpected operand.')
                else:
                    next_state = NEXT_STATE_OPERATION
            else:
                if pos == len(condensed_expr) - 1:
                    raise ExpressionOrderError(
                        self.infix_expr, self.get_expanded_position(pos),
                        'Unexpected operation.')
                elif c == SYM_NOT:
                    if next_state != NEXT_STATE_OPERAND:
                        raise ExpressionOrderError(
                            self.infix_expr, self.get_expanded_position(pos),
                            'Unexpected operation.')
                else:
                    if next_state != NEXT_STATE_OPERATION:
                        raise ExpressionOrderError(
                            self.infix_expr, self.get_expanded_position(pos),
                            'Unexpected operation.')
                    else:
                        next_state = NEXT_STATE_OPERAND

        if left_paren_pos_stack:
            raise UnbalancedParenError(
                self.infix_expr,
                self.get_expanded_position(left_paren_pos_stack[0]),
                'Unbalanced left parenthesis.')

        condensed_expr = condensed_expr.replace(SYM_NOT, '1' + SYM_XOR)

        return without_spaces(condensed_expr)

    def get_expanded_position(self, at_pos):
        """Get the position of ``at_pos`` in the non-condensed expression.

        The infix expression is condensed in ``condense_expr``, but nice error
        messages need to display the position of the error to the user in their
        originally entered expression. To do this, the 'condense history'
        before at_pos is considered the offset of at_pos from its equivalent
        position in ``raw_infix_expr``. This function returns the 'uncondensed'
        position.

        Args:
            at_pos (int): The position at which to determine the expanded
                position.

        Returns:
            int: The expanded position of ``at_pos`` in ``raw_infix_expr``.

        """
        offset = sum(
            [mag for pos, mag in self.pos_to_condensed_magnitude_map.items()
             if pos < at_pos])
        return offset + at_pos


# === Equation Manipulation Free Functions ====================================
def infix_to_postfix(infix_expr, symbol_list):
    """Convert the passed infix expression into its postfix form.

    This conversion allows for simpler evaluation later on in the program flow.
    Uses the Shunting-yard Algorithm.

    Args:
        infix_expr (str): An infix expression that has been run through
            ``condense_expr``. It is assumed to contain any operations except
            for Boolean NOT, which should have been replaced with 1 XOR earlier
            in the program flow.
        symbol_list (List[str]): The list of single-character string symbols
            existing in ``infix_expr``.

    Returns:
        str: The equivalent postfix expression to ``infix_expr``.

    """
    stack = []
    postfix = []
    operators = schema.keys()

    for c in infix_expr:
        if c in symbol_list or c in ['0', '1']:
            postfix += c
        elif c == '(':
            stack += c
        elif c in operators:
            if not stack:
                stack += c
            else:
                while (stack and stack[-1] != '(' and
                       schema[stack[-1]].precedence > schema[c].precedence):
                    postfix += stack.pop()
                stack += c
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()

    for c in reversed(stack):
        postfix += c

    return ''.join(postfix)


def extract_output_sym_and_expr(eq):
    """Parse the passed Boolean equation about its equals sign.

    Assume the left side of the equation is the output variable and the right
    side is the equivalent expression.

    Args:
        eq (str): The Boolean equation to split.

    Returns:
        output_sym (str): The output symbol.
        expr (str): The Boolean expression.

    Raises:
        BadSymbolError: Raise if no equals signs present or more than one
            equals sign present.

    """
    output_and_expr = eq.split('=')

    if len(output_and_expr) == 1:
        raise BadSymbolError(eq, -1, 'Equation did not contain equals sign.')
    elif len(output_and_expr) > 2:
        error_pos = eq.index('=', eq.index('=')+1)
        raise BadSymbolError(eq, error_pos, 'Unexpected equals sign.')

    output_sym, expr = output_and_expr[0].strip(), output_and_expr[1].strip()
    return output_sym, expr


def eval_postfix_expr(expr_to_eval):
    """Evaluate the passed postfix expression.

    Args:
        expr_to_eval (str): A string postfix expression, containing only '0's,
            '1's, and single character operations. Assume to be well-formed.

    Returns:
        int: The result of the evaluation, as 0 or 1.

    """
    stack = []

    for c in expr_to_eval:
        if c in ['0', '1']:
            stack.append(int(c))
        else:
            stack.append(schema[c].bool_func(stack.pop(), stack.pop()))
    return stack[0]


# === Utility Free Functions ==================================================
def get_symbol_input_array(sym_list):
    return itertools.product(['0', '1'], repeat=len(sym_list))


# === Grammar-related rules ===================================================
def is_valid_operand_char_non_leading(c):
    return c == '_' or c.isalnum()


# === Custom exception types ==================================================
class TooManySymbolsError(Exception):

    """Error for when too many symbols were in the user's equation.

    Because user-entered variable names are mapped to single characters for
    the evaluation of Boolean equations in ``BooleanEquationWrapper``, there
    are a finite and controlled set of valid symbols to which the mapping is
    done. Currently, this is just the set of capital alphabetic characters
    (i.e., A-Z). tt becomes unusably slow when 26 variables are entered in an
    equation anyways, so there is currently no need to expand the set of
    symbols beyond its current capacity of 26.

    """

    pass


class GrammarError(Exception):

    """Error for problems in equation parsing.

    This error type adds information for indicating the expression or
    equation that raised the error to the base Exception class.

    Notes:
        This error type is meant to be subclassed and should not be
        raised directly.

    """

    def __init__(self, expr_or_equation, error_pos, message, *args):
        self.expr_or_equation = expr_or_equation
        self.error_pos = error_pos
        self.message = message
        super(GrammarError, self).__init__(self.message, *args)

    def log(self):
        """Output an informative error message to the log.

        Outputs the error message, as well as the problemed expression/equation
        with the error position indicated, if a valid non-negative position is
        passed.

        Returns:
            None

        """
        print_err(self.message)
        if self.error_pos >= 0:
            print_err(self.expr_or_equation)
            print_err(' ' * self.error_pos + '^')


class BadSymbolError(GrammarError):

    """Error for an unexpected symbol in variable names or operation words.

    Examples:
        Leading with an underscore::

            'F = _A or B'

        Containing a forbidden symbol::

            'F = opera*nd1 or operand2'

    """

    pass


class ExpressionOrderError(GrammarError):

    """Error for bad order of operands/operations.

    Examples:
        Consecutive operations::

            "F = A and and B"

        Consecutive operands::

            "F = A A or B"

    """

    pass


class BadParenPositionError(GrammarError):

    """Error for improper positioning of parentheses.

    Examples:

        TODO

    """

    pass


class UnbalancedParenError(GrammarError):

    """Error for improper balancing of parentheses.

    Examples:
        Too many left parentheses::

            "F = A or ((B and C)"

        Too many right parentheses::

            "F = (A and B)) or C"

    """

    pass
