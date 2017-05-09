=============
Release Notes
=============

Check below for new features added in each release. Please note that release notes were not recorded before version 0.5.0.

0.6.x
-----

Features in the 0.6.x series of releases are focused on expanding functionality to include expression optimization, satisfiability, and transformations.

0.6.1
`````

    * Add iff and implies Boolean operators
    * Add :data:`is_cnf <tt.expressions.bexpr.BooleanExpression.is_cnf>` attribute to :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

0.6.0
`````
    * Add :func:`is_valid_identifier <tt.definitions.operands.is_valid_identifier>` helper method for checking if symbol names are valid
    * Add checking of valid symbol names to :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` and :class:`TruthTable <tt.tables.truth_table.TruthTable>` initalization logic, with corresponding new exception type :exc:`InvalidIdentifierError <tt.errors.grammar.InvalidIdentifierError>`
    * Add :func:`boolean_variables_factory <tt.definitions.operands.boolean_variables_factory>` helper for generating more intuitive collections of symbol inputs
    * Update ``__iter__`` in  :class:`TruthTable <tt.tables.truth_table.TruthTable>` to yield inputs as a :func:`namedtuple <python:collections.namedtuple>`-like object rather than a plain :class:`tuple <python:tuple>`
    * Re-organize :doc:`User Guide </user_guide>` into different sections instead of one long page
    * Remove PyPy support, due to addition of C-extensions
    * Add OS X builds to Travis
    * Include both 32-bit and 64-bit builds on AppVeyor
    * Add initial wrapper around `PicoSAT`_ library for future satisfiability interface; namely, the :func:`sat_one <tt.satisfiability.picosat.sat_one>` method
    * Add automated deployment to PyPI on tagged commits from CI services

0.5.x
-----

Features in the 0.5.x series of releases were focused on expanding the top-level interface and improving optimizations under the hood. See below for specific features and fixes.

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
.. _PicoSAT: http://fmv.jku.at/picosat/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
