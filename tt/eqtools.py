"""
A module for extracting and manipulating information from Boolean equations.
"""

import logging as log
import itertools

from utils import without_spaces
from schema_provider import schema, schema_search_ordered_list, SYM_NOT, SYM_XOR


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

        self.output_symbol, self.infix_expr = extract_output_sym_and_expr(raw_bool_eq)

        self.condensed_infix_expr = self.condense_expression(self.infix_expr)
        self.postfix_expr = self.infix_to_postfix(self.condensed_infix_expr)

    def get_input_symbol_list(self):
        """
        Get the list of input symbols contained within this equation.

        Returns:
            The list of input symbols of the equation, sorted by their order in the equation.
        """
        return [self.unique_symbol_to_var_name_dict[key] for key in self.get_unique_symbol_list()]

    def get_unique_symbol_list(self):
        return sorted(self.unique_symbol_to_var_name_dict.keys())

    def get_unique_symbol(self, var_name):
        if not self.unique_symbols_left:
            log.error("Exhausted all variable symbols in Boolean equation. "
                      "This means you tried to evaluate an equation of more than 26 variables, which is not supported. "
                      "Cannot continue program execution.")
            raise RuntimeError # TODO: better exception type?
        elif var_name in self.unique_symbol_to_var_name_dict.values():
            # all values should be unique, so we should be safe to assume this list comprehension will yield one element
            return [key for key, val in self.unique_symbol_to_var_name_dict.items() if val == var_name][0]
        else:
            unique_symbol = self.unique_symbols_left.pop()
            self.unique_symbol_to_var_name_dict[unique_symbol] = var_name
            return unique_symbol

    def get_evaluation_result(self):
        eval_result_wrapper = EvaluationResultWrapper(self.get_input_symbol_list(), self.output_symbol)

        input_symbols = self.unique_symbol_list()
        for input_row in get_symbol_input_array(self.input_symbols()):
            expr_to_eval = replace_inputs(self.postfix_expr, input_symbols, input_row)
            result = eval_postfix_expr(expr_to_eval)
            eval_result_wrapper.result_list.append(str(result))

        return eval_result_wrapper

    def condense_expression(self, raw_infix_expr):
        # TODO: doc
        """

        Args:
            raw_infix_expr:

        Returns:

        """

        # TODO: need to check for consecutive symbols
        condensed_expr = raw_infix_expr
        curr_idx = 0
        prev_char_is_operand = False
        left_paren_positions = []
        right_paren_positions = []
        operand_positions = []
        operation_positions = []

        while curr_idx < len(condensed_expr):
            c = condensed_expr[curr_idx].strip()
            if not c:
                pass
            elif c == "(":
                left_paren_positions.append(curr_idx)
            elif c == ")":
                right_paren_positions.append(curr_idx)
            else:
                # TODO: need to do Boolean not transformation
                is_operation = False
                for tt_operation_symbol in schema_search_ordered_list:
                    equivalent_symbols = schema[tt_operation_symbol].equivalent_symbols # assume this list is pre-ordered by length in the schema
                    operation_symbol_lens = [len(equivalent_symbol) for equivalent_symbol in equivalent_symbols]
                    test_idxs = [curr_idx+operation_symbol_len for operation_symbol_len in operation_symbol_lens]
                    possible_matches = [condensed_expr[curr_idx:test_idx] for test_idx in test_idxs if test_idx <= len(condensed_expr)]
                    matches = [possible_match for operation_symbol, possible_match in zip(equivalent_symbols, possible_matches) if operation_symbol == possible_match]

                    if matches:
                        match = matches[0]
                        matched_idx = possible_matches.index(match)
                        replacement_idx = test_idxs[matched_idx]

                        if replacement_idx < len(condensed_expr):
                            if match[-1].isalpha() and condensed_expr[replacement_idx] not in [" ", "("]:
                                # this is just an operand that begins with one of the tt schema symbols;
                                # we can break out of this because no operation symbols for different operations
                                # start with another symbol
                                break

                        expr_kept_leading = condensed_expr[:curr_idx]
                        expr_kept_trailing = condensed_expr[replacement_idx:]
                        if tt_operation_symbol == SYM_NOT:
                            replacement_symbol = "1" + SYM_XOR
                            curr_idx += 1
                        else:
                            replacement_symbol = tt_operation_symbol

                        condensed_expr = expr_kept_leading + replacement_symbol + expr_kept_trailing
                        is_operation = True
                        break

                if not is_operation:
                    if c.isalpha(): # operand names must start with letter
                        # parse the variable name
                        test_idx = curr_idx + 1
                        while test_idx < len(condensed_expr) and is_valid_operand_char_non_leading(condensed_expr[test_idx]):
                            test_idx += 1

                        var_name = condensed_expr[curr_idx:test_idx]
                        unique_symbol = self.get_unique_symbol(var_name)
                        condensed_expr = condensed_expr[:curr_idx] + unique_symbol + condensed_expr[test_idx:]
                    elif c in ["0", "1"]:
                        pass
                    else:
                        log.error("TEMP ERROR MSG: Invalid symbol")
            curr_idx += 1

        # Extensive syntax checking is done in a post-processing of the condensed expression
        left_paren_pos_stack = []
        operand_pos_list = []
        operation_pos_list = []
        for pos, c in enumerate(condensed_expr):
            if not c.strip():
                continue
            elif c == "(":
                left_paren_pos_stack.append(pos)
            elif c == ")":
                if not left_paren_pos_stack:
                    # TODO: log message
                    raise UnbalancedParenException
                else:
                    left_paren_pos_stack.pop()
            elif c in self.get_unique_symbol_list() or c in ["0", "1"]:
                operand_pos_list.append(pos)
            else:
                # assume we replaced correctly above and c must be an operation symbol
                operation_pos_list.append(pos)

        if left_paren_pos_stack:
            # TODO: log message
            raise UnbalancedParenException

        if len(operand_pos_list) - len(operation_pos_list) != 1:
            # TODO: log message
            raise GrammarException

        for operand_pos, operation_pos in itertools.zip_longest(operand_pos_list, operation_pos_list, fillvalue=float("inf")):
            if operand_pos > operation_pos:
                # TODO: log message
                raise GrammarException

        return without_spaces(condensed_expr)

    def infix_to_postfix(self, infix_expr):
        """
        Convert the passed infix expression into its equivalent postfix form. The Shunting-Yard Algorithm is used to
        perform this conversion.

        Args:
            infix_expr: The Boolean expression to convert in infix form, as a string.

        Returns:
            A BooleanEquationWrapper instance filled with the infix and postfix representations of the expression
        """
        stack = []
        postfix = []
        operators = schema.keys()

        for c in infix_expr:
            if c in self.get_unique_symbol_list():
                postfix += c
            elif c == "(":
                stack += c
            elif c in operators:
                if not stack:
                    stack += c
                else:
                    while stack and stack[-1] != "(" and schema[stack[-1]].precedence > schema[c].precedence:
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
    Split the passed boolean equation on its equals sign into the output symbol and its equivalent boolean expression.
    Look for errors involving the absence of or multiple equals signs.
    Warn about an improperly formatted output symbol.

    Args:
        eq: The boolean expression to split.

    Returns:
        output_sym: The output symbol, assumed to be the left side of the passed equation.
        expr: The Boolean expression.

    Raises:
        RuntimeError: Raise if no equals signs present or more than one equals sign present.
    """
    output_and_expr = eq.split("=")

    if len(output_and_expr) == 1:
        log.error("Boolean equation did not contain equals sign (\"=\"). Cannot continue program execution.")
        raise RuntimeError
    elif len(output_and_expr) > 2:
        log.error("More than one equals sign (\"=\") found in your equation. Cannot continue program execution.")
        raise RuntimeError

    output_sym, expr = output_and_expr[0], output_and_expr[1]
    return output_sym, expr


def replace_inputs(postfix_expr, inputs, input_vals):
    """
    Replace the inputs in a postfix expression string to be evaluated.

    Args:
        postfix_expr: The postfix expression to be evaluated, as a string.
        inputs: A list of the symbols as strings in postfix_expr to replaced.
        input_vals: A list of the values as strings with which to replace the symbols in inputs in postfix_expr.

    Returns:
        A string postfix expression with the symbols in inputs replaced with the values in input_vals.
        For example:

        >>> replace_inputs("AB&", ["A", "B"], ["0", "1"])
        >>> '01&'
    """
    replaced_expr = postfix_expr
    for i, sym in enumerate(inputs):
        replaced_expr = replaced_expr.replace(sym, input_vals[i])
    return replaced_expr


def eval_postfix_expr(expr_to_eval):
    stack = []
    for c in expr_to_eval:
        if c in ["0", "1"]:
            stack.append(int(c))
        else:
            stack.append(schema[c].bool_func(stack.pop(), stack.pop()))
    return stack[0]


def get_symbol_input_array(sym_list):
    return itertools.product(["0", "1"], repeat=len(sym_list))


# === Grammar-related rules ============================================================================================
def is_valid_operand_char_non_leading(c):
    return c == "_" or c.isalnum()


# === Custom exception types ===========================================================================================
class UnbalancedParenException(Exception):
    pass


class EmptyScopeException(Exception):
    pass


class GrammarException(Exception):
    pass
