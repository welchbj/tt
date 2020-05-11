"""Utilities for building more complex transformations."""

import functools

from collections import deque

from tt.errors import (
    InvalidArgumentValueError,
    InvalidArgumentTypeError)
from tt.expressions import BooleanExpression


_DEFAULT_TIMES = 1


def ensure_bexpr(expr):
    """Return an expression object or raise an InvalidArgumentTypeError.

    :param expr: The expression whose type is being checked.
    :type expr: :class:`BooleanExpression <tt.expressions.bexpr.\
BooleanExpression>` or :class:`str <python:str>`

    :raises InvalidArgumentTypeError: If ``expr`` is not of a valid type.

    """
    if isinstance(expr, str):
        return BooleanExpression(expr)
    elif isinstance(expr, BooleanExpression):
        return expr
    else:
        raise InvalidArgumentTypeError(
            'Transformations accept either a string or BooleanExpression '
            'argument')


@functools.total_ordering
class RepeatableAction(object):

    """A mixin for describing actions that can be repeated.

    This class is meant to be used as a mixin when simple access to a ``times``
    attribute is needed, presumably to perform some action or task multiple
    times. Here's a simple look at the class::

        >>> from tt import RepeatableAction
        >>> r = RepeatableAction(5)
        >>> print(r)
        5 times
        >>> r
        <RepeatableAction [5 times]>
        >>> r.times
        5

    The passed ``times`` argument to this class must be a value that implements
    ``__lt__`` that is not less than 1. Here's an example::

        >>> r = RepeatableAction(-1)
        Traceback (most recent call last):
            ...
        tt.errors.arguments.InvalidArgumentValueError: `times` must be at \
least 1

    Instances of :class:`RepeatableAction` are immutable, hashable, and
    implement all rich comparison operators. Let's take a look::

        >>> r1, r2 = RepeatableAction(3), RepeatableAction(4)
        >>> hash(r1)
        3
        >>> hash(r2)
        4
        >>> r1 < r2
        True
        >>> r1 == r2
        False
        >>> r1 > r2
        False
        >>> r3 = RepeatableAction(4)
        >>> r2 == r3
        True

    :param times: The number of times that this action would be repeated when
        executed.
    :type times: Typically an :class:`int <python:int>`

    :raises InvalidArgumentValueError: If ``times`` is less than 1.

    """

    __slots__ = ('_times',)

    def __init__(self, times=_DEFAULT_TIMES):
        if times < 1:
            raise InvalidArgumentValueError('`times` must be at least 1')

        self._times = times

    @property
    def times(self):
        """The number of times the action is to be repeated.

        :type: :class:`int <python:int>`

        .. code-block:: python

            >>> from tt import RepeatableAction
            >>> r = RepeatableAction(3)
            >>> r.times
            3
            >>> r = RepeatableAction(float('inf'))
            >>> r.times
            inf

        """
        return self._times

    def __hash__(self):
        return hash(self._times)

    def __eq__(self, other):
        if isinstance(other, RepeatableAction):
            return self._times == other._times
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, RepeatableAction):
            return self._times < other._times
        else:
            return NotImplemented

    def __str__(self):
        return '{} time'.format(self._times) + (
               '' if self._times == 1 else 's')

    def __repr__(self):
        return '<RepeatableAction [{}]>'.format(str(self))


class ComposedTransformation(RepeatableAction):

    """An encapsulation of composed transformation functions.

    This class opens up a world of functionality consisting of buildable (i.e.,
    composed) transformation functions. While instances of this class will work
    when manually initialized by the user, it will likely be easier to compose
    functions using the :func:`tt_compose` method from this module.

    Transformation functions, held within the ``fn`` attribute of this class,
    are intended to be pure functions that both receive and produce an instance
    of :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>`.

    When called, instances of this class will repeatedly apply the ``fn``
    callable to the passed argument. The repeated application of the ``fn``
    callable will continue until either the specified number of ``times`` is
    met or the callable produces no change to the expression during the
    transformation.

    Let's take a look at a simple example, where all we do is compose two
    fairly basic transformations::

        >>> from tt import coalesce_negations, to_primitives, tt_compose
        >>> f = tt_compose(to_primitives, coalesce_negations)
        >>> f
        <ComposedTransformation [to_primitives -> coalesce_negations]>
        >>> to_primitives('~A <-> ~B')
        <BooleanExpression "(~A /\\ ~B) \\/ (~~A /\\ ~~B)">
        >>> f('~A <-> ~B')
        <BooleanExpression "(~A /\\ ~B) \\/ (A /\\ B)">

    This fairly simple example gives us an idea of how to compose functions
    using the :func:`tt_compose` helper. A few operators make manual
    composition of instances of this class a little more intuitive, too. Let's
    take a look at how we would make the same composition from above using the
    ``>>`` operator::

        >>> from tt import ComposedTransformation
        >>> one = ComposedTransformation(to_primitives)
        >>> two = ComposedTransformation(coalesce_negations)
        >>> one >> two
        <ComposedTransformation [to_primitives -> coalesce_negations]>

    The ``>>`` and ``<<`` operators shown above are just shallow wrappers
    around the core :func:`compose <tt.transformations.utils.\
ComposedTransformation.compose>` function.

    It is important to note that instances of this class are immutable and
    hashable; consequently, they support ``==`` and ``!=`` equality checks.
    We can see this by continuing our example from above::

        >>> three = ComposedTransformation(to_primitives)
        >>> one == two
        False
        >>> one == three
        True
        >>> two == three
        False

    The hash of instances of this class is computed at initialization and never
    updated, so meddling with ``ComposedTransformation`` instances will likely
    have unintended consequences for you.

    :param fn: The callable transformation function wrapped by this class.
    :type fn: :data:`Callable <python:typing.Callable>`

    :param next_transformation: The next transformation in the constructed
        composed sequence of transformation functions.
    :type next_transformation: :class:`ComposedTransformation`

    :param times: The number of times the wrapped function is to be repeatedly
        applied to its passed argument when called.
    :type times: Typically an :class:`int <python:int>`

    :raises InvalidArgumentTypeError: If the passed ``fn`` argument is not
        a callable.
    :raises InvalidArgumentValueError: If ``times`` is not valid, as per the
        :class:`RepeatableAction` initialization logic.

    """

    def __init__(self, fn, next_transformation=None, times=_DEFAULT_TIMES):
        RepeatableAction.__init__(self, times)

        if not callable(fn):
            raise InvalidArgumentTypeError('`fn` must be callable')

        if isinstance(next_transformation, ComposedTransformation):
            self._next_transformation = next_transformation
        elif next_transformation is None:
            self._next_transformation = None
        else:
            raise InvalidArgumentTypeError(
                '`next_transformation` must be of type '
                '`ComposedTransformation` when used')

        self._fn = fn
        self._fn_name = getattr(fn, '__name__', str(fn))
        self._computed_hash = hash(
            (self._fn, self._next_transformation, self.times))

    def __call__(self, expr):
        bexpr = ensure_bexpr(expr)
        prev_tree = bexpr.tree
        transformed_expr = None

        t = 0
        if hasattr(prev_tree, self._fn_name):
            next_tree = prev_tree
            while t < self._times:
                t += 1
                prev_tree = next_tree
                next_tree = getattr(next_tree, self._fn_name)()
                if next_tree == prev_tree:
                    break

            transformed_expr = BooleanExpression(next_tree)
        else:
            prev_expr = expr
            next_expr = prev_expr
            while t < self._times:
                t += 1
                prev_expr = next_expr
                next_expr = self._fn(next_expr)
                if next_expr == prev_expr:
                    break

            transformed_expr = next_expr

        if self._next_transformation is not None:
            return self._next_transformation(transformed_expr)
        else:
            return transformed_expr

    def __rshift__(self, other):
        return self.compose(other)

    def __lshift__(self, other):
        return other.compose(self)

    def __str__(self):
        ret = self._fn_name

        if self._times > 1:
            ret += ' ({})'.format(RepeatableAction.__str__(self))

        if self._next_transformation is not None:
            ret += ' -> '
            ret += str(self._next_transformation)

        return ret

    def __repr__(self):
        return '<ComposedTransformation [{}]>'.format(str(self))

    def __hash__(self):
        return self._computed_hash

    def __eq__(self, other):
        if isinstance(other, ComposedTransformation):
            return (self._fn == other._fn and
                    self._next_transformation == other._next_transformation and
                    self.times == other.times)
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def compose(self, other):
        """Compose this transformation with another.

        :param other: The callable transformation function, composed
            transformation object, or modifier object to either be composed
            with or modify this object.
        :type other: A :data:`Callable <python:typing.Callable>`, instance of
            :class:`ComposedTransformation`, or instance of
            :class:`AbstractTransformationModifier`.

        :returns: A new composed transformation instance, with the intended
            composition or modification applied.
        :rtype: :class:`ComposedTransformation`

        :raises InvalidArgumentType: If the ``other`` argument is not of an
            expected type.

        """
        if isinstance(other, ComposedTransformation):
            return ComposedTransformation(
                self._fn, next_transformation=other, times=self.times)
        elif callable(other):
            return ComposedTransformation(
                self._fn, next_transformation=ComposedTransformation(other))
        elif isinstance(other, AbstractTransformationModifier):
            return other.modify(self)
        else:
            raise InvalidArgumentTypeError(
                'compose() expects arguments to either be callable or to '
                'be of instance AbstractTransformationModifier')

    @property
    def fn(self):
        """The callable transformation function that this class wraps.

        This callable should both accept as an argument and produce as its
        result an instance of the :class:`BooleanExpression <tt.expressions.\
bexpr.BooleanExpression>` class.

        :type: :data:`Callable <python:typing.Callable>`

        .. code-block:: python

            >>> from tt import tt_compose, apply_de_morgans, twice
            >>> f = tt_compose(apply_de_morgans, twice)
            >>> f.fn.__name__
            'apply_de_morgans'

        """
        return self._fn

    @property
    def next_transformation(self):
        """The next transformation that this object's result will be passed to.

        The next transformation function in the chain of composed functions. A
        value of ``None`` indicates that this is the last function in the
        composition.

        :type: :class:`ComposedTransformation`

        """
        return self._next_transformation


class AbstractTransformationModifier(object):

    def modify(self, other):
        """Modify a transformation composition or other modifier.

        This method must be implemented by descendants of this class.

        :param other: A transformation composition or
        :type other: :class:`ComposedTransformation` or
            :class:`AbstractTransformationModifier`

        :returns: A modified composition or modifier.
        :rtype: The same type as ``other``

        """
        raise NotImplementedError(
            'Descendants of AbstractTransformationModifier must implement '
            '`modify()`')


class repeat(AbstractTransformationModifier, RepeatableAction):

    """Factory for a repeating transformation modifier.

    This factory method is largely meant to provide repeating modifier for the
    :func:`tt_compose` function. As an example, let's compose a transformation
    that will be applied 7 times to expressions passed to it::

        >>> from tt import tt_compose, coalesce_negations, repeat
        >>> tt_compose(coalesce_negations, repeat(7))
        <ComposedTransformation [coalesce_negations (7 times)]>

    Check out the :data:`twice` and :data:`forever` modifiers for some pre-made
    utilities that may come in handy.

    """

    def __init__(self, times):
        AbstractTransformationModifier.__init__(self)
        RepeatableAction.__init__(self, times)

    def modify(self, other):
        if isinstance(other, ComposedTransformation):
            modified_times = other.times * self._times
            return ComposedTransformation(
                other.fn, next_transformation=other.next_transformation,
                times=modified_times)
        else:
            raise InvalidArgumentTypeError(
                'modify() expects `other` to be of type '
                '`ComposedTransformation`')


twice = repeat(2)
"""A repeating modifier to perform a transformation twice.

:type: :class:`repeat`

"""


forever = repeat(float('inf'))
"""A repeating modifier to perform a transformation forever.

:type: :class:`repeat`

"""


def tt_compose(*fns):
    """Compose multiple transformations into a new callable transformation.

    This function will compose multiple transformations and transformation
    modifiers into a single callable. When called, this new transformation will
    apply the composition to generate a transformed expression.

    :param fns: A sequence of callable transformation functions or
        transformation modifiers from which a single composed transformation
        will be constructed.
    :type fns: :data:`Callable <python:typing.Callable>`,
               :class:`ComposedTransformation`, or
               :class:`AbstractTransformationModifier`

    :returns: The callable composition of all functions in ``fn``, which will
        return a :class:`BooleanExpression <tt.expressions.bexpr.\
BooleanExpression>` object when called.
    :rtype: :data:`Callable <python:typing.Callable>`

    :raises InvalidArgumentTypeError: If a modifier is ordered incorrectly or
        a non-callable function is included in the sequence.
    :raises InvalidArgumentValueError: If an insufficient number of arguments
        is provided (must be at least 2).

    Let's say we wanted a transformation that would first convert all operators
    in our expression to their equivalent primitive form, and then apply De
    Morgan's Law twice::

        >>> from tt.transformations import *
        >>> f = tt_compose(
        ...     to_primitives,
        ...     apply_de_morgans, twice
        ... )
        >>> f
        <ComposedTransformation [to_primitives -> apply_de_morgans (2 times)]>
        >>> f('~A <-> ~B')
        <BooleanExpression "(~A /\\ ~B) \\/ (~~A /\\ ~~B)">

    Composed transformations can be nested, too. Let's add some functionality
    to our composed transformation so that all redundant negations are
    coalesced::

        >>> g = tt_compose(f, coalesce_negations)
        >>> g
        <ComposedTransformation [to_primitives -> apply_de_morgans (2 times)\
 -> coalesce_negations]>
        >>> g('~A <-> ~B')
        <BooleanExpression "(~A /\\ ~B) \\/ (A /\\ B)">

    """
    if len(fns) < 2:
        raise InvalidArgumentValueError(
            '`tt_compose()` expects at least two arguments')

    first_fn = fns[0]
    if isinstance(first_fn, AbstractTransformationModifier):
        raise InvalidArgumentTypeError(
            '`tt_compose()` sequence cannot begin with a composition modifier')
    elif not callable(first_fn):
        raise InvalidArgumentTypeError(
            '`tt_compose()` sequence must begin with a callable '
            'transformation function or composition')

    modified_compositions = deque()
    curr_composition = ComposedTransformation(first_fn)

    for fn in fns[1:]:
        if isinstance(fn, AbstractTransformationModifier):
            curr_composition = fn.modify(curr_composition)
        elif callable(fn):
            modified_compositions.append(curr_composition)
            curr_composition = ComposedTransformation(fn)
        else:
            raise InvalidArgumentTypeError(
                '`tt_compose()` sequence must consist solely of callable '
                'transformation functions and transformation modifiers')

    modified_compositions.append(curr_composition)

    # compose into a single transformation
    composition = modified_compositions.pop()
    while modified_compositions:
        composition = modified_compositions.pop().compose(composition)

    return composition
