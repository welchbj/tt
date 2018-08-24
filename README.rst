|pypi| |pyversions| |docs| |nixbuild| |winbuild|

Synopsis
--------

tt (**t**\ ruth **t**\ able) is a library aiming to provide a Pythonic toolkit for working with Boolean expressions and truth tables. Please see the `project site`_ for guides and documentation, or check out `bool.tools`_ for a simple web application powered by this library.

Installation
------------

tt is tested on CPython 2.7, 3.3, 3.4, 3.5, and 3.6. You can get the latest release from PyPI with::

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

    >>> b = BooleanExpression('(A /\ B) -> (C \/ D)')
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
    A=0, B=1, C=1
    A=1, B=0, C=1
    A=1, B=1, C=1
    A=0, B=0, C=0

Find just a few::

    >>> with b.constrain(A=1):
    ...     for sat_solution in b.sat_all():
    ...         print(sat_solution)
    ...
    A=1, B=0, C=1
    A=1, B=1, C=1

Or just one::

    >>> b.sat_one()
    <BooleanValues [A=0, B=1, C=1]>

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
.. _project site: http://tt.brianwel.ch
.. _bool.tools: http://www.bool.tools
.. _much more: http://tt.brianwel.ch/en/stable/user_guide.html

.. |pypi| image:: https://img.shields.io/pypi/v/ttable.svg?style=flat-square&label=pypi
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt's PyPI page

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/ttable.svg?style=flat-square
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt runs on Python 2.7, 3.3, 3.4, 3.5, and 3.6

.. |docs| image:: https://img.shields.io/badge/docs-latest-c944ff.svg?style=flat-square
    :target: http://tt.brianwel.ch/en/latest/
    :alt: tt documentation site

.. |nixbuild| image:: https://img.shields.io/travis/welchbj/tt/develop.svg?style=flat-square&label=mac%2Flinux%20build
    :target: https://travis-ci.org/welchbj/tt
    :alt: Linux build on Travis CI

.. |winbuild| image:: https://img.shields.io/appveyor/ci/welchbj/tt/develop.svg?style=flat-square&label=windows%20build
    :target: https://ci.appveyor.com/project/welchbj/tt
    :alt: Windows build on AppVeyor
