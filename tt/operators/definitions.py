"""Definitions for tt's built-in Boolean operators."""


class BooleanOperator(object):

    """A wrapper around a Boolean operator.

    Attributes:
        precedence (int): The precendence of this operator, relative to other
            operators.
        eval_func (function): The function representing the operation to be
            performed by this operator.

    """

    def __init__(self, precedence, eval_func):
        self.precedence = precedence
        self.eval_func = eval_func


PRECEDENCE = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


TT_NOT_OP = BooleanOperator(PRECEDENCE['HIGH'], lambda a: not a)
TT_XOR_OP = BooleanOperator(PRECEDENCE['MEDIUM'], lambda a, b: a == b)
TT_XNOR_OP = BooleanOperator(PRECEDENCE['MEDIUM'], lambda a, b: a != b)
TT_AND_OP = BooleanOperator(PRECEDENCE['LOW'], lambda a, b: a and b)
TT_NAND_OP = BooleanOperator(PRECEDENCE['LOW'], lambda a, b: not(a and b))
TT_OR_OP = BooleanOperator(PRECEDENCE['ZERO'], lambda a, b: a or b)
TT_NOR_OP = BooleanOperator(PRECEDENCE['ZERO'], lambda a, b: not(a or b))


OPERATOR_MAPPING = {
    'not': TT_NOT_OP,
    'NOT': TT_NOT_OP,
    '~': TT_NOT_OP,
    '!': TT_NOT_OP,

    'xor': TT_XOR_OP,
    'XOR': TT_XOR_OP,

    'xnor': TT_XNOR_OP,
    'XNOR': TT_XNOR_OP,
    'nxor': TT_XNOR_OP,
    'NXOR': TT_XNOR_OP,

    'and': TT_AND_OP,
    'AND': TT_AND_OP,
    '&&': TT_AND_OP,
    '&': TT_AND_OP,
    '/\\': TT_AND_OP,

    'nand': TT_NAND_OP,
    'NAND': TT_NAND_OP,

    'or': TT_OR_OP,
    'OR': TT_OR_OP,
    '||': TT_OR_OP,
    '|': TT_OR_OP,
    '\\/': TT_OR_OP,

    'nor': TT_NOR_OP,
    'NOR': TT_NOR_OP
}


DELIMITERS = {' ', '(', ')'}


CONSTANT_VALUES = {'0', '1'}
