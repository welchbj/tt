"""Python wrapper around the _clibs PicoSAT extension."""

import os

from tt.errors.arguments import (InvalidArgumentTypeError,
                                 InvalidArgumentValueError)

if os.environ.get('READTHEDOCS') != 'True':
    from tt._clibs import picosat as _c_picosat
    VERSION = _c_picosat.VERSION


def sat_one(clauses, assumptions=None):
    """Find a solution that satisfies the specified clauses and assumptions.

    This provides a light Python wrapper around the same method in the PicoSAT
    C-extension. While completely tested and usable, this method is probably
    not as useful as the

    :param clauses: CNF (AND of ORs) clauses; positive integers represent
        non-negated terms and negative integers represent negated terms.
    :type clauses: List[List[:class:`int <python:int>`]]

    :param assumptions: Assumed terms; same negation logic from ``clauses``
        applies here.
    :type assumptions: List[:class:`int <python:int>`]

    :returns: If solution is found, a list of ints representing the terms of
        the solution; otherwise, if no solution found, ``None``.
    :rtype: List[:class:`int <python:int>`] or ``None``

    :raises InvalidArgumentTypeError: If ``clauses`` is not a list of lists of
        ints or ``assumptions`` is not a list of ints.
    :raises InvalidArgumentValueError: If any literal ints are equal to zero.

    Example usage::

        >>> from tt import picosat
        >>> # Return None when no solution possible
        ... picosat.sat_one([[1], [-1]]) is None
        True
        >>> # Compute a satisfying solution
        ... picosat.sat_one([[1, 2, 3], [-2, -3], [-3]])
        [1, -2, -3]
        >>> # Include assumptions
        ... picosat.sat_one([[1, 2, 3], [2, 3]], assumptions=[-3])
        [1, 2, -3]

    """
    try:
        return _c_picosat.sat_one(clauses, assumptions=assumptions)
    except TypeError as e:
        raise InvalidArgumentTypeError(str(e))
    except ValueError as e:
        raise InvalidArgumentValueError(str(e))
