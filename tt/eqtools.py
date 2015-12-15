'''
A module for extracting and manipulating information from Boolean equations.
'''
import logging as log
import itertools

from utils import without_spaces
from schema_provider import schema, schema_search_ordered_list, SYM_NOT, SYM_XOR

class EvaluationResultWrapper(object):
    def __init__(self, input_syms_in, output_sym_in):
        self.input_syms = input_syms_in
        self.output_sym = output_sym_in
        self.result_list = []

    def get_num_evaluations(self):
        return 2**len(self.input_syms)

def get_evaluation_result(raw_eq):
    generic_schema_eq = transform_eq_to_generic_schema(raw_eq)
    output_sym, expr = extract_output_sym_and_expr(generic_schema_eq)
    input_syms = sorted(extract_eq_symbols(expr))
    postfix_expr = infix_to_postfix(expr)

    eval_result_wrapper = EvaluationResultWrapper(input_syms, output_sym)

    for input_row in get_sym_input_array(input_syms):
        expr_to_eval = replace_inputs(postfix_expr, input_syms, input_row)
        result = eval_postfix_expr(expr_to_eval)
        eval_result_wrapper.result_list.append(str(result))

    return eval_result_wrapper

def transform_eq_to_generic_schema(raw_eq):
    transformed_eq = raw_eq
    for tt_schema_sym in schema_search_ordered_list: # TODO: need to update to use new schema
        for sym in schema[tt_schema_sym].equivalent_symbols:
            if sym in transformed_eq:
                replacement_sym = ("1"+SYM_XOR) if (tt_schema_sym == SYM_NOT) else tt_schema_sym
                transformed_eq = transformed_eq.replace(sym, replacement_sym)
    return without_spaces(transformed_eq)

def extract_output_sym_and_expr(eq):
    '''Assumes that the equation has already been transformed to tt's generic
    schema for Boolean equations'''

    output_and_expr = eq.split("=")

    if len(output_and_expr) == 1:
        log.error("Boolean equation did not contain equals sign (\"=\"). Cannot continue program execution.")
        raise RuntimeError
    elif len(output_and_expr) > 2:
        log.error("More than one equals sign (\"=\") found in your Boolean equation. Cannot continue program execution.")
        raise RuntimeError 
    
    output_sym, expr = output_and_expr[0], output_and_expr[1]
    if not is_valid_variable_symbol(output_sym):
        log.warning("Output symbol did not meet the recommended guidelines for equation symbols.\n"
                    "This is probably fine for the output variable, but may cause problems if you followed the same "
                    "patterns for dependent variable symbols.")
    return output_sym, expr

def infix_to_postfix(infix):
    # TODO: currently can only handle well-formed expressions
    stack = []
    postfix = []
    operators = schema.keys()

    for c in infix:
        if is_valid_eq_input(c):
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

def is_valid_variable_symbol(sym):
    return len(sym) == 1 and sym.isalpha() and sym.isupper()

def is_valid_eq_input(sym):
    return is_valid_variable_symbol(sym) or str(sym) in ["0", "1"]

def extract_eq_symbols(eq):
    '''Returns a list of the symbols in the passed Boolean equation.
    All symbols are assumed to be uppercase and one character. 
    All other characters are discarded in the processing of the equation.
    The first symbols in the list is the result of the equation.
    '''
    # TODO: more advanced logic in determining valid symbols
    stored_syms = []
    for sym in eq:
        if is_valid_variable_symbol(sym) and sym not in stored_syms:
            stored_syms.append(sym)
    return stored_syms

def replace_inputs(postfix_expr, inputs, input_vals):
    replaced_expr = postfix_expr
    for i, sym in enumerate(inputs):
        replaced_expr = replaced_expr.replace(sym, input_vals[i])
    return replaced_expr

def eval_postfix_expr(expr_to_eval):
    # TODO: account for boolean not

    stack = []
    for c in expr_to_eval:
        if c in ["0", "1"]:
            stack.append(int(c))
        else:
            stack.append(schema[c].bool_func(stack.pop(), stack.pop()))
    return stack[0]

def get_sym_input_array(sym_list):
    return itertools.product(["0", "1"], repeat=len(sym_list))

def extract_eq_intermediates(eq):
    pass