==========
User Guide
==========

The below code samples should give you an idea of how to use the tools provided in this library. If anything remains unclear, please feel free to open an `issue on GitHub`_ or reach out to :doc:`the author </author>`.

Expression basics
-----------------

The top-level class for interacting with boolean expressions in tt is, fittingly named, :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`. Let's start by importing it::

    >>> from tt import BooleanExpression

This class accepts boolean expressions as strings and provides the interface for parsing and tokenizing string expressions into a sequence of tokens and symbols, as we see here::

    >>> b = BooleanExpression('(A nand B) or (C and D)')
    >>> b.tokens
    ['(', 'A', 'nand', 'B', ')', 'or', '(', 'C', 'and', 'D', ')']
    >>> b.symbols
    ['A', 'B', 'C', 'D']

During initialization, the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` also does some work behind the scenes to build a basic understanding of the expression's structure. It re-orders the tokens into postfix order, and uses this representation to build a :class:`BooleanExpressionTree <tt.trees.expr_tree.BooleanExpressionTree>`. We can see this with::

    >>> b.postfix_tokens
    ['A', 'B', 'nand', 'C', 'D', 'and', 'or']
    >>> print(b.tree)
    or
    `----nand
    |    `----A
    |    `----B
    `----and
         `----C
         `----D

Under the hood, this expression tree is used for evaluation of the expression. The expression object provides an interface to this evaluation functionality; use it like this::

    >>> b.evaluate(A=True, B=False, C=True, D=False)
    True
    >>> b.evaluate(A=1, B=0, C=1, D=0)
    True

Notice that we can use ``0`` or ``False`` to represent low values and ``1`` or ``True`` to represent high values. tt makes sure that only valid Boolean-esque values are accepted for evaluation. For example, if we tried something like::

    >>> b.evaluate(A=1, B='not a Boolean value', C=0, D=0)
    Traceback (most recent call last):
        ...
    tt.errors.evaluation.InvalidBooleanValueError: "not a Boolean value" passed as value for "B" is not a valid Boolean value

or if we didn't include a value for each of the symbols::

    >>> b.evaluate(A=1, B=0, C=0)
    Traceback (most recent call last):
        ...
    tt.errors.symbols.MissingSymbolError: Did not receive value for the following symbols: "D"

we see that we get an exception. This brings up one of the key design philosophies of tt: exceptions are specific and abundant. This library does its best to make sure you use its top-level interfaces as designed, and will raise exceptions if something isn't right.

Exceptions in tt are organized in a hierarchy, with each category of exceptions grouped under a base exception type. For example, a common group of exceptions you'll deal with if you might handle malformed expressions is  :exc:`GrammarError <tt.errors.grammar.GrammarError>`. :exc:`GrammarError <tt.errors.grammar.GrammarError>` is a unique type of exception in tt, as it provides attributes for accessing the specific position in the expression string that caused an error. This is best illustrated with an example::

    >>> from tt import GrammarError
    >>> try:
    ...     b = BooleanExpression('A or or B')
    ... except GrammarError as e:
    ...     print("Here's what happened:")
    ...     print(e.message)
    ...     print("Here's where it happened:")
    ...     print(e.expr_str)
    ...     print(' '*e.error_pos + '^')
    ...
    Here's what happened:
    Unexpected binary operator "or"
    Here's where it happened:
    A or or B
         ^

Table basics
------------

Now that we've gotten the basic idea of how expressions work, we can use them to fill some truth tables. Surprisingly, the top-level class for dealing with truth tables in tt is called :class:`TruthTable <tt.tables.truth_table.TruthTable>`. Let's begin by importing it::

    >>> from tt import TruthTable

There are a few ways we can fill up a truth table in tt. One of them is to pass in an expression, either as an already-created :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` object or a string::

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

As we saw in the above example, printing tables produces a nicely-formatted text table. While we have stuck to simple variable names (``A``, ``B``, ``C``, etc.) so far, these tables will scale to fit the size of the symbol names::

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

These tables are populated by evaluating the expression for each combination of input values. Let's say that you already have the values you want in your truth table and would rather skip over re-evaluating ; you'd populate your table like this::

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

Notice that populating tables like this allows for *don't cares* (indicating by ``x``) to be present in your table. Additionally, we can see that symbol names were automatically generated for us. That's nice sometimes, but what if we want to specify them ourselves? We return to the ``ordering`` keyword argument::

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

So far, we've only been able to examine the results stored in our tables by printing them. This is nice for looking at an end result, but we need programmatic methods of accessing the values in our tables, like these::

    >>> t = TruthTable('!A && B')
    >>> t.results
    [False, True, False, False]
    >>> for inputs, result in t:
    ...     inputs, result
    ...
    ((False, False), False)
    ((False, True), True)
    ((True, False), False)
    ((True, True), False)
    >>> t[0], t[1], t[2], t[3]
    (False, True, False, False)

Accessing results by index is also an intuitive time to use binary literal values::

    >>> t[0b00], t[0b01], t[0b10], t[0b11]
    (False, True, False, False)

Up to this point, we've only taken a look at tables with all their results filled in, but we don't have to completely fill up our tables to start working with them. Here's an example of iteratively filling a table::

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

Another neat feature provided by tt's tables is the checking of logical equivalence::

    >>> t1 = TruthTable('A xor B')
    >>> t2 = TruthTable(from_values='0110')
    >>> t1.equivalent_to(t2)
    True
    >>> t1.equivalent_to('C xor D')
    True

Note that this equivalence comparison looks only at the result values of the tables and doesn't look at the symbols of either table.

Next, let's examine how *don't cares* function within tt's concept of logical equivalence. *Don't cares* in the calling table will be considered to equal to any value in the comparison table, but any explicity value in the calling table must be matched in the comparison table to be considered equal.

In this sense, a fully-specified table (i.e., one without any *don't cares*) will never be logically equivalent to one which contains *don't cares*, but the converse may be true. Let's see an example::

    >>> t1 = TruthTable('C nand D')
    >>> t2 = TruthTable(from_values='xx10')
    >>> t1.equivalent_to(t2)
    False
    >>> t2.equivalent_to(t1)
    True


.. _issue on GitHub: https://github.com/welchbj/tt/issues/new
