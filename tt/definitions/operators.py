"""Definitions for tt's built-in Boolean operators."""


class BooleanOperator(object):

    """A wrapper around a Boolean operator.

    Attributes:
        precedence (int): The precendence of this operator, relative to other
            operators.
        eval_func (function): The function representing the operation to be
            performed by this operator.

    """

    def __init__(self, precedence, eval_func, name):
        self.precedence = precedence
        self.eval_func = eval_func
        self.name = name

    def __repr__(self):
        return '<BooleanOperator {}>'.format(self.name)


_PRECEDENCE = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


TT_NOT_OP = BooleanOperator(_PRECEDENCE['HIGH'],
                            lambda a: not a,
                            'NOT')
"""BooleanOperator: tt's implementation of a Boolean NOT."""

TT_XOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                            lambda a, b: a != b,
                            'XOR')
"""BooleanOperator: tt's implementation of a Boolean XOR."""

TT_XNOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                             lambda a, b: a == b,
                             'XNOR')
"""BooleanOperator: tt's implementation of a Boolean XNOR."""

TT_AND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                            lambda a, b: a and b,
                            'AND')
"""BooleanOperator: tt's implementation of a Boolean AND."""

TT_NAND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                             lambda a, b: not(a and b),
                             'NAND')
"""BooleanOperator: tt's implementation of a Boolean NAND."""

TT_OR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                           lambda a, b: a or b,
                           'OR')
"""BooleanOperator: tt's implementation of a Boolean OR."""

TT_NOR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                            lambda a, b: not(a or b),
                            'NOR')
"""BooleanOperator: tt's implementation of a Boolean NOR."""


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
"""Dict: A mapping of Boolean operators.

This mapping serves to define all valid operator strings and maps them to the
appropriate ``BooleanOperator`` object defining the operator behavior.

"""


MAX_OPERATOR_STR_LEN = max(len(k) for k in OPERATOR_MAPPING.keys())
"""int: The length of the longest operator from ``OPERATOR_MAPPING``."""
