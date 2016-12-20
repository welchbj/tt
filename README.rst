Synopsis
--------

tt is a Python library and command-line tool for working with Boolean expressions. This README provides a high level glance at the project; please check out the `project site`_ for more information.

Installation
------------

tt has been tested with Python 2.7, 3.3, 3.4, and 3.5 and is written in pure Python with no dependencies, so it only requires a compatible Python installation to run. You can get the latest release from PyPI with::

    pip install ttable

Basic Usage
-----------

Below are a couple of examples to show you the kind of things tt can do. For more examples and further documentation, take a look at the `project site`_.

As a Library
````````````

tt aims to provide a Pythonic interface for working with Boolean expressions. Here are some simple examples from the REPL::

    >>> from tt import BooleanExpression, TruthTable
    >>> b = BooleanExpression('A xor (B or C)')
    >>> b.tokens
    ['A', 'xor', '(', 'B', 'or', 'C', ')']
    >>> print(b.tree)
    xor
    `----A
    `----or
        `----B
        `----C
    >>> b.evaluate(A=True, B=False, C=True)
    False
    >>> t = TruthTable(b)
    >>> print(t)
    +---+---+---+---+
    | A | B | C |   |
    +---+---+---+---+
    | 0 | 0 | 0 | 0 |
    +---+---+---+---+
    | 0 | 0 | 1 | 1 |
    +---+---+---+---+
    | 0 | 1 | 0 | 1 |
    +---+---+---+---+
    | 0 | 1 | 1 | 1 |
    +---+---+---+---+
    | 1 | 0 | 0 | 1 |
    +---+---+---+---+
    | 1 | 0 | 1 | 0 |
    +---+---+---+---+
    | 1 | 1 | 0 | 0 |
    +---+---+---+---+
    | 1 | 1 | 1 | 0 |
    +---+---+---+---+
    >>> t = TruthTable('A or B', fill_all=False)
    >>> print(t)
    Empty!
    >>> t.fill(A=0)
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 1 |
    +---+---+---+
    >>> t.fill(A=1)
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
    | 1 | 1 | 1 |
    +---+---+---+


From the Command Line
`````````````````````

tt also provides a command-line interface for working with expressions. Here are a couple of examples::

    $ tt tokens "(op1 nand op2) xnor op3"
    (
    op1
    nand
    op2
    )
    xnor
    op3

    $ tt table A or B
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 1 |
    +---+---+---+
    | 1 | 0 | 1 |
    +---+---+---+
    | 1 | 1 | 1 |
    +---+---+---+

    $ tt tree A or or B
    Error! Unexpected binary operator "or":
    A or or B
         ^


License
-------

tt uses the `MIT License`_.

.. _MIT License: https://opensource.org/licenses/MIT
.. _project site: http://tt.bwel.ch
