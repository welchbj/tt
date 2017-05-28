"""Definitions related to operands."""

import re

from collections import namedtuple
from keyword import kwlist

from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)


BOOLEAN_VALUES = {0, 1, True, False}
"""Set of truthy values valid to submit for evaluation.

:type: Set[:class:`int <python:int>`, :class:`bool <python:bool>`]

"""


DONT_CARE_VALUE = 'x'
"""The don't care string identifier.

:type: :class:`str <python:str>`

"""


# False and True are not considered keywords in Python 2
_tt_keywords = set(kwlist) | {'False', 'True'}


def is_valid_identifier(identifier_name):
    """Returns whether the string is a valid symbol identifier.

    Valid identifiers are those that follow Python variable naming conventions,
    are not Python keywords, and do not begin with an underscore.

    :param identifier_name: The string to test.
    :type identifier_name: :class:`str <python:str>`

    :returns: True if the passed string is valid identifier, otherwise False.
    :rtype: :class:`bool <python:bool>`

    :raises InvalidArgumentTypeError: If ``identifier_name`` is not a string.
    :raises InvalidArgumentValueError: If ``identifier_name`` is an empty
        string.

    As an example::

        >>> from tt import is_valid_identifier
        >>> is_valid_identifier('$var')
        False
        >>> is_valid_identifier('va#r')
        False
        >>> is_valid_identifier('for')
        False
        >>> is_valid_identifier('False')
        False
        >>> is_valid_identifier('var')
        True
        >>> is_valid_identifier('')
        Traceback (most recent call last):
            ...
        tt.errors.arguments.InvalidArgumentValueError: identifier_name cannot \
be empty
        >>> is_valid_identifier(None)
        Traceback (most recent call last):
            ...
        tt.errors.arguments.InvalidArgumentTypeError: identifier_name must be \
a string

    """
    if not isinstance(identifier_name, str):
        raise InvalidArgumentTypeError('identifier_name must be a string')

    if not identifier_name:
        raise InvalidArgumentValueError('identifier_name cannot be empty')

    if identifier_name.startswith('_'):
        return False

    if identifier_name in _tt_keywords:
        return False

    identifier_re = re.compile(r'^[^\d\W]\w*\Z', re.UNICODE)
    if re.match(identifier_re, identifier_name) is None:
        return False

    return True


def boolean_variables_factory(symbols):
    """Returns a class for namedtuple-like objects for holding boolean values.

    :param symbols: A list of the symbol names for which instances of this
        class will hold an entry.
    :type symbols: List[:class:`str <python:str>`]

    :returns: An object where the passed ``symbols`` can be accessed as
        attributes.
    :rtype: :func:`namedtuple <python:collections.namedtuple>`-like object

    This functionality is best demonstrated with an example::

        >>> from tt import boolean_variables_factory
        >>> factory = boolean_variables_factory(['op1', 'op2', 'op3'])
        >>> instance = factory(op1=True, op2=False, op3=False)
        >>> instance.op1
        True
        >>> instance.op2
        False
        >>> print(instance)
        op1=1, op2=0, op3=0
        >>> instance = factory(op1=0, op2=0, op3=1)
        >>> instance.op3
        1
        >>> print(instance)
        op1=0, op2=0, op3=1

    It should be noted that this function is used internally within
    functionality where the validity of inputs is already checked. As such,
    this class won't enforce the Boolean-ness of input values::

        >>> factory = boolean_variables_factory(['A', 'B'])
        >>> instance = factory(A=-1, B='value')
        >>> print(instance)
        A=-1, B=value

    Instances produced from the generated factory are descendants of
    :func:`namedtuple <python:collections.namedtuple>` generated classes; some
    of the inherited attributes may be useful::

        >>> instance = factory(A=True, B=False)
        >>> instance._fields
        ('A', 'B')
        >>> instance._asdict()
        OrderedDict([('A', True), ('B', False)])

    """
    class _bvf(namedtuple('_bvf', symbols)):
        __slots__ = ()

        def __str__(self):
            pairs = []
            for field, val in self._asdict().items():
                val = int(val) if isinstance(val, bool) else val
                pairs.append(field + '=' + str(val))
            return ', '.join(pairs)

        def __repr__(self):
            return '<BooleanValues [{}]>'.format(str(self))

    return _bvf
