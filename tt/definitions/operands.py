"""Definitions related to operands."""

import re
from keyword import kwlist


BOOLEAN_VALUES = {0, 1, True, False}
"""Set of truthy values valid to submit for evaluation.

:type: Set[:class:`int <python:int>`, :class:`bool <python:bool>`]

"""


DONT_CARE_VALUE = 'x'
"""The don't care string identifier.

:type: :class:`str <python:str>`

"""


# False, True not considered keywords in Python 2
_tt_keywords = set(kwlist) | {'False', 'True'}


def is_valid_identifier(identifier_name):
    """Returns whether the string is a valid symbol identifier.

    Valid identifiers are those that follow Python variable naming conventions
    and are not Python keywords.

    :param identifier_name: The string to test.
    :type identifier_name: :class:`str <python:str>`

    :returns: True if the passed string is valid identifier, otherwise False.
    :rtype: :class:`bool <python:bool>`

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

    ."""
    identifier_re = re.compile(r'^[^\d\W]\w*\Z', re.UNICODE)
    valid_re = re.match(identifier_re, identifier_name) is not None
    return valid_re and identifier_name not in _tt_keywords
