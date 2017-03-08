"""Definitions for tt's built-in Boolean operators."""


class BooleanOperator(object):

    """A wrapper around a Boolean operator."""

    def __init__(self, precedence, eval_func, name):
        self._precedence = precedence
        self._eval_func = eval_func
        self._name = name

    def __repr__(self):
        return '<BooleanOperator {}>'.format(self.name)

    @property
    def precedence(self):
        """Precedence of this operator, relative to other operators.

        :type: :class:`int <python:int>`

        .. code-block:: python

            >>> from tt.definitions import TT_AND_OP, TT_OR_OP
            >>> TT_AND_OP.precedence > TT_OR_OP.precedence
            True

        """
        return self._precedence

    @property
    def eval_func(self):
        """The evaluation function wrapped by this operator.

        :type: :data:`Callable <python:typing.Callable>`

        .. code-block:: python

            >>> from tt.definitions import TT_XOR_OP
            >>> TT_XOR_OP.eval_func(0, 0)
            False
            >>> TT_XOR_OP.eval_func(True, False)
            True

        """
        return self._eval_func

    @property
    def name(self):
        """The human-readable name of this operator.

        :type: :class:`str <python:str>`

        .. code-block:: python

            >>> from tt.definitions import TT_NOT_OP, TT_XOR_OP
            >>> TT_NOT_OP.name
            'NOT'
            >>> TT_XOR_OP.name
            'XOR'

        """
        return self._name


_PRECEDENCE = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


TT_NOT_OP = BooleanOperator(_PRECEDENCE['HIGH'],
                            lambda a: not a,
                            'NOT')
"""tt's operator implementation of a Boolean NOT.

:type: :class:`BooleanOperator`

"""

TT_XOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                            lambda a, b: a != b,
                            'XOR')
"""tt's operator implementation of a Boolean XOR.

:type: :class:`BooleanOperator`

"""

TT_XNOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                             lambda a, b: a == b,
                             'XNOR')
"""tt's operator implementation of a Boolean XNOR.

:type: :class:`BooleanOperator`

"""

TT_AND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                            lambda a, b: a and b,
                            'AND')
"""tt's operator implementation of a Boolean AND.

:type: :class:`BooleanOperator`

"""

TT_NAND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                             lambda a, b: not(a and b),
                             'NAND')
"""tt's operator implementation of a Boolean NAND.

:type: :class:`BooleanOperator`

"""

TT_OR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                           lambda a, b: a or b,
                           'OR')
"""tt's operator implementation of a Boolean OR.

:type: :class:`BooleanOperator`

"""

TT_NOR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                            lambda a, b: not(a or b),
                            'NOR')
"""tt's operator implementation of a Boolean NOR.

:type: :class:`BooleanOperator`

"""


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
"""A mapping of Boolean operators.

This mapping serves to define all valid operator strings and maps them to the
appropriate :class:`BooleanOperator` object defining the operator behavior.

:type: Dict{:class:`str <python:str>`: :class:`BooleanOperator`}

"""


MAX_OPERATOR_STR_LEN = max(len(k) for k in OPERATOR_MAPPING.keys())
"""The length of the longest operator from :data:`OPERATOR_MAPPING`.

:type: :class:`int <python:int>`

"""
