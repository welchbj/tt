=============
Release Notes
=============

Check below for new features added in each release. Please note that release notes were not recorded before version 0.5.0.

0.5.x
-----

Features in the 0.5.x series of releases were focused on expanding the top-level interfacing and imporving optimizations under the hood. See below for specific features and fixes.

0.5.1
`````
    * Add ``from_values`` option to the :class:`TruthTable <tt.tables.truth_table.TruthTable>` initializer, allowing for table creation directly from values
    * Add ability to store *don't cares* in a :class:`TruthTable <tt.tables.truth_table.TruthTable>`
    * Add :func:`equivalent_to <tt.tables.truth_table.TruthTable.equivalent_to>` method to :class:`TruthTable <tt.tables.truth_table.TruthTable>` to check for equivalence of sources of truth
    * Convert :func:`generate_symbols <tt.tables.truth_table.TruthTable.generate_symbols>` and :func:`input_combos <tt.tables.truth_table.TruthTable.input_combos>` to be static methods of the :class:`TruthTable <tt.tables.truth_table.TruthTable>` class
    * Add :data:`is_full <tt.tables.truth_table.TruthTable.is_full>` to :class:`TruthTable <tt.tables.truth_table.TruthTable>`
    * Add __iter__ and __getitem__ functionality to :class:`TruthTable <tt.tables.truth_table.TruthTable>`
    * Add nice-looking __str__ to :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`
    * Add new exception types: :exc:`AlreadyFullTableError <tt.errors.state.AlreadyFullTableError>`, :exc:`ConflictingArgumentsError <tt.errors.arguments.ConflictingArgumentsError>`, and :exc:`RequiredArgumentError <tt.errors.arguments.RequiredArgumentError>`
    * Re-organize exception hierarchy so each group of exceptions extends from the same base class
    * Re-organize the test file structure into more-focused files
    * Add :doc:`User Guide </user_guide>`, acting as tutorial-style documentation
    * Remove CLI example from the README
    * Update documentation color palette

0.5.0
`````
    * Added the Release Notes section to the project's documentation (how fitting for this page)
    * Publically exposed the :func:`input_combos <tt.tables.truth_table.TruthTable.input_combos>` method in the :class:`TruthTable <tt.tables.truth_table.TruthTable>` class
    * Added test coverage for the CPython 3.6, PyPy, and PyPy3 runtimes
    * Migrated all documentation to from `Napoleon`_ docstrings to standard `Sphinx`_ docstrings
    * Added `doctest`_ tests to the documentation
    * Added type-checking to the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` class's initialization
    * Fixed a bug in the handling of empty expressions in the CLI

pre-0.5
-------

Unfortunatley, release notes were not kept before the 0.5.0 release.


.. _doctest: https://docs.python.org/3/library/doctest.html
.. _Napoleon: http://www.sphinx-doc.org/en/stable/ext/napoleon.html
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
