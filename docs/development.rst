===========
Development
===========

Managing with ``ttasks.py``
---------------------------

tt ships with a script ``ttasks.py`` (tt + tasks = ttasks) in the project's top-level directory, used to manage common project tasks. You will see it referenced below.


Dependencies
------------

All development requirements for tt are stored in the ``dev-requirements.txt`` file in the project's top-level directory. You can install all of these dependencies with::

    pip install -r dev-requirements.txt


Testing
-------

Testing is done with Python's `unittest`_ module. All tests can be run using the ``ttasks.py`` script::

    python ttasks.py test

Cross-Python version testing is achieved through `tox`_. To run changes against the reference and style tests, simply invoke ``tox`` from the top-level directory of the project; tox will run the unit tests against Python 3.3, 3.4, 3.5, and 3.6 as well as run the source through `Flake8`_. Whenever new code is pushed to the repo, this same set of `tox`_ tests is run on `AppVeyor`_ (for Windows builds). A separate configuration is used for `Travis CI`_ in order to test on Linux and the `PyPy`_ runtime, too.


Style
-----

tt aims to be strictly `PEP8`_ compliant, enforcing this compliance via `Flake8`_. This project includes an `editorconfig`_ file to help with formatting issues, as well. `Google style docstrings`_ are used in the source code code documentation and processed via `napoleon`_.


Long Term Development Goals
---------------------------

Below are features I'd like to add eventually, roughly ordered in anticipated schedule of completion. A new release will be cut every so often down the list.

* For the CLI

    * Functional testing, capturing stdout/stderr
    * Option for interfacing with the truth table's ``fill`` method
    * Option for interfacing with the truth table's ``ordering`` attribute
    * Option for specifying output delimiters for token-listing commands

* For the project as a whole

    * A *Getting Started* section for the docs, with a tutorial-style guide to the library and CLI
    * Karnaugh map support
    * Interface for substituting/transforming expression symbols
    * Functionality for optimizing/simplifying expressions (pos, sop, espresso, etc.)


.. _unittest: https://docs.python.org/3/library/unittest.html
.. _tox: https://tox.readthedocs.org/en/latest/
.. _Travis CI: https://travis-ci.org/welchbj/tt/
.. _AppVeyor: https://ci.appveyor.com/project/welchbj/tt
.. _PyPy: https://pypy.org/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Flake8: http://flake8.pycqa.org/en/latest/
.. _editorconfig: http://editorconfig.org/
.. _Google style docstrings: https://google.github.io/styleguide/pyguide.html
.. _napoleon: http://www.sphinx-doc.org/en/latest/ext/napoleon.html
