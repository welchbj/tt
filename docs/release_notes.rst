=============
Release Notes
=============

Check below for new features added in each release. Please note that release notes were not recorded before version 0.5.0.

0.5.0
-----

    * Added the Release Notes section to the project's documentation (how fitting for this page)
    * Publically exposed the :func:`input_combos <tt.tables.truth_table.TruthTable.input_combos>` method in the :class:`TruthTable <tt.tables.truth_table.TruthTable>` class
    * Added test coverage for the CPython 3.6, PyPy, and PyPy3 runtimes
    * Migrated all documentation to from `Napoleon`_ docstrings to standard `Sphinx`_ docstrings
    * Added `doctest`_ tests to the documentation
    * Added type-checking to the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` class's initialization
    * Fixed a bug in the handling of empty expressions in the CLI


.. _doctest: https://docs.python.org/3/library/doctest.html
.. _Napoleon: http://www.sphinx-doc.org/en/stable/ext/napoleon.html
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
