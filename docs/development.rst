===========
Development
===========

If you'd like to help out with the development of tt, we'd love to have you. Below are some helpful tips for working on this library. Feel free to :doc:`reach out </author>` with any questions about getting involved in this project.


Managing with ``ttasks.py``
---------------------------

tt ships with a script ``ttasks.py`` (tt + tasks = ttasks) in the project's top-level directory to help manage common project tasks such as running tests, building the docs, and serving the docs via a live-reload server. You will see this script referenced below.


Dependencies
------------

This project uses `uv`_ to manage its dependencies. To create a new virtual environment with `uv`, use::

    uv venv
    source .venv/bin/activate

Development dependencies can then be installed into this virtual environment with::

    uv install


Testing
-------

Testing is done with Python's `unittest`_ and `doctest`_ modules. All tests can be run using the ``ttasks.py`` script::

    python ttasks.py test

Note that while doc tests are used, their main purpose is to ensure the documentation examples are valid rather than extensively test functionality. The true behavior of the library and its public contract are enforced through the unit tests.

Local cross-Python version testing is achieved through `tox`_. To run changes against the reference and style tests, simply invoke ``tox .`` from the top-level directory of the project; tox will run the unit tests against the compatible CPython runtimes.


Coding Style
------------

tt aims to be strictly `PEP8`_ compliant, enforcing this compliance via `Ruff`_. This project also includes an `editorconfig`_ file to help with formatting issues.

Code linting and formatting checks can be performed with::

    ruff check .
    ruff format --check .

Code formatting can be applied with::

    ruff format .


Documentation
-------------

To build the docs from source, run the following::

    python ttasks.py build-docs

If you're going to be working for a little while, it's usually more convenient to boot up a live-reload server that will re-build the docs on any source file change. To run one on port 5000 of your machine, run::

    python ttasks.py build-docs && python ttasks.py serve-docs


Releases
--------

TODO: Describe uv-based workflow


.. _uv: https://docs.astral.sh/uv/
.. _unittest: https://docs.python.org/3/library/unittest.html
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _tox: https://tox.readthedocs.org/en/latest/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Ruff: https://docs.astral.sh/ruff/
.. _editorconfig: http://editorconfig.org/
