from enum import Enum

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

class Precedence(Enum):
    ZERO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

def bool_not(a, b):
    return not a

def bool_and(a, b):
    return int(a and b)

def bool_nand(a, b):
    return int(a == b)

def bool_xor(a, b):
    return int(a != b)

def bool_xnor(a, b):
    return int(a == b)

def bool_or(a, b):
    return int(a or b)

def bool_nor(a, b):
    return int(not (a or b))

# TODO: possibly allow users to make their own precedence maps in the future
schema = {
    "~" : BooleanOperator(Precedence.HIGH, bool_not, "not", "NOT", "~", "!"),
    "+" : BooleanOperator(Precedence.MEDIUM, bool_xor, "xor", "XOR"),
    "@" : BooleanOperator(Precedence.MEDIUM, bool_xnor, "xnor", "XNOR", "nxor", "NXOR"),
    "&" : BooleanOperator(Precedence.LOW, bool_and, "and", "AND", "&", "&&", "/\\"),
    "$" : BooleanOperator(Precedence.LOW, bool_nand, "nand", "NAND"),
    "|" : BooleanOperator(Precedence.ZERO, bool_or, "or", "OR", "|", "||", "\\/"),
    "%" : BooleanOperator(Precedence.ZERO, bool_nor, "nor", "NOR")
}

schema_search_ordered_list = ["@", "+", "%", "$", "&", "|", "~"]