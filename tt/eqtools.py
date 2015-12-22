"""
A module for extracting and manipulating information from Boolean equations.
"""

import logging as log
import itertools

from enum import Enum

from utils import without_spaces
from schema_provider import schema, schema_search_ordered_list
from schema_provider import SYM_NOT, SYM_XOR


# === Wrapper Classes =========================================================
class EvaluationResultWrapper(object):
    def __init__(self, input_symbols, output_symbol):
        self.input_symbols = input_symbols
        self.output_symbol = output_symbol
        self.result_list = []

    def get_num_evaluations(self):
        return 2**len(self.input_symbols)


class BooleanEquationWrapper(object):
    def __init__(self, raw_bool_eq):
        self.unique_symbols_left = list(reversed("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.unique_symbol_to_var_name_dict = {}
        self.pos_to_condensed_magnitude_map = {}

        self.output_symbol, self.infix_expr = (
            extract_output_sym_and_expr(raw_bool_eq))
        self.condensed_infix_expr = self.condense_expression(self.infix_expr)
        self.postfix_expr = infix_to_postfix(
            self.condensed_infix_expr, self.get_unique_symbol_list())

    def get_input_symbol_list(self):
        """
        Get the list of input symbols contained within this equation.

        Returns:
            The list of input symbols of the equation as strings, sorted by
            their order of appearance in the equation.
        """
        return [self.unique_symbol_to_var_name_dict[key]
                for key in self.get_unique_symbol_list()]

    def get_unique_symbol_list(self):
        return sorted(self.unique_symbol_to_var_name_dict.keys())

    def get_unique_symbol(self, var_name):
        if not self.unique_symbols_left:
            log.error("Exhausted all variable symbols in Boolean equation. "
                      "This means you tried to evaluate an equation of more "
                      "than 26 variables, which is not supported. "
                      "Cannot continue program execution.")
            # TODO: need to change below exception type
            raise RuntimeError
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
        eval_result_wrapper = EvaluationResultWrapper(
            self.get_input_symbol_list(), self.output_symbol)

        input_symbols = self.get_unique_symbol_list()
        for input_row in get_symbol_input_array(input_symbols):
            expr_to_eval = replace_inputs(
                self.postfix_expr, input_symbols, input_row)
            result = eval_postfix_expr(expr_to_eval)
            eval_result_wrapper.result_list.append(str(result))

        return eval_result_wrapper

    def condense_expression(self, raw_infix_expr):
        condensed_expr = raw_infix_expr
        curr_idx = 0
        left_paren_positions = []
        right_paren_positions = []

        while curr_idx < len(condensed_expr):
            c = condensed_expr[curr_idx].strip()
            if not c:
                pass
            elif c == "(":
                left_paren_positions.append(curr_idx)
            elif c == ")":
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
                                        else ""
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
                                [" ", "("]):
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
                        unique_symbol = self.get_unique_symbol(var_name)
                        condensed_expr = (
                            condensed_expr[:curr_idx] + unique_symbol +
                            condensed_expr[test_idx:])
                        self.pos_to_condensed_magnitude_map[curr_idx] = (
                            len(var_name) - len(unique_symbol))
                    elif c in ["0", "1"]:
                        pass
                    else:
                        raise BadSymbolError(
                            self.infix_expr,
                            self.get_expanded_position(curr_idx),
                            "Invalid symbol.")
            curr_idx += 1

        # Syntax checking is done in a post-processing of the condensed
        # expression

        class NextValidState(Enum):
            OPERAND = 0
            OPERATION = 1

        left_paren_pos_stack = []
        next_state = NextValidState.OPERAND
        for pos, c in enumerate(condensed_expr):
            if not c.strip():
                continue
            elif c == "(":
                if next_state != NextValidState.OPERAND:
                    raise BadParenPositionError(
                        self.infix_expr, self.get_expanded_position(pos),
                        "Unexpected parenthesis.")
                else:
                    left_paren_pos_stack.append(pos)
            elif c == ")":
                if next_state != NextValidState.OPERATION:
                    raise BadParenPositionError(
                        self.infix_expr, self.get_expanded_position(pos),
                        "Unexpected parenthesis.")
                else:
                    if not left_paren_pos_stack:
                        raise UnbalancedParenError(
                            self.infix_expr, self.get_expanded_position(pos),
                            "Unbalanced right parenthesis.")
                    else:
                        left_paren_pos_stack.pop()
            elif c in self.get_unique_symbol_list() or c in ["0", "1"]:
                if next_state != NextValidState.OPERAND:
                    raise ExpressionOrderError(
                        self.infix_expr, self.get_expanded_position(pos),
                        "Unexpected operand.")
                else:
                    next_state = NextValidState.OPERATION
            else:
                if pos == len(condensed_expr) - 1:
                    raise ExpressionOrderError(
                        self.infix_expr, self.get_expanded_position(pos),
                        "Unexpected operation.")
                elif c == SYM_NOT:
                    if next_state != NextValidState.OPERAND:
                        raise ExpressionOrderError(
                            self.infix_expr, self.get_expanded_position(pos),
                            "Unexpected operation.")
                else:
                    if next_state != NextValidState.OPERATION:
                        raise ExpressionOrderError(
                            self.infix_expr, self.get_expanded_position(pos),
                            "Unexpected operation.")
                    else:
                        next_state = NextValidState.OPERAND

        if left_paren_pos_stack:
            raise UnbalancedParenError(
                self.infix_expr,
                self.get_expanded_position(left_paren_pos_stack[0]),
                "Unbalanced left parentheses.")

        condensed_expr = condensed_expr.replace(SYM_NOT, "1" + SYM_XOR)

        return without_spaces(condensed_expr)

    def get_expanded_position(self, at_pos):
        offset = sum(
            [mag for pos, mag in self.pos_to_condensed_magnitude_map.items()
             if pos < at_pos])
        return offset + at_pos


# === Equation Manipulation Free Functions ====================================
def infix_to_postfix(infix_expr, symbol_list):
    """
    Convert the passed infix expression into its postfix form, for simpler
    evaluation later on in the program flow.
    Uses the Shunting-yard Algorithm.

    Args:
        infix_expr: A string infix expression, containing any operations in the
                    schema except for Boolean not. It is assumed that
                    infix_expr is the result of a call to condense_expr.
        symbol_list: The list of single-character string symbols existing in
                     infix_expr.

    Returns:
        The equivalent postfix expression to infix_expr, as a string.
    """
    stack = []
    postfix = []
    operators = schema.keys()

    for c in infix_expr:
        if c in symbol_list or c in ["0", "1"]:
            postfix += c
        elif c == "(":
            stack += c
        elif c in operators:
            if not stack:
                stack += c
            else:
                while (stack and stack[-1] != "(" and
                       schema[stack[-1]].precedence > schema[c].precedence):
                    postfix += stack.pop()
                stack += c
        elif c == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()
            stack.pop()

    for c in reversed(stack):
        postfix += c

    return "".join(postfix)


def extract_output_sym_and_expr(eq):
    """
    Split the passed Boolean equation on its equals sign into the output symbol
    and its equivalent boolean expression.
    Look for errors involving the absence of or multiple equals signs.

    Args:
        eq: The boolean expression to split.

    Returns:
        output_sym: The output symbol, assumed to be the left side of the
                    passed equation.
        expr: The Boolean expression.

    Raises:
        RuntimeError: Raise if no equals signs present or more than one equals
                      sign present.
    """
    output_and_expr = eq.split("=")

    if len(output_and_expr) == 1:
        log.error("Boolean equation did not contain equals sign (\"=\"). "
                  "Cannot continue program execution.")
        raise RuntimeError
    elif len(output_and_expr) > 2:
        log.error("More than one equals sign (\"=\") found in your equation. "
                  "Cannot continue program execution.")
        raise RuntimeError

    output_sym, expr = output_and_expr[0].strip(), output_and_expr[1].strip()
    return output_sym, expr


def replace_inputs(postfix_expr, inputs, input_vals):
    """
    Replace the inputs in a postfix expression string to later be evaluated.

    Args:
        postfix_expr: The postfix expression to be evaluated, as a string.
        inputs: A list of the symbols as strings in postfix_expr to replaced.
        input_vals: A list of the values as strings with which to replace the
                    symbols in inputs in postfix_expr.

    Returns:
        A string postfix expression with the symbols in inputs replaced with
        the values in input_vals.
        For example:
        >>> replace_inputs("AB&", ["A", "B"], ["0", "1"])
        >>> '01&'
    """
    replaced_expr = postfix_expr
    for i, sym in enumerate(inputs):
        replaced_expr = replaced_expr.replace(sym, input_vals[i])
    return replaced_expr


def eval_postfix_expr(expr_to_eval):
    """
    Evaluate the passed postfix expression.

    Args:
        expr_to_eval: A string postfix expression, containing only 0s, 1s, and
                      single character operations. Assumed to be well-formed.

    Returns:
        The result of the evaluation, as int 0 or 1.
    """
    stack = []
    for c in expr_to_eval:
        if c in ["0", "1"]:
            stack.append(int(c))
        else:
            stack.append(schema[c].bool_func(stack.pop(), stack.pop()))
    return stack[0]


# === Utility Free Functions ==================================================
def get_symbol_input_array(sym_list):
    return itertools.product(["0", "1"], repeat=len(sym_list))


# === Grammar-related rules ===================================================
def is_valid_operand_char_non_leading(c):
    return c == "_" or c.isalnum()


# === Custom exception types ==================================================
class GrammarError(Exception):
    def __init__(self, expr_or_equation, error_pos, message, *args):
        self.expr_or_equation = expr_or_equation
        self.error_pos = error_pos
        self.message = message
        super(GrammarError, self).__init__(self.message, *args)

    def log(self):
        log.error(self.message)
        log.error(self.expr_or_equation)
        log.error(" " * self.error_pos + "^")


class BadSymbolError(GrammarError):
    pass


class ExpressionOrderError(GrammarError):
    pass


class BadParenPositionError(GrammarError):
    pass


class UnbalancedParenError(GrammarError):
    pass
