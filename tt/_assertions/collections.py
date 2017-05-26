"""Collection and sequence assertion helpers."""

from tt.definitions import BOOLEAN_VALUES
from tt.errors import (
    DuplicateSymbolError,
    ExtraSymbolError,
    InvalidBooleanValueError,
    MissingSymbolError)


def assert_iterable_contains_all_expr_symbols(iter_of_strs, reference_set):
    """Assert a one-to-one presence of all symbols in the passed iterable.

    :param iter_of_strs: An iterable of strings to assert.
    :type iter_of_strs: Iterable[:class:`str <python:str>`]

    :param reference_set: A set of strings, each of which will be asserted to
        be present in the passed iterable.
    :type reference_set: Set[:class:`str <python:str>`]

    .. note::

        This function will consume ``iter_of_strs``.

    :raises DuplicateSymbolError: If the passed iterable contains more than one
        of a given symbol.
    :raises ExtraSymbolError: If the passed iterable contains symbols not
        present in the reference set.
    :raises MissingSymbolError: If the passed iterable is missing symbols
        present in the reference set.

    This assertion is used for validation of user-specified sets of symbols.

    """
    passed_symbol_list = list(iter_of_strs)
    passed_symbol_set = set(passed_symbol_list)
    if len(passed_symbol_list) != len(passed_symbol_set):
        raise DuplicateSymbolError('Received duplicate symbols')

    passed_excess_set = passed_symbol_set - reference_set
    reference_excess_set = reference_set - passed_symbol_set

    if reference_excess_set:
        msg = 'Did not receive value for the following symbols: '
        msg += ', '.join('"{}"'.format(sym) for sym in reference_excess_set)
        raise MissingSymbolError(msg)

    if passed_excess_set:
        msg = 'Received unexpected symbols: '
        msg += ', '.join('"{}"'.format(sym) for sym in passed_excess_set)
        raise ExtraSymbolError(msg)


def assert_all_valid_keys(symbol_input_dict, symbol_set):
    """Assert that all keys in the passed input dict are valid.

    Valid keys are considered those that are present in the passed set of
    symbols and that map to valid Boolean values. Dictionaries cannot have
    duplicate keys, so no duplicate checking is necessary.

    :param symbol_input_dict: A dict containing symbol names mapping to what
        should be Boolean values.
    :type symbol_input_dict: Dict{:class:`str <python:str>`: truthy}

    :param symbol_set: A set of the symbol names expected to be present as keys
        in ``symbol_input_dict``.
    :type symbol_set: Set[:class:`str <python:str>`]

    :raises ExtraSymbolError: If any keys in the passed input dict are not
        present in the passed set of symbols.
    :raises InvalidBooleanValueError: If any values in the passed input dict
        are not valid Boolean values (``1``, ``0``, ``True``, or ``False``).

    This assert is used for validation of user-specified kwargs which map
    symbols to expected values.

    """
    for k, v in symbol_input_dict.items():
        if k not in symbol_set:
            raise ExtraSymbolError(
                '"{}" is not a symbol in this expression'.format(k))

        if v not in BOOLEAN_VALUES:
            raise InvalidBooleanValueError(
                '"{}" passed as value for "{}" is not a valid Boolean '
                'value'.format(v, k))
