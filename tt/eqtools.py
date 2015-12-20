"""
A module for extracting and manipulating information from Boolean equations.
"""

import logging as log
import itertools

from utils import without_spaces
from schema_provider import schema, schema_search_ordered_list


class EvaluationResultWrapper(object):
    def __init__(self, input_symbols, output_symbol):
        self.input_symbols = input_symbols
        self.output_symbols = output_symbol
        self.result_list = []

    def get_num_evaluations(self):
        return 2**len(self.input_symbols)


class BooleanExpressionWrapper(object):
    def __init__(self, raw_infix_expr):
        self.unique_symbols_left = list(reversed("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.unique_symbol_to_var_name_dict = {}

        self.infix_expr = raw_infix_expr
        self.condensed_infix_expr = self.condense_expression(raw_infix_expr)
        self.postfix_expr = self.infix_to_postfix(self.condensed_infix_expr)

    def get_variable_list(self):
        return [val for key, val in self.unique_symbol_to_var_name_dict.items()]

    def get_unique_symbol_list(self):
        return self.unique_symbol_to_var_name_dict.keys()

    def get_unique_symbol(self, var_name):
        if not self.unique_symbols_left:
            log.fatal("Exhausted all variable symbols in Boolean equation. "
                      "This means you tried to evaluate an equation of more than 26 variables. "
                      "Cannot continue program execution.")
            raise RuntimeError
        elif var_name in self.unique_symbol_to_var_name_dict.values():
            # all values should be unique, so we should be safe to assume this list comprehension will yield one element
            return [key for key, val in self.unique_symbol_to_var_name_dict.items() if val == var_name][0]
        else:
            unique_symbol = self.unique_symbols_left.pop()
            self.unique_symbol_to_var_name_dict[unique_symbol] = var_name
            return unique_symbol

    def condense_expression(self, raw_infix_expr):
        # TODO: doc
        """
        Ensures that the expression is well-formed and transforms variable names to single inputs and converts
        Boolean operations to single character equivalents defined in the tt schema.

        Returns:

        """

        # TODO: need to check for consecutive symbols

        curr_idx = 0
        prev_char_is_operand = False
        left_paren_positions = []
        right_paren_positions = []

        while curr_idx < len(raw_infix_expr):
            c = raw_infix_expr[curr_idx].strip()
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
                    possible_matches = [raw_infix_expr[curr_idx:test_idx] for test_idx in test_idxs if test_idx <= len(raw_infix_expr)]
                    matches = [possible_match for operation_symbol, possible_match in zip(equivalent_symbols, possible_matches) if operation_symbol == possible_match]

                    if matches:
                        match = matches[0]
                        matched_idx = possible_matches.index(match)
                        replacement_idx = test_idxs[matched_idx]

                        if replacement_idx == len(raw_infix_expr):
                            log.error("Boolean equation ended with an operation. Its last scope must end with an operand.")
                            raise GrammarException

                        if match[-1].isalpha() and raw_infix_expr[replacement_idx] not in [" ", "("]:
                            # this is just an operand that begins with one of the tt schema symbols;
                            # we can break out of this because no operation symbols for different operation
                            # start with another symbol
                            break

                        raw_infix_expr = raw_infix_expr[:curr_idx] + tt_operation_symbol + raw_infix_expr[replacement_idx:]
                        is_operation = True
                        break
                if not is_operation:
                    if c.isalpha(): # operand names must start with letter
                        # parse the variable name
                        test_idx = curr_idx + 1
                        while test_idx < len(raw_infix_expr) and is_valid_operand_char_non_leading(raw_infix_expr[test_idx]):
                            test_idx += 1

                        var_name = raw_infix_expr[curr_idx:test_idx]
                        unique_symbol = self.get_unique_symbol(var_name)
                        raw_infix_expr = raw_infix_expr[:curr_idx] + unique_symbol + raw_infix_expr[test_idx:]
                    elif c in ["0", "1"]:
                        pass
                    else:
                        log.error("TEMP ERROR MSG: Invalid symbol")
            curr_idx += 1

        # TODO: Check parentheses
        # Syntax checking is done in a post-processing of the condensed expression

        return without_spaces(raw_infix_expr)

    def infix_to_postfix(self, infix_expr):
        """
        Convert the passed infix expression into its equivalent postfix form. The Shunting-Yard Algorithm is used to
        perform this conversion.

        Args:
            infix_expr: The Boolean expression to convert in infix form, as a string.

        Returns:
            A BooleanExpressionWrapper instance filled with the infix and postfix representations of the expression
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


def get_evaluation_result(raw_eq):
    """
    This is the main flow for truth table computation.  The flow is divided into several steps:
        1. Transform the passed equation into the tt schema, as defined in the schema_provider module.
        2. Split the equation i\nto the result symbol and the infix Boolean expression to be evaluated.
        3. Extract the input symbols from the Boolean expression.
        4. Convert the infix expression to its postfix form.
        5. Evaluate the postfix expression at each possible combination of bool inputs to the expression.

    Args:
        raw_eq: The infix boolean equation to evaluate, unchanged from the user's original entry.

    Returns:
        An instance of EvaluationResultWrapper containing the input symbols, output symbol, and list of results of the
        equation's evaluation for each possible boolean combination of its inputs.
    """
    generic_schema_eq = transform_eq_to_generic_schema(raw_eq)
    output_sym, expr = extract_output_sym_and_expr(generic_schema_eq)
    # input_syms = sorted(extract_symbols(expr))
    expr = "A and B"
    bool_expr_wrapper = infix_to_postfix(expr)
    postfix_expr = bool_expr_wrapper.postfix_repr
    input_syms = sorted(bool_expr_wrapper.get_unique_symbol_list())

    eval_result_wrapper = EvaluationResultWrapper(input_syms, output_sym)
    for input_row in get_sym_input_array(input_syms):
        expr_to_eval = replace_inputs(postfix_expr, input_syms, input_row)
        result = eval_postfix_expr(expr_to_eval)
        eval_result_wrapper.result_list.append(str(result))

    return eval_result_wrapper


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
        log.error("Boolean equation did not contain equals sign (\"=\").\n"
                  "Cannot continue program execution.")
        raise RuntimeError
    elif len(output_and_expr) > 2:
        log.error("More than one equals sign (\"=\") found in your equation.\n"
                  "Cannot continue program execution.")
        raise RuntimeError 
    
    output_sym, expr = output_and_expr[0], output_and_expr[1]
    if not is_valid_variable_symbol(output_sym):
        log.warning("Output symbol did not meet the recommended guidelines for equation symbols. "
                    "This is probably fine for the output variable, but may cause problems if you followed the same "
                    "patterns for dependent variable symbols.")
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


def get_sym_input_array(sym_list):
    return itertools.product(["0", "1"], repeat=len(sym_list))


# === Grammar-related rules ============================================================================================
def is_valid_operand_char_non_leading(c):
    return c == "_" or c.isalnum()

def is_non_item_changing_char(c):
    pass


# === Custom exception types ===========================================================================================
class UnbalancedParenException(Exception):
    pass


class EmptyScopeException(Exception):
    pass


class GrammarException(Exception):
    pass
