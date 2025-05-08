Synopsis
--------

tt (**t**\ ruth **t**\ able) is a library aiming to provide a toolkit for working with Boolean expressions and truth tables. Please see the `project site`_ for guides and documentation.

Installation
------------

tt is tested on the latest three major versions of CPython. You can get the latest release from PyPI with::

    pip install ttable

Features
--------

Parse expressions::

    >>> from tt import BooleanExpression
    >>> b = BooleanExpression('A impl not (B nand C)')
    >>> b.tokens
    ['A', 'impl', 'not', '(', 'B', 'nand', 'C', ')']
    >>> print(b.tree)
    impl
    `----A
    `----not
         `----nand
              `----B
              `----C

Evaluate expressions::

    >>> b = BooleanExpression('(A /\\ B) -> (C \\/ D)')
    >>> b.evaluate(A=1, B=1, C=0, D=0)
    False
    >>> b.evaluate(A=1, B=1, C=1, D=0)
    True

Interact with expression structure::

    >>> b = BooleanExpression('(A and ~B and C) or (~C and D) or E')
    >>> b.is_dnf
    True
    >>> for clause in b.iter_dnf_clauses():
    ...     print(clause)
    ...
    A and ~B and C
    ~C and D
    E

Apply expression transformations::

    >>> from tt import to_primitives, to_cnf
    >>> to_primitives('A xor B')
    <BooleanExpression "(A and not B) or (not A and B)">
    >>> to_cnf('(A nand B) impl (C or D)')
    <BooleanExpression "(A or C or D) and (B or C or D)">

Or create your own::

    >>> from tt import tt_compose, apply_de_morgans, coalesce_negations, twice
    >>> b = BooleanExpression('not (not (A or B))')
    >>> f = tt_compose(apply_de_morgans, twice)
    >>> f(b)
    <BooleanExpression "not not A or not not B">
    >>> g = tt_compose(f, coalesce_negations)
    >>> g(b)
    <BooleanExpression "A or B">

Exhaust SAT solutions::

    >>> b = BooleanExpression('~(A or B) xor C')
    >>> for sat_solution in b.sat_all():
    ...     print(sat_solution)
    ...
    A=0, B=0, C=0
    A=1, B=0, C=1
    A=0, B=1, C=1
    A=1, B=1, C=1

Find just a few::

    >>> with b.constrain(A=1):
    ...     for sat_solution in b.sat_all():
    ...         print(sat_solution)
    ...
    A=1, B=0, C=1
    A=1, B=1, C=1

Or just one::

    >>> b.sat_one()
    <BooleanValues [A=0, B=0, C=0]>

Build truth tables::

    >>> from tt import TruthTable
    >>> t = TruthTable('A iff B')
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 1 |
    +---+---+---+
    | 0 | 1 | 0 |
    +---+---+---+
    | 1 | 0 | 0 |
    +---+---+---+
    | 1 | 1 | 1 |
    +---+---+---+

And `much more`_!

License
-------

tt uses the `MIT License`_.


.. _MIT License: https://opensource.org/licenses/MIT
.. _project site: https://tt.brianwel.ch
.. _bool.tools: http://www.bool.tools
.. _much more: https://tt.brianwel.ch/en/latest/user_guide.html
