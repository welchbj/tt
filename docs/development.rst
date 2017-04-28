===========
Development
===========

If you'd like to help out with tt, we'd love to have you. Below are some helpful tips to development. Feel free to :doc:`reach out </author>` with any questions about development or getting involved.


Managing with ``ttasks.py``
---------------------------

tt ships with a script ``ttasks.py`` (tt + tasks = ttasks) in the project's top-level directory, used to manage common project tasks such as running tests, building the docs, and serving the docs via a live-reload server. You will see this script referenced below.


Dependencies
------------

All development requirements for tt are stored in the ``dev-requirements.txt`` file in the project's top-level directory. You can install all of these dependencies with::

    pip install -r dev-requirements.txt


Testing
-------

Testing is done with Python's `unittest`_ and `doctest`_ modules. All tests can be run using the ``ttasks.py`` script::

    python ttasks.py test

Note that while doc tests are used, this is mostly just to make sure the documentation examples are valid. The true behavior of the library and its public contract are enforced through the unit tests.

Cross-Python version testing is achieved through `tox`_. To run changes against the reference and style tests, simply invoke ``tox`` from the top-level directory of the project; tox will run the unit tests against the compatible CPython runtimes. Additionally, the source is run through the `Flake8`_ linter. Whenever new code is pushed to the repo, this same set of `tox`_ tests is run on `AppVeyor`_ (for Windows builds). A separate configuration is used for `Travis CI`_, which tests on Linux.


Coding Style
------------

tt aims to be strictly `PEP8`_ compliant, enforcing this compliance via `Flake8`_. This project also includes an `editorconfig`_ file to help with formatting issues.


Documentation
-------------

To build the docs from source, run the following::

    python ttasks.py build-docs

If you're going to be working for a little bit, it's usually more convenient to boot up a live-reload server that will re-build the docs on any source file changes. To run one on port 5000 of your machine, run::

    python ttasks.py serve-docs


Building C-extensions
---------------------

tt contains some C-extensions that need to be built before the library is fully usable. They can be built in a development environment by running::

    python setup.py develop

from the project's top-level directory. There are some dependencies required for compiling these extensions. Let's start with what to do on Windows. You will need to install several different compilers:

    * `Microsoft Visual C++ 9.0`_ (for Python 2.7)
    * `Microsoft Visual C++ 10.0`_ (for Python 3.3 and 3.4)
    * `Microsoft Visual C++ 14.0`_ (for Python 3.5 and 3.6)

For reference, check out this `comprehensive list of Windows compilers`_ necessary for building Python and C-extensions. You may have some trouble installing the 7.1 SDK (which contains Visual C++ 10.0). `This stackoverflow answer`_ provides some possible solutions.

Releases
--------

Work for each release is done in a branch off of develop following the naming convention v{major}.{minor}.{micro}. When work for a version is complete, its branch is merged back into develop, which is subsequently merged into master. The master branch is then tagged with the release version number, following the scheme {major}.{minor}.{micro}.

After these steps, make sure you update the release notes, publish on Read the Docs, and publish on PyPI.


.. _unittest: https://docs.python.org/3/library/unittest.html
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _tox: https://tox.readthedocs.org/en/latest/
.. _Travis CI: https://travis-ci.org/welchbj/tt/
.. _AppVeyor: https://ci.appveyor.com/project/welchbj/tt
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Flake8: http://flake8.pycqa.org/en/latest/
.. _editorconfig: http://editorconfig.org/
.. _Microsoft Visual C++ 9.0: http://aka.ms/vcpython27
.. _Microsoft Visual C++ 10.0: http://www.microsoft.com/download/details.aspx?id=8279
.. _Microsoft Visual C++ 14.0: https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017
.. _comprehensive list of Windows compilers: https://wiki.python.org/moin/WindowsCompilers
.. _This stackoverflow answer: http://stackoverflow.com/a/32534158/2225145
