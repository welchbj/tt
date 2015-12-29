WARNING:
If you are reading this page, this is a working copy. None of the code examples (specifically anything
related to installing from PyPI) are guaranteed/expected to work. Please use the README file on the master branch
as a reference for featues currently present in tt.

.. contents::
    :local:
    :depth: 1
    :backlinks: none

========
Synopsis
========

tt is a command line tool for truth table and, in the future, Karnaugh Map generation.
It currently features syntax checking of Boolean equations and output of corresponding truth tables.

============
Installation
============

tt was developed in Python 3 and no effort has been made for compatibility with Python 2.
tt was written in pure Python, so it only requires a Python installation to run.

You can get the latest release from PyPI. Just use::

    $ pip install ttable

Using this method, you can invoke tt with::

    $ tt "F = A or B"

If you want to get the most up to date stable version, you can get the sources directly with::

    $ git clone https://github.com/welchbj/tt.git
    $ cd tt

If you install tt using the git approach, you will have to invoke it directly with Python.
This can be done with::

    $ python [-m] tt "F = A or B"

================
Command Line Use
================

All you need to specify to tt is your Boolean equation (surrounded in quotes).
Right now, tt assumes that your output variable will be on the left side of your equals sign and that
the equivalent expression will be on the right side of the equals sign.

A simple example::

    $ tt "F = A and B"
    +---+---+---+
    | A | B | F |
    +---+---+---+
    | 0 | 0 | 0 |
    | 0 | 1 | 0 |
    | 1 | 0 | 0 |
    | 1 | 1 | 1 |
    +---+---+---+

tt can handle more complex variable names, too::

    $ tt "out = operand_1 or operand_2"
    +-----------+-----------+-----+
    | operand_1 | operand_2 | out |
    +-----------+-----------+-----+
    |     0     |     0     |  0  |
    |     0     |     1     |  1  |
    |     1     |     0     |  1  |
    |     1     |     1     |  1  |
    +-----------+-----------+-----+

tt can handle more complex Boolean operations and syntax, as well::

    $ tt "out = (op1 xor (op2 and op3)) nand op4"
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

    $ tt "F = ~(A || B) && C"
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

    $ tt "out == A or B"
    ERROR: Unexpected equals sign.
    ERROR: out == A or B
    ERROR:      ^

Unbalanced parentheses::

    $ tt "out = ((A and B) or C))"
    ERROR: Unbalanced right parenthesis.
    ERROR: ((A and B) or C))
    ERROR:                 ^

Malformed equation::

    $ tt "out = A or (B and and C)"
    ERROR: Unexpected operation.
    ERROR: A or (B and and C)
    ERROR:             ^

===========
Development
===========

The tt development pipeline was built with all major OSes in mind, and all command line
instructions should be identical not matter what terminal or cmd prompt you're using. 
All common development tasks should have a corresponding make target (either in make.bat or the Makefile). 
If you can't find a target that you find yourself needing frequently, please feel free to add it!
Please note, though, that the two "make" files are meant to be functionally equivalent, 
so don't change one without updating the other.

It is recommended that all development is done in a `virtualenv`_. `virtualenvwrapper`_ is super helpful, too.

.. _virtualenv: https://virtualenv.readthedocs.org/en/latest/userguide.html
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/

Please note: All below examples are assumed to be done from within the top-level tt directory;
this is where the make files reside.

The dependencies for different setups of tt environments are defined in the tt\\reqs directory.
For development, you can install the appropriate packages with::

    $ make get-reqs

This file can easily be updated with your current environment's installed packages with
the target::

    $ make write-reqs

We ask that you update the production requirements.txt manually, as there should be significantly fewer
required packages for the published releases and we want to keep the install as lean as possible.

Running tt's tests is pretty easy, too. You can run all the tests at once with::

    $ make test

Or you can run the tests by group::

    $ make test-unit
    $ make test-functional

Alternatively, you can invoke the Python unittest module directly. The same three examples would be run with::

    $ python -m unittest discover -s tt\tests

    $ python -m unittest discover -s tt\tests\unit
    $ python -m unittest discover -s tt\tests\functional

For formatting of the code, tt tries to follow `PEP8`_ closely. flake8 is used to ensure that the code complies
with this standard. Additionally, `Google style`_ docstrings are used. The docstrings in tt are modelled after 
those found in the `napoleon documentation`_. 

.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Google style: https://google.github.io/styleguide/pyguide.html 
.. _napoleon documentation: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html

tt is designed to be a thoroughly tested application. Its test are divided into two groups:

    #. unit - For testing individual methods in isolation
    #. functional - For simulating actual use of the application by capturing what is sent to stdout and stderr

The git structure of tt is pretty simple, as tt is a pretty simple application itself. Each release has its own 
branch. Branch names are in the form v{major.minor}. If a branch is in a working and functional state,
it should be merged into the develop branch. Working and functional is defined as:

    #. Passing all tests
    #. No output from flake8

Once a release is completed, the develop branch will be merged into the master branch, and the master branch 
will be tagged with the corresponding version, in the form release-{major}.{minor}. Following these guideleines, 
any clone from the master or develop branch should yield a functioning version of tt, with master being a fully stable release.

=======
Roadmap
=======

Below indicates what is aimed to be included in the releases leading up to v1.0:

    * v0.1

        #. Initial release

    * v0.2

        #. add make file support
        #. introduce the project's setup.py file
        #. improve requirements management, for both production and development
        #. update README, in reStructuredText instead of markdown
        #. introduce functional test framework
        #. integrate with Travis CI
        #. initial publish to PyPI

    * v0.3

        #. product-of-sum (--pos) and sum-of-product (--sop) form generation for Boolean equations
        #. initial Karnaugh Map generation for equations of up to 4 variables

    * v0.4

        #. add indication of optimal groupings on Karnaugh Maps, perhaps with color via colorama
        #. increase number of variables allowed in Karnaugh Map generation
        #. add --raw modifier to indicate only a plain Karnaugh Map should be output
        #. add --min modifier to --pos and --som forms for minimization of result

    * v0.5

        #. introduce the ability to generate logic circuit diagrams from equations

=======
License
=======

tt uses the `MIT License`_.

.. _MIT License: https://opensource.org/licenses/MIT