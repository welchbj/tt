import logging as log

class BooleanOperator(object):
    def __init__(self, precedence_in, bool_func_in, *args):
        self.precedence = precedence_in
        self.bool_func = bool_func_in
        self.equivalent_symbols = list(args)

    def result(self, a, b):
        return self.bool_func(a, b)

    # define rich-comparison operators
    def __gt__(self, other):
        return self.precedence.__gt__(other.precedence)
    
    def __ge__(self, other):
        return self.precedence.__ge__(other.precedence)
    
    def __lt__(self, other):
        return self.precedence.__lt__(other.precedence)
    
    def __le__(self, other):
        return self.precedence.__le__(other.precedence)
    
    def __eq__(self, other):
        return self.precedence.__eq__(other.precedence)
    
    def __ne__(self, other):
        return self.precedence.__ne__(other.precedence)

def bool_not(a, b):
    # this should never be called;
    # not is implemented as xor w/ 1
    log.fatal("Boolean not function was explicitly called.\n"
              "This should not happen; not is implemented as xor with 1.\n"
              "Cannot continue program execution.\n")
    raise RuntimeError

def bool_and(a, b):
    return int(a and b)

def bool_nand(a, b):
    return int(not (a and b))

def bool_xor(a, b):
    return int(a != b)

def bool_xnor(a, b):
    return int(a == b)

def bool_or(a, b):
    return int(a or b)

def bool_nor(a, b):
    return int(not (a or b))

# Define schema information

precedence = {
    "ZERO" : 0,
    "LOW" : 1,
    "MEDIUM" : 2,
    "HIGH" : 3
}

SYM_NOT = "~"
SYM_XOR = "+"
SYM_XNOR = "@"
SYM_AND = "&"
SYM_NAND = "$"
SYM_OR = "|"
SYM_NOR = "%"

# TODO: possibly allow users to make their own precedence maps in the future
schema = {
    SYM_NOT : BooleanOperator(precedence["HIGH"], bool_not, "not", "NOT", "~", "!"),
    SYM_XOR : BooleanOperator(precedence["MEDIUM"], bool_xor, "xor", "XOR"),
    SYM_XNOR : BooleanOperator(precedence["MEDIUM"], bool_xnor, "xnor", "XNOR", "nxor", "NXOR"),
    SYM_AND : BooleanOperator(precedence["LOW"], bool_and, "and", "AND", "&", "&&", "/\\"),
    SYM_NAND : BooleanOperator(precedence["LOW"], bool_nand, "nand", "NAND"),
    SYM_OR : BooleanOperator(precedence["ZERO"], bool_or, "or", "OR", "|", "||", "\\/"),
    SYM_NOR : BooleanOperator(precedence["ZERO"], bool_nor, "nor", "NOR")
}

schema_search_ordered_list = [SYM_XNOR, SYM_XOR, SYM_NOR, SYM_NAND, SYM_AND, SYM_OR, SYM_NOT]