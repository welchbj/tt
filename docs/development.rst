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

Testing is done with Python's `unittest`_ and `doctest`_ modules. All tests can be run using the ``ttasks.py`` script::

    python ttasks.py test

Note that while doc tests are used, this is mostly just to make sure the documentation examples are valid. The true behavior of the library and public contract is enforced through unit tests.

Cross-Python version testing is achieved through `tox`_. To run changes against the reference and style tests, simply invoke ``tox`` from the top-level directory of the project; tox will run the unit tests against the compatible CPython runtimes. Additionally, the source is run through the `Flake8`_ linter. Whenever new code is pushed to the repo, this same set of `tox`_ tests is run on `AppVeyor`_ (for Windows builds). A separate configuration is used for `Travis CI`_, which tests on Linux and also adds the ability to test on the `PyPy`_ runtime.


Style
-----

tt aims to be strictly `PEP8`_ compliant, enforcing this compliance via `Flake8`_. This project includes an `editorconfig`_ file to help with formatting issues, as well.


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
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _tox: https://tox.readthedocs.org/en/latest/
.. _Travis CI: https://travis-ci.org/welchbj/tt/
.. _AppVeyor: https://ci.appveyor.com/project/welchbj/tt
.. _PyPy: https://pypy.org/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Flake8: http://flake8.pycqa.org/en/latest/
.. _editorconfig: http://editorconfig.org/
