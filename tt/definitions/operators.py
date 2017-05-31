"""Definitions for tt's built-in Boolean operators."""


class BooleanOperator(object):

    """A thin wrapper around a Boolean operator."""

    def __init__(self, precedence, eval_func, default_symbol_str,
                 default_plain_english_str):
        self._precedence = precedence
        self._eval_func = eval_func
        self._default_symbol_str = default_symbol_str
        self._default_plain_english_str = default_plain_english_str

    def __str__(self):
        return self._default_plain_english_str

    def __repr__(self):
        return '<BooleanOperator "{}">'.format(self._default_plain_english_str)

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
    def default_symbol_str(self):
        """The default symbolic string representation of this operator.

        Some operators may not have a recognized symbol str, in which case
        this attribute will be ``None``.

        :type: :class:`str <python:str>` or ``None``

        .. code-block:: python

            >>> from tt.definitions import TT_AND_OP, TT_NAND_OP
            >>> print(TT_AND_OP.default_symbol_str)
            /\\
            >>> print(TT_NAND_OP.default_symbol_str)
            None

        """
        return self._default_symbol_str

    @property
    def default_plain_english_str(self):
        """The default plain English string representation of this operator.

        Unlike :data:`default_symbol_str`, this attribute should never be
        ``None``.

        :type: :class:`str <python:str>`

        .. code-block:: python

            >>> from tt.definitions import TT_AND_OP, TT_NAND_OP
            >>> print(TT_AND_OP.default_plain_english_str)
            and
            >>> print(TT_NAND_OP.default_plain_english_str)
            nand

        """
        return self._default_plain_english_str


_PRECEDENCE = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


TT_NOT_OP = BooleanOperator(_PRECEDENCE['HIGH'],
                            lambda a: not a,
                            '~', 'not')
"""tt's operator implementation of a Boolean NOT.

:type: :class:`BooleanOperator`

"""

TT_IMPL_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                             lambda a, b: (not a) or b,
                             '->', 'impl')
"""tt's operator implementation of a Boolean IMPLIES.

:type: :class:`BooleanOperator`

"""

TT_XOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                            lambda a, b: a != b,
                            None, 'xor')
"""tt's operator implementation of a Boolean XOR.

:type: :class:`BooleanOperator`

"""

TT_XNOR_OP = BooleanOperator(_PRECEDENCE['MEDIUM'],
                             lambda a, b: a == b,
                             None, 'xnor')
"""tt's operator implementation of a Boolean XNOR.

:type: :class:`BooleanOperator`

"""

TT_AND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                            lambda a, b: a and b,
                            '/\\', 'and')
"""tt's operator implementation of a Boolean AND.

:type: :class:`BooleanOperator`

"""

TT_NAND_OP = BooleanOperator(_PRECEDENCE['LOW'],
                             lambda a, b: not(a and b),
                             None, 'nand')
"""tt's operator implementation of a Boolean NAND.

:type: :class:`BooleanOperator`

"""

TT_OR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                           lambda a, b: a or b,
                           '\\/', 'or')
"""tt's operator implementation of a Boolean OR.

:type: :class:`BooleanOperator`

"""

TT_NOR_OP = BooleanOperator(_PRECEDENCE['ZERO'],
                            lambda a, b: not(a or b),
                            None, 'nor')
"""tt's operator implementation of a Boolean NOR.

:type: :class:`BooleanOperator`

"""

BINARY_OPERATORS = {
    TT_AND_OP,
    TT_IMPL_OP,
    TT_NAND_OP,
    TT_NOR_OP,
    TT_OR_OP,
    TT_XNOR_OP,
    TT_XOR_OP
}
"""The set of all binary operators available in tt.

:type: Set{:class:`BooleanOperator`}

"""

NON_PRIMITIVE_OPERATORS = BINARY_OPERATORS - {TT_AND_OP, TT_OR_OP}
"""The set of non-primitive operators available in tt.

This includes all binary operators other than AND and OR.

:type: Set{:class:`BooleanOperator`}

"""


SYMBOLIC_OPERATOR_MAPPING = {
    '~': TT_NOT_OP,
    '!': TT_NOT_OP,

    '->': TT_IMPL_OP,

    '<->': TT_XNOR_OP,

    '&&': TT_AND_OP,
    '&': TT_AND_OP,
    '/\\': TT_AND_OP,

    '||': TT_OR_OP,
    '|': TT_OR_OP,
    '\\/': TT_OR_OP
}
"""A mapping of Boolean operators.

This mapping includes the symbolic variants of the available Boolean
operators.

:type: Dict{:class:`str <python:str>`: :class:`BooleanOperator`}

"""

PLAIN_ENGLISH_OPERATOR_MAPPING = {
    'not': TT_NOT_OP,
    'NOT': TT_NOT_OP,

    'xor': TT_XOR_OP,
    'XOR': TT_XOR_OP,

    'impl': TT_IMPL_OP,
    'IMPL': TT_IMPL_OP,

    'iff': TT_XNOR_OP,
    'IFF': TT_XNOR_OP,

    'xnor': TT_XNOR_OP,
    'XNOR': TT_XNOR_OP,
    'nxor': TT_XNOR_OP,
    'NXOR': TT_XNOR_OP,

    'and': TT_AND_OP,
    'AND': TT_AND_OP,

    'nand': TT_NAND_OP,
    'NAND': TT_NAND_OP,

    'or': TT_OR_OP,
    'OR': TT_OR_OP,

    'nor': TT_NOR_OP,
    'NOR': TT_NOR_OP
}
"""A mapping of Boolean operators.

This mapping includes the plain-English variants of the available Boolean
operators.

:type: Dict{:class:`str <python:str>`: :class:`BooleanOperator`}

"""

OPERATOR_MAPPING = {}
"""A mapping of all available Boolean operators.

This dictionary is the concatentation of the
:data:`PLAIN_ENGLISH_OPERATOR_MAPPING` and :data:`SYMBOLIC_OPERATOR_MAPPING`
dictionaries.

:type: Dict{:class:`str <python:str>`: :class:`BooleanOperator`}

"""

OPERATOR_MAPPING.update(PLAIN_ENGLISH_OPERATOR_MAPPING)
OPERATOR_MAPPING.update(SYMBOLIC_OPERATOR_MAPPING)

MAX_OPERATOR_STR_LEN = max(len(k) for k in OPERATOR_MAPPING.keys())
"""The length of the longest operator from :data:`OPERATOR_MAPPING`.

:type: :class:`int <python:int>`

"""
