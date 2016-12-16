"""Utilities for asserting inputs and states."""

from ..definitions import BOOLEAN_VALUES
from ..errors import (ExtraSymbolError, InvalidBooleanValueError,
                      MissingSymbolError)


def assert_iterable_contains_all_expr_symbols(iterable, reference_set):
    """Assert that all values in the passed reference set are in the iterable.

    Args:
        iterable: An iterable of strings to assert.
        reference_set (Set[str]): A set of strings, each of which will be
            asserted to be present in the passed iterable.

    Notes:
        This function will consume the passed iterable.

    """
    passed_symbol_set = set(iterable)
    diff_set = reference_set - passed_symbol_set
    if diff_set:
        msg = 'Did not receive value for the following symbols: '
        msg += ', '.join('"{}"'.format(sym) for sym in diff_set)
        raise MissingSymbolError(msg)


def assert_all_valid_keys(symbol_input_dict, symbol_set):
    """Assert that all keys in the passed input dict are valid.

    Valid keys are considered those that are present in the passed set of
    symbols and that map to valid Boolean values.

    Args:
        symbol_input_dict (Dict): A dict containing symbol names mapping to
            what should be Boolean values.
        symbol_set (Set[str]): A set of the symbol names expected to

    Raises:
        ExtraSymbolError: If any keys in the passed input dict are not present
            in the passed set of symbols.
        InvalidBooleanValueError: If any values in the passed input dict are
            not valid Boolean values (``1``, ``0``, ``True``, or ``False``).

    """
    for k, v in symbol_input_dict.items():
        if k not in symbol_set:
            raise ExtraSymbolError(
                '"{}" is not a symbol in this expression'.format(k))

        if v not in BOOLEAN_VALUES:
            raise InvalidBooleanValueError(
                '"{}" passed as value for "{}" is not a valid Boolean '
                'value'.format(v, k))
