========
Synopsis
========

tt is a commandline tool for truth table and, in the future, Karnaugh Map generation.
It currently features syntax checking of Boolean equations and output of corresponding truth tables.

============
Installation
============

tt was developed in a Python 3.4 environment, and has not been extensively tested with any other Python versions.
tt was written in pure Python, so it only requires a Python installation to run.

Right now, the only way to get tt is straight from the source on Github. To do so, use::

    $ git clone https://github.com/welchbj/tt.git
    $ cd tt

================
Command line Use
================

All you need to specify to tt is your Boolean equation (surrounded in quotes).
Right now, tt assumes that your output variable will be on the left side of your equals sign and that
the equivalent expression will be on the right side of the equals sign.

A simple example::

    $ python tt "F = A and B"
    +---+---+---+
    | A | B | F |
    +---+---+---+
    | 0 | 0 | 0 |
    | 0 | 1 | 0 |
    | 1 | 0 | 0 |
    | 1 | 1 | 1 |
    +---+---+---+

tt can handle more complex variable names, too::

    $ python tt "out = operand_1 or operand_2"
    +-----------+-----------+-----+
    | operand_1 | operand_2 | out |
    +-----------+-----------+-----+
    |     0     |     0     |  0  |
    |     0     |     1     |  1  |
    |     1     |     0     |  1  |
    |     1     |     1     |  1  |
    +-----------+-----------+-----+

tt can handle more complex Boolean operations and syntax, as well::

    $ python tt "out = (op1 xor (op2 and op3)) nand op4"
    +-----+-----+-----+-----+-----+
    | op1 | op2 | op3 | op4 | out |
    +-----+-----+-----+-----+-----+
    |  0  |  0  |  0  |  0  |  1  |
    |  0  |  0  |  0  |  1  |  1  |
    |  0  |  0  |  1  |  0  |  1  |
    |  0  |  0  |  1  |  1  |  1  |
    |  0  |  1  |  0  |  0  |  1  |
    |  0  |  1  |  0  |  1  |  1  |
    |  0  |  1  |  1  |  0  |  1  |
    |  0  |  1  |  1  |  1  |  0  |
    |  1  |  0  |  0  |  0  |  1  |
    |  1  |  0  |  0  |  1  |  0  |
    |  1  |  0  |  1  |  0  |  1  |
    |  1  |  0  |  1  |  1  |  0  |
    |  1  |  1  |  0  |  0  |  1  |
    |  1  |  1  |  0  |  1  |  0  |
    |  1  |  1  |  1  |  0  |  1  |
    |  1  |  1  |  1  |  1  |  1  |
    +-----+-----+-----+-----+-----+

tt doesn't limit you to plain English operations, either::

    $ python tt "F = ~(A || B) && C"
    +---+---+---+---+
    | A | B | C | F |
    +---+---+---+---+
    | 0 | 0 | 0 | 0 |
    | 0 | 0 | 1 | 1 |
    | 0 | 1 | 0 | 0 |
    | 0 | 1 | 1 | 0 |
    | 1 | 0 | 0 | 0 |
    | 1 | 0 | 1 | 0 |
    | 1 | 1 | 0 | 0 |
    | 1 | 1 | 1 | 0 |
    +---+---+---+---+

tt provides syntax checking for your equations, too. Below are a few examples.

Too many equals signs::

    $ python tt "out == A or B"
    ERROR: Unexpected equals sign.
    ERROR: out == A or B
    ERROR:      ^

Unbalanced parentheses::

    $ python tt "out = ((A and B) or C))"
    ERROR: Unbalanced right parenthesis.
    ERROR: ((A and B) or C))
    ERROR:                 ^

Malformed equation::

    $ python tt "out = A or (B and and C)"
    ERROR: Unexpected operation.
    ERROR: A or (B and and C)
    ERROR:             ^


=====
Tests
=====

tt's tests were written using the Python unittest module. All of tt's tests can be run from
the top-level tt directory with::

    $ python -m unittest discover -s tt



=======
License
=======

tt uses the MIT License.