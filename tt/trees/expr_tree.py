"""An expression tree implementation for Boolean expressions."""

from ..errors import InvalidArgumentTypeError, InvalidArgumentValueError
from ..definitions import OPERATOR_MAPPING, TT_NOT_OP
from .tree_node import (BinaryOperatorExpressionTreeNode,
                        OperandExpressionTreeNode,
                        UnaryOperatorExpressionTreeNode)


class BooleanExpressionTree(object):

    """An expression tree for Boolean expressions.

    This class expects any input it receives to be well-formed; any tokenized
    lists you pass it directly (instead of from the attribute of the
    :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` class)
    will not be checked. Like expressions, expression trees cannot be empty.

    :param postfix_tokens: A list of tokens in postfix order, representing the
        structure of the tree; the validity/order of this list is not checked.
    :type postfix_tokens: List[:class:`str <python:str>`]

    :raises InvalidArgumentTypeError: If ``postfix_tokens`` is not a list or
        contains non-:class:`str <python:str>` elements.
    :raises InvalidArgumentValueError: If ``postfix_tokens`` is an empty list.

    Here's a look at the basic functionality::

        >>> from tt import BooleanExpressionTree
        >>> tree = BooleanExpressionTree(['A', 'B', 'or',
        ...                               'C', 'D', 'E', 'or', 'or',
        ...                               'and'])
        >>> print(tree)
        and
        `----or
        |    `----A
        |    `----B
        `----or
             `----C
             `----or
                  `----D
                  `----E
        >>> tree.is_cnf
        True

    When printing trees, it is important to note that the ordering of children
    will always be left and then right. Let's illustrate this by continuing our
    above example::

        >>> print(tree.root.l_child)
        or
        `----A
        `----B
        >>> print(tree.root.r_child)
        or
        `----C
        `----or
             `----D
             `----E

    """

    def __init__(self, postfix_tokens):

        if (not isinstance(postfix_tokens, list) or
                not all(isinstance(elt, str) for elt in postfix_tokens)):
            raise InvalidArgumentTypeError(
                'postfix_tokens must be a list of strings')

        if not len(postfix_tokens):
            raise InvalidArgumentValueError('postfix_tokens cannot be empty')

        self._postfix_tokens = postfix_tokens
        self._root = None
        self._build_tree()

    @property
    def postfix_tokens(self):
        """The tokens, in postfix order, from which this tree was built.

        :type: List[:class:`str <python:str>`]

        """
        return self._postfix_tokens

    @property
    def root(self):
        """The root of the tree.

        :type: :class:`ExpressionTreeNode\
                       <tt.trees.tree_node.ExpressionTreeNode>`

        """
        return self._root

    @property
    def is_cnf(self):
        """Whether this tree is in cnf form.

        :type: :class:`bool <python:bool>`

        Here are a few examples::

            >>> from tt import BooleanExpressionTree as bet
            >>> b = bet(['A', 'B', 'xor'])
            >>> print(b)
            xor
            `----A
            `----B
            >>> b.is_cnf
            False
            >>> b = bet(['A', 'B', 'or',
            ...          'C', 'B', 'E', 'or', 'or',
            ...          'D', 'A', 'C', 'or', 'or',
            ...          'and', 'and'])
            >>> print(b)
            and
            `----or
            |    `----A
            |    `----B
            `----and
                 `----or
                 |    `----C
                 |    `----or
                 |         `----B
                 |         `----E
                 `----or
                      `----D
                      `----or
                           `----A
                           `----C
            >>> b.is_cnf
            True

        """
        return self._root.is_cnf

    def evaluate(self, input_dict):
        """Evaluate the expression held in this tree for specified inputs.

        :param input_dict: A dict mapping string variable names to the values
            for which they should be evaluated. This variable is not check
            for validity in any way; you should perform validation before
            passing values here.
        :type input_dict: Dict{:class:`str <python:str>`: truthy}

        :returns: The result of the expression tree evaluation.
        :rtype: :class:`bool <python:bool>`

        While you would normally evaluate expressions through the interface
        provided by the :class:`BooleanExpression\
        <tt.expressions.bexpr.BooleanExpression>` class, this interface is
        still exposed for your use if you want to avoid any overhead introduced
        by the extra layer of abstraction. For example::

            >>> from tt import BooleanExpressionTree
            >>> bet = BooleanExpressionTree(['A', 'B', 'xor'])
            >>> bet.evaluate({'A': 1, 'B': 0})
            True
            >>> bet.evaluate({'A': 1, 'B': 1})
            False

        """
        return self._root.evaluate(input_dict)

    def _build_tree(self):
        """Iterate over the ``postfix_tokens``, constructing the tree.

        .. note::

            This method will populate this class's ``root`` attribute.

        """
        stack = []
        operators = OPERATOR_MAPPING.keys()

        for token in self.postfix_tokens:
            if token in operators:
                if OPERATOR_MAPPING[token] == TT_NOT_OP:
                    node = UnaryOperatorExpressionTreeNode(
                        token, stack.pop())
                else:
                    right, left = stack.pop(), stack.pop()
                    node = BinaryOperatorExpressionTreeNode(
                        token, left, right)
            else:
                node = OperandExpressionTreeNode(token)

            stack.append(node)

        self._root = stack.pop()

    def __str__(self):
        return str(self._root)
