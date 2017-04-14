============
Table basics
============

Truth tables are a nice way of showing the behavior of an expression for each permutation of possible inputs and are nice tool to pair with expressions. Let's examine the interface provided by tt for working with truth tables.


Creating a table object from an expression
``````````````````````````````````````````

Surprisingly, the top-level class for dealing with truth tables in tt is called :class:`TruthTable <tt.tables.truth_table.TruthTable>`. Let's begin by importing it::

    >>> from tt import TruthTable

There are a few ways we can fill up a truth table in tt. One of them is to pass in an expression, either as an already-created :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` object or as a string::

    >>> t = TruthTable('A xor B')
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 1 |
    +---+---+---+
    | 1 | 0 | 1 |
    +---+---+---+
    | 1 | 1 | 0 |
    +---+---+---+

As we we in the above example, printing tables produces a nicely-formatted text table. Tables will scale to fit the size of the symbol names, too::

    >>> t = TruthTable('operand_1 and operand_2')
    >>> print(t)
    +-----------+-----------+---+
    | operand_1 | operand_2 |   |
    +-----------+-----------+---+
    |     0     |     0     | 0 |
    +-----------+-----------+---+
    |     0     |     1     | 0 |
    +-----------+-----------+---+
    |     1     |     0     | 0 |
    +-----------+-----------+---+
    |     1     |     1     | 1 |
    +-----------+-----------+---+

By default, tt will order the symbols in the top row of of the table to match the order of their appearance in the original expression; however, you can impose your own order, too::

    >>> t = TruthTable('A xor B', ordering=['B', 'A'])
    >>> print(t)
    +---+---+---+
    | B | A |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 1 |
    +---+---+---+
    | 1 | 0 | 1 |
    +---+---+---+
    | 1 | 1 | 0 |
    +---+---+---+


Creating a table object from values
```````````````````````````````````

The tables we looked at above were populated by evaluating the expression for each combination of input values, but let's say that you already have the values you want in your truth table. You'd populate your table like this::

    >>> t = TruthTable(from_values='00x1')
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 0 |
    +---+---+---+
    | 0 | 1 | 0 |
    +---+---+---+
    | 1 | 0 | x |
    +---+---+---+
    | 1 | 1 | 1 |
    +---+---+---+

Notice that populating tables like this allows for *don't cares* (indicated by ``'x'``) to be present in your table. Additionally, we can see that symbol names were automatically generated for us. That's nice sometimes, but what if we want to specify them ourselves? We return to the ``ordering`` keyword argument::

    >>> t = TruthTable(from_values='1x01', ordering=['op1', 'op2'])
    >>> print(t)
    +-----+-----+---+
    | op1 | op2 |   |
    +-----+-----+---+
    |  0  |  0  | 1 |
    +-----+-----+---+
    |  0  |  1  | x |
    +-----+-----+---+
    |  1  |  0  | 0 |
    +-----+-----+---+
    |  1  |  1  | 1 |
    +-----+-----+---+


Accessing values from a table
`````````````````````````````

So far, we've only been able to examine the results stored in our tables by printing them. This is nice for looking at an end result, but we need programmatic methods of accessing the values in our tables. There's a few ways to do this in tt; one such example is the :data:`results <tt.tables.truth_table.TruthTable.results>` attribute present on :class:`TruthTable <tt.tables.truth_table.TruthTable>` objects, which stores all results in the table::

    >>> t = TruthTable('!A && B')
    >>> t.results
    [False, True, False, False]

Results in the table are also available by indexing the table::

    >>> t[0], t[1], t[2], t[3]
    (False, True, False, False)

Accessing results by index is also an intuitive time to use binary literals::

    >>> t[0b00], t[0b01], t[0b10], t[0b11]
    (False, True, False, False)

Tables in tt are also iterable. There are a couple of important items to note. First, iterating through the entries in a table will skip over the entries that would have appeared as ``None`` in the :data:`results <tt.tables.truth_table.TruthTable.results>` list. Second, in addition to the result, each iteration through the table yields a :func:`namedtuple <python:collections.namedtuple>`-like object representing the inputs associated with that result. Let's take a look::

    >>> for inputs, result in t:
    ...     inputs.A, inputs.B
    ...     str(inputs), result
    ...
    (False, False)
    ('A=0, B=0', False)
    (False, True)
    ('A=0, B=1', True)
    (True, False)
    ('A=1, B=0', False)
    (True, True)
    ('A=1, B=1', False)


Partially filling tables
````````````````````````

Up to this point, we've only taken a look at tables with all of their results filled in, but we don't have to completely fill up our tables to start working with them. Here's an example of iteratively filling a table::

    >>> t = TruthTable('A nor B', fill_all=False)
    >>> t.is_full
    False
    >>> print(t)
    Empty!
    >>> t.fill(A=0)
    >>> t.is_full
    False
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 1 |
    +---+---+---+
    | 0 | 1 | 0 |
    +---+---+---+
    >>> t.fill()
    >>> t.is_full
    True
    >>> print(t)
    +---+---+---+
    | A | B |   |
    +---+---+---+
    | 0 | 0 | 1 |
    +---+---+---+
    | 0 | 1 | 0 |
    +---+---+---+
    | 1 | 0 | 0 |
    +---+---+---+
    | 1 | 1 | 0 |
    +---+---+---+

Empty slots in the table will be represented with a corresponding ``None`` entry for their result::

    >>> t = TruthTable('A or B', fill_all=False)
    >>> t.results
    [None, None, None, None]
    >>> t.fill(B=0)
    >>> t.results
    [False, None, True, None]

Make sure not to try to keep filling an already-full table, though::

    >>> t = TruthTable(from_values='0110')
    >>> t.is_full
    True
    >>> t.fill()
    Traceback (most recent call last):
        ...
    tt.errors.state.AlreadyFullTableError: Cannot fill an already-full table


Logical equivalence
```````````````````

Another neat feature provided by tt's tables is the checking of logical equivalence::

    >>> t1 = TruthTable('A xor B')
    >>> t2 = TruthTable(from_values='0110')
    >>> t1.equivalent_to(t2)
    True
    >>> t1.equivalent_to('C xor D')
    True

Note that this equivalence comparison looks only at the result values of the tables and doesn't examine at the symbols of either table.

Next, let's examine how *don't cares* function within tt's concept of logical equivalence. *Don't cares* in the calling table will be considered to equal to any value in the comparison table, but any explicity value in the calling table must be matched in the comparison table to be considered equal.

In this sense, a fully-specified table (i.e., one without any *don't cares*) will never be logically equivalent to one which contains *don't cares*, but the converse may be true. Let's see an example::

    >>> t1 = TruthTable('C nand D')
    >>> t2 = TruthTable(from_values='xx10')
    >>> t1.equivalent_to(t2)
    False
    >>> t2.equivalent_to(t1)
    True
