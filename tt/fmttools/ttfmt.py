"""
A module for generating well-formatted truth tables.
"""

__all__ = ['get_truth_table',
           'get_vars',
           'get_title_row']

def get_truth_table(equation):
    transformed_eq = transform_to_generic_schema(equation)
    vars = get_vars(transformed_eq)
    
    

def transform_to_generic_schema(equation):
    # TODO
    # In the future, this function will be able to transform
    # Boolean equations with symbolic operators to the traditional Python 
    # Boolean schema (i.e. and, or)
    return equation

def get_vars(equation):
    """Returns a list of the variables in the passed Boolean equation.
    All variables are assumed to be uppercase and one character. 
    All other symbols/characters are discarded in the processing of the equation.
    The first variable in the list is the output variable.
    """
    return [x for x in equation if x.isalnum() and x.isupper()]


def get_title_row(col_titles, delim="|"):
    """Constructs a string of the table's title row.
    """
    return delim + [col_title + delim for col_title in col_titles]