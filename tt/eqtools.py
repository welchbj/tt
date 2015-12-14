'''
A module for extracting and manipulating information from Boolean equations.
'''
import logging as log
import itertools

from utils import without_spaces
from schema_provider import schema, schema_search_ordered_list

def print_truth_table(raw_eq):
    generic_schema_eq = transform_eq_to_generic_schema(raw_eq)
    output_sym, expr = extract_output_sym_and_expr(generic_schema_eq)
    postfix_expr = infix_to_postfix(expr)

    input_syms = sorted(extract_eq_symbols(expr))
    num_inputs = len(input_syms)

    input_val_list = list(itertools.product(["0", "1"], repeat=num_inputs))
    result_list = []

    for input_row in input_val_list:
        expr_to_eval = replace_inputs(postfix_expr, input_syms, input_row)
        result = eval_postfix_expr(expr_to_eval)
        result_list.append(str(result))

    title_row = table_rowify(itertools.chain(input_syms, output_sym))
    fancy_row_separator = "+" + "+".join(itertools.repeat("---", len(input_syms) + 1)) + "+"
    row_separator = "\n" + "-" * len(title_row) + "\n"

    table_content = ""
    for i, input_val_row in enumerate(input_val_list):
        table_content += table_rowify(itertools.chain(input_val_row, result_list[i]))
        table_content += "\n"

    the_table = ""
    the_table += fancy_row_separator + "\n"
    the_table += title_row + "\n"
    the_table += fancy_row_separator + "\n"
    the_table += table_content
    the_table += fancy_row_separator  + "\n"

    print(the_table)

def transform_eq_to_generic_schema(raw_eq):
    '''Receives a user-specified Boolean equation and attempts to transform it
    to the generic Python boolean schema, using keywords and, or, not.
    '''

    transformed_eq = raw_eq
    for tt_schema_sym in schema_search_ordered_list: # TODO: need to update to use new schema
        for sym in schema[tt_schema_sym].equivalent_symbols:
            if sym in transformed_eq:
                transformed_eq = transformed_eq.replace(sym, tt_schema_sym)
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
                while stack and stack[-1] != "(" and schema[stack[-1]] > schema[c]:
                    postfix += stack.pop()
                stack += c
        elif c == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()
            stack.pop()

    # TODO: check for remaining parens
    for c in reversed(stack):
        postfix += c

    return "".join(postfix)

def is_valid_variable_symbol(sym):
    # TODO: support for lowercase and checking of numeric symbols
    return len(sym) == 1 and sym.isalpha() and sym.isupper()

def is_valid_eq_input(sym):
    return len(sym) == 1 and sym.isalnum() and sym.isupper()

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

def construct_sym_to_input_map(input_syms):
    sym_to_input_map = {}

    for sym in input_syms:
        sym_to_input_map[sym] = []

    input_array = list(itertools.product([0, 1], repeat=len(input_syms)))
    for bool_tuple in input_array:
        for i, sym in enumerate(input_syms):
            sym_to_input_map[sym].append(bool_tuple[i])

    return sym_to_input_map

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

def table_rowify(syms):
    return "| " + " | ".join(syms) + " |"

def extract_eq_intermediates(eq):
    pass