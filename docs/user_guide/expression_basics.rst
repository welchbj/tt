=================
Expression basics
=================

At tt's core is the concept of the Boolean expression, encapsulated in this library with the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` class. Let's take look at what we can do with expressions.


Creating an expression object
`````````````````````````````

The top-level class for interacting with boolean expressions in tt is, fittingly named, :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`. Let's start by importing it::

    >>> from tt import BooleanExpression

This class accepts boolean expressions as strings and provides the interface for parsing and tokenizing string expressions into a sequence of tokens and symbols, as we see here::

    >>> b = BooleanExpression('(A nand B) or (C and D)')
    >>> b.tokens
    ['(', 'A', 'nand', 'B', ')', 'or', '(', 'C', 'and', 'D', ')']
    >>> b.symbols
    ['A', 'B', 'C', 'D']

We can also always retrieve the original string we passed in via the ``raw_expr`` attribute::

    >>> b.raw_expr
    '(A nand B) or (C and D)'

During initialization, the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` also does some work behind the scenes to build a basic understanding of the expression's structure. It re-orders the tokens into postfix order, and uses this representation to build a :class:`ExpressionTreeNode <tt.trees.tree_node.ExpressionTreeNode>`. We can see this with::

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

This expression tree represents tt's understanding of the structure of your expression. If you are receiving an unexpected error for a more complicated expression, inspecting the ``tree`` attribute on the :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` instance can be a good starting point for debugging the issue.


Evaluating expressions
``````````````````````

Looking at expression symbols and tokens is nice, but we need some real functionality for our expressions; a natural starting point is the ability to evaluate expressions. A :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` object provides an interface to this evaluation functionality; use it like this::

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

These exceptions can be nice if you aren't sure about your input, but if you think this safety is just adding overhead for you, there's a way to skip those extra checks::

    >>> b.evaluate_unchecked(A=0, B=0, C=1, D=0)
    True


Handling malformed expressions
``````````````````````````````

So far, we've only seen one example of a :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` instance, and we passed a valid expression string to it. What happens when we pass in a malformed expression? And what does tt even consider to be a malformed expression?

While there is no explicit grammar for expressions in tt, using your best judgement will work most of the time. Most well-known Boolean expression operators are available in plain-English and symbolic form. You can see the list of available operators like so::

    >>> from tt import OPERATOR_MAPPING
    >>> print(', '.join(sorted(OPERATOR_MAPPING.keys())))
    !, &, &&, ->, /\, <->, AND, IFF, IMPL, NAND, NOR, NOT, NXOR, OR, XNOR, XOR, \/, and, iff, impl, nand, nor, not, nxor, or, xnor, xor, |, ||, ~

Another possible source of errors in your expressions will be invalid symbol names. Due to some functionality based on accessing symbol names from :func:`namedtuple <python:collections.namedtuple>`-like objects, symbol names must meet the following criteria:

    1. Must be a valid `Python identifiers`_.
    2. Cannot be a `Python keyword`_.
    3. Cannot begin with an underscore

An exception will be raised if a symbol name in your expression does not meet the above criteria. Fortunately, tt provides a way for us to check if our symbols are valid. Let's take a look::

    >>> from tt import is_valid_identifier
    >>> is_valid_identifier('False')
    False
    >>> is_valid_identifier('_bad')
    False
    >>> is_valid_identifier('not$good')
    False
    >>> is_valid_identifier('a_good_symbol_name')
    True
    >>> b = BooleanExpression('_A or B')
    Traceback (most recent call last):
        ...
    tt.errors.grammar.InvalidIdentifierError: Invalid operand name "_A"

As we saw in the above example, we caused an error from the ``tt.errors.grammar`` module. If you play around with invalid expressions, you'll notice that all of these errors come from that module; that's because errors in this logical group are all descendants of :exc:`GrammarError <tt.errors.grammar.GrammarError>`. This is the type of error that lexical expression errors will fall under::

    >>> from tt import GrammarError
    >>> invalid_expressions = ['A xor or B', 'A or ((B nand C)', 'A or B B']
    >>> for expr in invalid_expressions:
    ...     try:
    ...             b = BooleanExpression(expr)
    ...     except Exception as e:
    ...             print(type(e))
    ...             print(isinstance(e, GrammarError))
    ...
    <class 'tt.errors.grammar.ExpressionOrderError'>
    True
    <class 'tt.errors.grammar.UnbalancedParenError'>
    True
    <class 'tt.errors.grammar.ExpressionOrderError'>
    True

:exc:`GrammarError <tt.errors.grammar.GrammarError>` is a unique type of exception in tt, as it provides attributes for accessing the specific position in the expression string that caused an error. This is best illustrated with an example::

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


.. _Python identifiers: https://docs.python.org/3/reference/lexical_analysis.html#identifiers
.. _Python keyword: https://docs.python.org/3/reference/lexical_analysis.html#keywords
