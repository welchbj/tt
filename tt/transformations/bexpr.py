"""Transformation functions for expressions."""

from tt.expressions import BooleanExpression

from tt.transformations.utils import ensure_bexpr


def apply_de_morgans(expr):
    """Convert an expression to a form with De Morgan's Law applied.

    :returns: A new expression object, transformed so that De Morgan's Law has
        been applied to negated *ANDs* and *ORs*.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a couple of simple examples showing De Morgan's Law being applied
    to a negated AND and a negated OR::

        >>> from tt import apply_de_morgans
        >>> apply_de_morgans('~(A /\\ B)')
        <BooleanExpression "~A \\/ ~B">
        >>> apply_de_morgans('~(A \\/ B)')
        <BooleanExpression "~A /\\ ~B">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.apply_de_morgans())


def apply_identity_law(expr):
    """Convert an expression to a form with the Identity Law applied.

    It should be noted that this transformation will also annihilate terms
    when possible. One such case where this would be applicable is the
    expression ``A and 0``, which would be transformed to the constant value
    ``0``.

    :returns: A new expression object, transformed so that the Identity Law
        has been applied to applicable *ANDs* and *ORs*.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here are a few simple examples showing the behavior of this transformation
    across all two-operand scenarios::

        >>> from tt import apply_identity_law
        >>> apply_identity_law('A and 1')
        <BooleanExpression "A">
        >>> apply_identity_law('A and 0')
        <BooleanExpression "0">
        >>> apply_identity_law('A or 0')
        <BooleanExpression "A">
        >>> apply_identity_law('A or 1')
        <BooleanExpression "1">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.apply_identity_law())


def apply_idempotent_law(expr):
    """Convert an expression to a form with the Idempotent Law applied.

    :returns: A new expression object, transformed so that the Idempotent Law
        has been applied to applicable clauses.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid data type.

    This transformation will apply the Idempotent Law to clauses of *AND* and
    *OR* operators containing redundant operands. Here are a couple of simple
    examples::

        >>> from tt import apply_idempotent_law
        >>> apply_idempotent_law('A and A')
        <BooleanExpression "A">
        >>> apply_idempotent_law('B or B')
        <BooleanExpression "B">

    This transformation will consider similarly-negated operands to be
    redundant; for example::

        >>> from tt import apply_idempotent_law
        >>> apply_idempotent_law('~A and ~~~A')
        <BooleanExpression "~A">
        >>> apply_idempotent_law('B or ~B or ~~B or ~~~B or ~~~~B or ~~~~~B')
        <BooleanExpression "B or ~B">

    Let's also take a quick look at this transformation's ability to prune
    redundant operands from CNF and DNF clauses::

        >>> from tt import apply_idempotent_law
        >>> apply_idempotent_law('(A and B and C and C and B) or (A and A)')
        <BooleanExpression "(A and B and C) or A">

    Of important note is that this transformation will not recursively apply
    the Idempotent Law to operands that bubble up. Here's an example
    illustrating this case::

        >>> from tt import apply_idempotent_law
        >>> apply_idempotent_law('(A or A) and (A or A)')
        <BooleanExpression "A and A">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.apply_idempotent_law())


def apply_inverse_law(expr):
    """Convert an expression to a form with the Inverse Law applied.

    :returns: A new expression object, transformed so that the Inverse Law
        has been applied to applicable *ANDs* and *ORs*.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    This transformation will apply the Identity Law to simple binary
    expressions consisting of negated and non-negated forms of the same
    operand. Let's take a look::

        >>> from tt.transformations import apply_inverse_law
        >>> apply_inverse_law('A and ~A')
        <BooleanExpression "0">
        >>> apply_inverse_law('A or B or ~B or C')
        <BooleanExpression "1">

    This transformation will also apply the behavior expected of the Inverse
    Law when negated and non-negated forms of the same operand appear in the
    same CNF or DNF clause in an expression::

        >>> from tt.transformations import apply_inverse_law
        >>> apply_inverse_law('(A or B or ~A) -> (C and ~C)')
        <BooleanExpression "1 -> 0">
        >>> apply_inverse_law('(A or !!!A) xor (not C or not not C)')
        <BooleanExpression "1 xor 1">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.apply_inverse_law())


def coalesce_negations(expr):
    """Convert an expression to a form with all negations condensed.

    :returns: A new expression object, transformed so that all "runs" of
        logical *NOTs* are condensed into the minimal equivalent number.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple example showing the basic premise of this transformation::

        >>> from tt import coalesce_negations
        >>> coalesce_negations('~~A or ~B or ~~~C or ~~~~D')
        <BooleanExpression "A or ~B or ~C or D">

    This transformation works on more complex expressions, too::

        >>> coalesce_negations('!!(A -> not not B) or ~(~(A xor B))')
        <BooleanExpression "(A -> B) or (A xor B)">

    It should be noted that this transformation will also apply negations
    to constant operands, as well. The behavior for this functionality is as
    follows::

        >>> coalesce_negations('~0')
        <BooleanExpression "1">
        >>> coalesce_negations('~1')
        <BooleanExpression "0">
        >>> coalesce_negations('~~~0 -> ~1 -> not 1')
        <BooleanExpression "1 -> 0 -> 0">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.coalesce_negations())


def distribute_ands(expr):
    """Convert an expression to distribute ANDs over ORed clauses.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to distribute ANDs over ORed
        clauses.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a couple of simple examples::

        >>> from tt import distribute_ands
        >>> distribute_ands('A and (B or C or D)')
        <BooleanExpression "(A and B) or (A and C) or (A and D)">
        >>> distribute_ands('(A or B) and C')
        <BooleanExpression "(A and C) or (B and C)">

    And an example involving distributing a sub-expression::

        >>> distribute_ands('(A and B) and (C or D or E)')
        <BooleanExpression "(A and B and C) or (A and B and D) or \
(A and B and E)">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.distribute_ands())


def distribute_ors(expr):
    """Convert an expression to distribute ORs over ANDed clauses.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to distribute ORs over ANDed
        clauses.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a couple of simple examples::

        >>> from tt import distribute_ors
        >>> distribute_ors('A or (B and C and D and E)')
        <BooleanExpression "(A or B) and (A or C) and (A or D) and (A or E)">
        >>> distribute_ors('(A and B) or C')
        <BooleanExpression "(A or C) and (B or C)">

    And an example involving distributing a sub-expression::

        >>> distribute_ors('(A or B) or (C and D)')
        <BooleanExpression "(A or B or C) and (A or B or D)">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.distribute_ors())


def to_cnf(expr):
    """Convert an expression to conjunctive normal form (CNF).

    This transformation only guarantees to produce an equivalent form of the
    passed expression in conjunctive normal form; the transformed expression
    may be an inefficent representation of the passed expression.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to be in CNF.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here are a few examples::

        >>> from tt import to_cnf
        >>> b = to_cnf('(A nor B) impl C')
        >>> b
        <BooleanExpression "A or B or C">
        >>> b.is_cnf
        True
        >>> b = to_cnf(r'~(~(A /\\ B) /\\ C /\\ D)')
        >>> b
        <BooleanExpression "(A \\/ ~C \\/ ~D) /\\ (B \\/ ~C \\/ ~D)">
        >>> b.is_cnf
        True

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.to_cnf())


def to_primitives(expr):
    """Convert an expression to a form with only primitive operators.

    All operators will be transformed equivalent form composed only of the
    logical AND, OR,and NOT operators. Symbolic operators in the passed
    expression will remain symbolic in the transformed expression and the same
    applies for plain English operators.

    :param expr: The expression to transform.
    :type expr: :class:`str <python:str>` or :class:`BooleanExpression \
    <tt.expressions.bexpr.BooleanExpression>`

    :returns: A new expression object, transformed to contain only primitive
        operators.
    :rtype: :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`

    :raises InvalidArgumentTypeError: If ``expr`` is not a valid type.

    Here's a simple transformation of exclusive-or::

        >>> from tt import to_primitives
        >>> to_primitives('A xor B')
        <BooleanExpression "(A and not B) or (not A and B)">

    And another example of if-and-only-if (using symbolic operators)::

        >>> to_primitives('A <-> B')
        <BooleanExpression "(A /\\ B) \\/ (~A /\\ ~B)">

    """
    bexpr = ensure_bexpr(expr)
    return BooleanExpression(bexpr.tree.to_primitives())
