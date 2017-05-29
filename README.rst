|pypi| |nixbuild| |winbuild|

Synopsis
--------

tt is a Python library and command-line tool for working with Boolean expressions. Please check out the `project site`_ for more information.

Installation
------------

tt is tested on CPython 2.7, 3.3, 3.4, 3.5, and 3.6. You can get the latest release from PyPI with::

    pip install ttable

Basic Usage
-----------

tt aims to provide a Pythonic interface for working with Boolean expressions. Here are some simple examples from the REPL:

.. code-block:: python

    >>> from tt import BooleanExpression, TruthTable
    >>> b = BooleanExpression('A xor (B and 1)')
    >>> b.tokens
    ['A', 'xor', '(', 'B', 'and', '1', ')']
    >>> b.symbols
    ['A', 'B']
    >>> print(b.tree)
    xor
    `----A
    `----and
         `----B
         `----1
    >>> b.evaluate(A=True, B=False)
    True
    >>> t = TruthTable(b)
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 1 |
    +---+---+---+
    | 1 | 0 | 1 |
    +---+---+---+
    | 1 | 1 | 0 |
    +---+---+---+
    >>> t = TruthTable(from_values='01xx')
    >>> t.ordering
    ['A', 'B']
    >>> for inputs, result in t:
    ...     print(inputs, '=>', result)
    ...
    A=0, B=0 => False
    A=0, B=1 => True
    A=1, B=0 => x
    A=1, B=1 => x
    >>> t.equivalent_to(b)
    True

License
-------

tt uses the `MIT License`_.


.. _MIT License: https://opensource.org/licenses/MIT
.. _project site: http://tt.bwel.ch

.. |pypi| image:: https://img.shields.io/pypi/v/ttable.svg?style=flat-square&label=pypi
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt's PyPI page

.. |nixbuild| image:: https://img.shields.io/travis/welchbj/tt/develop.svg?style=flat-square&label=linux%20build
    :target: https://travis-ci.org/welchbj/tt
    :alt: Linux build on Travis CI

.. |winbuild| image:: https://img.shields.io/appveyor/ci/welchbj/tt/develop.svg?style=flat-square&label=windows%20build
    :target: https://ci.appveyor.com/project/welchbj/tt
    :alt: Windows build on AppVeyor
