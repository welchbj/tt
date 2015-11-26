"""
A module for extracting an manipulating information from Boolean equations.
"""

from tt.utils import without_spaces

eq_transform_sym_dict = {
                         "~" : ["not", "NOT",  "~", "!"],
                         "&" : ["and", "AND", "&", "&&", "/\\"],
                         "|" : ["or", "OR", "|", "||", "\\/"]
                        }

def transform_eq_to_generic_schema(raw_eq):
    """Receives a user-specified Boolean equation and attempts to transform it
    to the generic Python boolean schema, using keywords and, or, not.
    
    Currently unsupported:
    nand
    nor
    xor
    xnor
    """
        
    transformed_eq = raw_eq
    for tt_schema_sym, other_schema_sym_list in eq_transform_sym_dict.items():
        for sym in other_schema_sym_list:
            if sym in transformed_eq:
                transformed_eq = transformed_eq.replace(sym, tt_schema_sym)
    return without_spaces(transformed_eq)

def extract_expr_from_eq(eq):
    pass

def extract_eq_symbols(eq):
    """Returns a list of the symbols in the passed Boolean equation.
    All symbols are assumed to be uppercase and one character. 
    All other characters are discarded in the processing of the equation.
    The first symbols in the list is the result of the equation.
    """
    # TODO: more advanced logic in determining valid symbols
    return [sym for sym in eq if sym.isalnum() and sym.isupper()]

def extract_eq_intermediates(eq):
    pass

def generate_eq_inputs(symbol_list):
    for sym in symbol_list:
        pass 
    
    
    
    
    