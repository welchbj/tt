|pypi| |pyversions| |docs| |nixbuild| |winbuild|

Synopsis
--------

tt is a library aiming to provide a Pythonic toolkit for working with Boolean expressions. Please check out the `project site`_ for more information.

Installation
------------

tt is tested on CPython 2.7, 3.3, 3.4, 3.5, and 3.6. You can get the latest release from PyPI with::

    pip install ttable

Features
--------

tt lets you do a few things with your prized Boolean expressions. Let's start by parsing one::

    >>> from tt import BooleanExpression
    >>> b = BooleanExpression('A impl not (B nand C)')
    >>> b.tokens
    ['A', 'impl', 'not', '(', 'B', 'nand', 'C', ')']
    >>> b.symbols
    ['A', 'B', 'C']
    >>> print(b.tree)
    impl
    `----A
    `----not
         `----nand
              `----B
              `----C

Then transform it a couple of times::

    >>> from tt import apply_de_morgans, to_cnf, to_primitives
    >>> b = to_primitives(b)
    >>> b
    <BooleanExpression "not A or not (not B or not C)">
    >>> b = apply_de_morgans(b)
    >>> b
    <BooleanExpression "not A or (not not B and not not C)">
    >>> b = to_cnf(b)
    >>> b
    <BooleanExpression "(not A or B) and (not A or C)">

Poke around its structure::

    >>> b.is_cnf
    True
    >>> b.is_dnf
    False
    >>> for clause in b.iter_clauses():
    ...     print(clause)
    ...
    not A or B
    not A or C

Find all of its SAT solutions::

    >>> for sat_solution in b.sat_all():
    ...     print(sat_solution)
    ...
    A=0, B=1, C=1
    A=0, B=1, C=0
    A=0, B=0, C=1
    A=0, B=0, C=0
    A=1, B=1, C=1

Or just find one::

    >>> with b.constrain(A=1):
    ...     b.sat_one()
    ...
    <BooleanValues [A=1, B=1, C=1]>

Turn it into a truth table::

    >>> from tt import TruthTable
    >>> t = TruthTable(b)
    >>> print(t)
    +---+---+---+---+
    | A | B | C |   |
    +---+---+---+---+
    | 0 | 0 | 0 | 1 |
    +---+---+---+---+
    | 0 | 0 | 1 | 1 |
    +---+---+---+---+
    | 0 | 1 | 0 | 1 |
    +---+---+---+---+
    | 0 | 1 | 1 | 1 |
    +---+---+---+---+
    | 1 | 0 | 0 | 0 |
    +---+---+---+---+
    | 1 | 0 | 1 | 0 |
    +---+---+---+---+
    | 1 | 1 | 0 | 0 |
    +---+---+---+---+
    | 1 | 1 | 1 | 1 |
    +---+---+---+---+

And compare it to another truth table::

    >>> other_table = TruthTable(from_values='111x00x1')
    >>> other_table.ordering
    ['A', 'B', 'C']
    >>> for inputs, result in other_table:
    ...     print(inputs, '=>', result)
    ...
    A=0, B=0, C=0 => True
    A=0, B=0, C=1 => True
    A=0, B=1, C=0 => True
    A=0, B=1, C=1 => x
    A=1, B=0, C=0 => False
    A=1, B=0, C=1 => False
    A=1, B=1, C=0 => x
    A=1, B=1, C=1 => True
    >>> other_table.equivalent_to(t)
    True


License
-------

tt uses the `MIT License`_.


.. _MIT License: https://opensource.org/licenses/MIT
.. _project site: http://tt.bwel.ch

.. |pypi| image:: https://img.shields.io/pypi/v/ttable.svg?style=flat-square&label=pypi
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt's PyPI page

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/ttable.svg?style=flat-square
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt runs on Python 2.7, 3.3, 3.4, 3.5, and 3.6

.. |docs| image:: https://img.shields.io/badge/docs-latest-c944ff.svg?style=flat-square
    :target: http://tt.bwel.ch/en/latest/
    :alt: tt documentation site

.. |nixbuild| image:: https://img.shields.io/travis/welchbj/tt/develop.svg?style=flat-square&label=mac%2Flinux%20build
    :target: https://travis-ci.org/welchbj/tt
    :alt: Linux build on Travis CI

.. |winbuild| image:: https://img.shields.io/appveyor/ci/welchbj/tt/develop.svg?style=flat-square&label=windows%20build
    :target: https://ci.appveyor.com/project/welchbj/tt
    :alt: Windows build on AppVeyor
