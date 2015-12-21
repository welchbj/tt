import logging as log

__all__ = ["BooleanOperator",
           "schema",
           "schema_search_ordered_list",
           "precedence",
           "SYM_NOT",
           "SYM_NAND",
           "SYM_AND",
           "SYM_OR",
           "SYM_NOR",
           "SYM_XNOR",
           "SYM_XOR"]


class BooleanOperator(object):
    def __init__(self, precedence_in, bool_func_in, *args):
        self.precedence = precedence_in
        self.bool_func = bool_func_in
        self.equivalent_symbols = list(args)

    def result(self, a, b):
        return self.bool_func(a, b)

# functions called in Boolean expression evaluation;
# a and b should always be passed as ints to these functions
tt_and = lambda a, b: int(a and b)
tt_nand = lambda a, b: int(not tt_and(a, b))
tt_or = lambda a, b: int(a or b)
tt_nor = lambda a, b: int(not tt_or(a, b))
tt_xor = lambda a, b: int((not a and b) or (a and not b))
tt_xnor = lambda a, b: int(not tt_xor(a, b))


def uncallable(a, b):
    log.critical("Boolean not function was explicitly called. "
              "This should not happen; not is implemented as xor with 1. "
              "Cannot continue program execution.")
    raise RuntimeError

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
    SYM_NOT : BooleanOperator(precedence["HIGH"], uncallable, "not", "NOT", "~", "!"),
    SYM_XOR : BooleanOperator(precedence["MEDIUM"], tt_xor, "xor", "XOR"),
    SYM_XNOR : BooleanOperator(precedence["MEDIUM"], tt_xnor, "xnor", "XNOR", "nxor", "NXOR"),
    SYM_AND : BooleanOperator(precedence["LOW"], tt_and, "and", "AND", "&&", "&", "/\\"),
    SYM_NAND : BooleanOperator(precedence["LOW"], tt_nand, "nand", "NAND"),
    SYM_OR : BooleanOperator(precedence["ZERO"], tt_or, "or", "OR", "||", "|", "\\/"),
    SYM_NOR : BooleanOperator(precedence["ZERO"], tt_nor, "nor", "NOR")
}

schema_search_ordered_list = [SYM_XNOR, SYM_XOR, SYM_NOR, SYM_NAND, SYM_AND, SYM_OR, SYM_NOT]