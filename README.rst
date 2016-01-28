*******************************************
tt - a Boolean algebra command-line utility
*******************************************

-----

|pypi| |nixbuild| |winbuild|

-----

.. contents::
    :local:
    :depth: 1
    :backlinks: none

========
Synopsis
========

tt is a command line tool for truth table and Karnuagh Map generation.
It currently features syntax checking of Boolean equations and output of corresponding truth tables.

============
Installation
============

tt has been tested with Python 2.7, 3.3, 3.4, and 3.5.
tt is written in pure Python, so it only requires a compatible Python installation to run.

You can get the latest release from PyPI. Right now, the PyPI version only works with Python 3.4 and 3.5. Just use::

    $ pip install ttable

Using this method, you can invoke tt with::

    $ tt

If you want to get the most up to date stable version, you can get the sources directly with::

    $ git clone https://github.com/welchbj/tt.git && cd tt && git checkout develop

If you install tt using the git approach, you will have to invoke it directly with Python.
This can be done with::

    $ python -m tt

================
Command Line Use
================

All you need to specify to tt is your Boolean equation, which can be optionally
surrouded in double quotes. Right now, tt assumes that your output variable will be on the left side of your equals sign and that
the equivalent expression will be on the right side of the equals sign.

You can use the ``--table`` option to output a truth table of your passed equation. Omitting all options
except for the required equation will default to truth table generation, too. 

A simple example::

    $ tt --table F = A and B
    +---+---+---+
    | A | B | F |
    +---+---+---+
    | 0 | 0 | 0 |
    | 0 | 1 | 0 |
    | 1 | 0 | 0 |
    | 1 | 1 | 1 |
    +---+---+---+

tt can handle more complex variable names, too::

    $ tt --table out = operand_1 or operand_2
    +-----------+-----------+-----+
    | operand_1 | operand_2 | out |
    +-----------+-----------+-----+
    |     0     |     0     |  0  |
    |     0     |     1     |  1  |
    |     1     |     0     |  1  |
    |     1     |     1     |  1  |
    +-----------+-----------+-----+

tt can handle more complex Boolean operations and syntax, as well::

    $ tt --table out = (op1 xor (op2 and op3)) nand op4
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

tt doesn't limit you to plain English operations, either. The equation is surrounded in quotes below
to avoid escaping the | and & characters in the terminal::

    $ tt --table "F = ~(A || B) && C"
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

And if you wanted a Karnaugh Map for that equation::

    $ tt --kmap "F = ~(A || B) && C"
    A \ B C

        00      01      11      10
      +-------+-------+-------+-------+
    0 | 0     | 1     | 3     | 2     |
      |   0   |   1   |   0   |   0   |
      |       |       |       |       |
      +-------+-------+-------+-------+
    1 | 4     | 5     | 7     | 6     |
      |   0   |   0   |   0   |   0   |
      |       |       |       |       |
      +-------+-------+-------+-------+

tt provides syntax checking for your equations, too. Below are a few examples.

Too many equals signs::

    $ tt "out == A or B"
    ERROR: Unexpected equals sign.
    ERROR: out == A or B
    ERROR:      ^

Unbalanced parentheses::

    $ tt --table "out = ((A and B) or C))"
    ERROR: Unbalanced right parenthesis.
    ERROR: ((A and B) or C))
    ERROR:                 ^

Malformed equation::

    $ tt out = A or (B and and C)
    ERROR: Unexpected operation.
    ERROR: A or (B and and C)
    ERROR:             ^

===========
Development
===========

The tt development pipeline was built with all major OSes in mind, and all command line
instructions should be identical no matter what terminal or cmd prompt you're using. 
All common development tasks should have a corresponding make target (either in make.bat or the Makefile). 
If you can't find a target that you find yourself needing frequently, please feel free to add it!
Please note, though, that the two "make" files are meant to be functionally equivalent, 
so please don't change one without updating the other.

It is recommended that all development is done in a `virtualenv`_. `virtualenvwrapper`_ is super helpful, too.

Please note: All below examples are assumed to be done from within the top-level tt directory;
this is where the make files reside.

The dependencies for different setups of tt environments are defined in the tt\\reqs directory.
For development, you can install the appropriate development packages with::

    $ make install-reqs

This file can easily be updated with your current environment's installed packages with
the target::

    $ make write-reqs

We ask that you update the production requirements.txt manually, as there should be significantly fewer
required packages for the published releases and we want to keep the install as lean as possible.

Running tt's tests is pretty easy, too. You can run all the Python unittests at once with::

    $ make test

Alternatively, you can invoke the Python unittest module directly to run different groups
of tests::

    $ python -m unittest discover -s tt\tests\unit
    $ python -m unittest discover -s tt\tests\functional

For formatting of the code, tt tries to follow `PEP8`_ closely. flake8 is used to ensure that the code complies
with this standard. Additionally, `Google style`_ docstrings are used. The docstrings in tt are modelled after 
the nice examples in the `napoleon documentation`_. 

tt is designed to be a thoroughly tested application. Its test are divided into two groups:

    #. unit - For testing individual methods and pieces of functionality
    #. functional - For simulating actual use of the application by capturing what is sent to stdout and stderr

Cross Python version testing is made easy with `tox`_. The configuration of the `tox.ini`_ file allows for the proper
testing against Python 2.7, 3.3, 3.4, and 3.5 just by invoking the ``tox`` command in the top-level directory of the project, 
regardless of your platform. The flexiblity of `tox`_ makes tt's CI on `Travis CI`_ and `AppVeyor`_ pretty seamless. 

The git structure of tt is pretty simple, as tt is a pretty simple application itself. Each release has its own 
branch. Branch names are in the form v{major.minor}. If a branch passes the builds by `Travis CI` and `AppVeyor`, then
it is considered stable and should be merged into the develop branch.

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

        #. introduce the project's setup.py file
        #. add Windows make file
        #. improve requirements management, for both production and development
        #. update README, in reStructuredText instead of markdown
        #. introduce functional test framework
        #. initial publish to PyPI

    * v0.3

        #. integrate with Travis CI
        #. integrate with AppVeyor
        #. integrate with Coveralls
        #. introduce Karnaugh Map functionality
        #. add indication of optimal groupings on Karnaugh Maps
        #. port Windows make file to \*nix

    * v0.4

        #. improve verbose output and logging
        #. add option to order inputs in truth table alphabetically (--alphabetical)
        #. product-of-sum (--pos) and sum-of-product (--sop) form generation for Boolean equations
        #. introduce functionality to generate logic circuit diagrams from equations

    * v0.5

        #. if too many options are present, we can look into the idea of using argument sub-groups (already supported by Python's argparse)
        #. add more Boolean operations, such as "if and only if" (<->) and "implies" (->)
        #. improve FunctionalTestCase's output diff for expected vs actual stdout/stderr

=======
License
=======

tt uses the `MIT License`_.

.. _virtualenv: https://virtualenv.readthedocs.org/en/latest/userguide.html
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Google style: https://google.github.io/styleguide/pyguide.html 
.. _napoleon documentation: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html
.. _tox: https://tox.readthedocs.org/en/latest/
.. _tox.ini: https://github.com/welchbj/tt/blob/develop/tox.ini
.. _Travis CI: https://travis-ci.org/welchbj/tt/
.. _AppVeyor: https://ci.appveyor.com/project/welchbj/tt
.. _MIT License: https://opensource.org/licenses/MIT

.. |pypi| image:: https://img.shields.io/pypi/v/ttable.svg?style=flat-square&label=pypi
    :target: https://pypi.python.org/pypi/ttable
    :alt: tt's PyPI page

.. |nixbuild| image:: https://img.shields.io/travis/welchbj/tt/develop.svg?style=flat-square&label=mac%2Flinux%20build
    :target: https://travis-ci.org/welchbj/tt
    :alt: Mac/Linux build on Travis CI

.. |winbuild| image:: https://img.shields.io/appveyor/ci/welchbj/tt/develop.svg?style=flat-square&label=windows%20build
    :target: https://ci.appveyor.com/project/welchbj/tt
    :alt: Windows build on AppVeyor

.. contents::
    :local:
    :depth: 1
    :backlinks: none
