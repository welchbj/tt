'''
A module for extracting and manipulating information from Boolean equations.
'''
import logging as log

from tt.utils import without_spaces
from tt.schema_provider import schema

def transform_eq_to_generic_schema(raw_eq):
    '''Receives a user-specified Boolean equation and attempts to transform it
    to the generic Python boolean schema, using keywords and, or, not.
    '''

    transformed_eq = raw_eq
    for tt_schema_sym, bool_operator in schema.items(): # TODO: need to update to use new schema
        for sym in bool_operator.equivalent_symbols:
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
    
    if len(output_and_expr) > 2:
        log.error("More than one equals sign (\"=\") found in your Boolean equation. Cannot continue program execution.")
        raise RuntimeError 
    
    output_sym = output_and_expr[0]
    if not is_valid_variable_symbol(output_sym):
        log.warning("Output symbol did not meet the recommended guidelines for equation symbols.\n"
                    "This is probably fine for the output variable, but may cause problems if you followed the same "
                    "patterns for dependent variable symbols.")
    
    expr = output_and_expr[1]
    
    return (output_sym, expr)

def infix_to_postfix(infix):
    # TODO: currently can only handle well-formed expressions
    stack = []
    postfix = []
    operators = schema.keys()

    for c in infix:
        if is_valid_variable_symbol(c):
            postfix += c
        elif c == "(":
            stack += c
        elif c in operators:
            if not stack:
                stack += c
            else:
                while stack[-1] != "(" and schema[stack[-1]] > schema[c]:
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

def transform_postfix_to_primitive_functions(postfix):
    pass

def is_valid_variable_symbol(sym):
    # TODO: support for lowercase and checking of numeric symbols
    return len(sym) == 1 and sym.isalnum() and sym.isupper()

def extract_eq_symbols(eq):
    '''Returns a list of the symbols in the passed Boolean equation.
    All symbols are assumed to be uppercase and one character. 
    All other characters are discarded in the processing of the equation.
    The first symbols in the list is the result of the equation.
    '''
    # TODO: more advanced logic in determining valid symbols
    return [sym for sym in eq if is_valid_variable_symbol(sym)]

def extract_eq_intermediates(eq):
    pass

def generate_eq_inputs(symbol_list):
    for sym in symbol_list:
        pass