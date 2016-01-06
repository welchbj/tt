"""Information about the symbols used in intermediate transformations of
Boolean equations in the scheme used by tt.
"""

import logging as log

__all__ = ['BooleanOperator',
           'schema',
           'schema_search_ordered_list',
           'precedence',
           'SYM_NOT',
           'SYM_NAND',
           'SYM_AND',
           'SYM_OR',
           'SYM_NOR',
           'SYM_XNOR',
           'SYM_XOR']


# === Wrapper Classes =========================================================
class BooleanOperator(object):

    def __init__(self, precedence_in, bool_func_in, *args):
        self.precedence = precedence_in
        self.bool_func = bool_func_in
        self.equivalent_symbols = list(args)

    def result(self, a, b):
        return self.bool_func(a, b)


# === Boolean Functions =======================================================
def tt_and(a, b):
    return int(a and b)


def tt_nand(a, b):
    return int(not(a and b))


def tt_or(a, b):
    return int(a or b)


def tt_nor(a, b):
    return int(not(a or b))


def tt_xor(a, b):
    return int(a != b)


def tt_xnor(a, b):
    return int(a == b)


def tt_uncallable(a, b):
    log.critical('Boolean not function was explicitly called. '
                 'This should not happen; not is implemented as xor with 1. '
                 'Cannot continue program execution.')
    raise RuntimeError


# === Schema Information ======================================================
precedence = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}

SYM_NOT = '~'
SYM_XOR = '+'
SYM_XNOR = '@'
SYM_AND = '&'
SYM_NAND = '$'
SYM_OR = '|'
SYM_NOR = '%'

schema = {
    SYM_NOT: BooleanOperator(precedence['HIGH'],
                             tt_uncallable,
                             'not', 'NOT', '~', '!'),
    SYM_XOR: BooleanOperator(precedence['MEDIUM'],
                             tt_xor,
                             'xor', 'XOR'),
    SYM_XNOR: BooleanOperator(precedence['MEDIUM'],
                              tt_xnor,
                              'xnor', 'XNOR', 'nxor', 'NXOR'),
    SYM_AND: BooleanOperator(precedence['LOW'],
                             tt_and,
                             'and', 'AND', '&&', '&', '/\\'),
    SYM_NAND: BooleanOperator(precedence['LOW'],
                              tt_nand,
                              'nand', 'NAND'),
    SYM_OR: BooleanOperator(precedence['ZERO'],
                            tt_or,
                            'or', 'OR', '||', '|', '\\/'),
    SYM_NOR: BooleanOperator(precedence['ZERO'],
                             tt_nor,
                             'nor', 'NOR')
}

schema_search_ordered_list = [SYM_XNOR,
                              SYM_XOR,
                              SYM_NOR,
                              SYM_NAND,
                              SYM_AND,
                              SYM_OR,
                              SYM_NOT]
