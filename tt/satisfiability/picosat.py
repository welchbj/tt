"""Python wrapper around the _clibs PicoSAT extension."""

import os

from tt.errors.arguments import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)

if os.environ.get('READTHEDOCS') != 'True':
    from tt._clibs import picosat as _c_picosat
    VERSION = _c_picosat.VERSION


def sat_one(clauses, assumptions=None):
    """Find a solution that satisfies the specified clauses and assumptions.

    This provides a light Python wrapper around the same method in the PicoSAT
    C-extension. While completely tested and usable, this method is probably
    not as useful as the interface provided through the
    :func:`sat_one <tt.expressions.bexpr.BooleanExpression.sat_one>` method in
    the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`
    class.

    :param clauses: CNF (AND of ORs) clauses; positive integers represent
        non-negated terms and negative integers represent negated terms.
    :type clauses: List[List[:class:`int <python:int>`]]

    :param assumptions: Assumed terms; same negation logic from ``clauses``
        applies here. Note that assumptions *cannot* be an empty list; leave it
        as ``None`` if there are no assumptions to include.
    :type assumptions: List[:class:`int <python:int>`]

    :returns: If solution is found, a list of ints representing the terms of
        the solution; otherwise, if no solution found, ``None``.
    :rtype: List[:class:`int <python:int>`] or ``None``

    :raises InvalidArgumentTypeError: If ``clauses`` is not a list of lists of
        ints or ``assumptions`` is not a list of ints.
    :raises InvalidArgumentValueError: If any literal ints are equal to zero.

    Let's look at a simple example with no satisfiable solution::

        >>> from tt import picosat
        >>> picosat.sat_one([[1], [-1]]) is None
        True

    Here's an example where a solution exists::

        >>> picosat.sat_one([[1, 2, 3], [-2, -3], [1, -2], [2, -3], [-2]])
        [1, -2, -3]

    Finally, here's an example using assumptions::

        >>> picosat.sat_one([[1, 2, 3], [2, 3]], assumptions=[-1, -3])
        [-1, 2, -3]

    """
    try:
        return _c_picosat.sat_one(clauses, assumptions=assumptions)
    except TypeError as e:
        raise InvalidArgumentTypeError(str(e))
    except ValueError as e:
        raise InvalidArgumentValueError(str(e))


def sat_all(clauses, assumptions=None):
    """Find all solutions that satisfy the specified clauses and assumptions.

    This provides a light Python wrapper around the same method in the PicoSAT
    C-extension. While completely tested and usable, this method is probably
    not as useful as the interface provided through the
    :func:`sat_all <tt.expressions.bexpr.BooleanExpression.sat_all>` method in
    the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`
    class.

    :param clauses: CNF (AND of ORs) clauses; positive integers represent
        non-negated terms and negative integers represent negated terms.
    :type clauses: List[List[:class:`int <python:int>`]]

    :param assumptions: Assumed terms; same negation logic from ``clauses``
        applies here. Note that assumptions *cannot* be an empty list; leave it
        as ``None`` if there are no assumptions to include.
    :type assumptions: List[:class:`int <python:int>`]

    :returns: An iterator of solutions; if no satisfiable solutions exist, the
        iterator will be empty.
    :rtype: Iterator[List[:class:`int <python:int>`]]

    :raises InvalidArgumentTypeError: If ``clauses`` is not a list of lists of
        ints or ``assumptions`` is not a list of ints.
    :raises InvalidArgumentValueError: If any literal ints are equal to zero.

    Here's an example showing the basic usage::

        >>> from tt import picosat
        >>> for solution in picosat.sat_all([[1], [2, 3, 4], [2, 3]]):
        ...     print(solution)
        ...
        [1, 2, 3, 4]
        [1, 2, 3, -4]
        [1, 2, -3, 4]
        [1, 2, -3, -4]
        [1, -2, 3, 4]
        [1, -2, 3, -4]

    We can cut down on some of the above solutions by including an assumption::

        >>> for solution in picosat.sat_all([[1], [2, 3, 4], [2, 3]],
        ...                                 assumptions=[-3]):
        ...     print(solution)
        ...
        [1, 2, -3, 4]
        [1, 2, -3, -4]

    """
    try:
        return _c_picosat.sat_all(clauses, assumptions=assumptions)
    except TypeError as e:
        raise InvalidArgumentTypeError(str(e))
    except ValueError as e:
        raise InvalidArgumentValueError(str(e))
