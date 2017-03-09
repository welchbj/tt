"""An expression tree implementation for Boolean expressions."""

from ..definitions import OPERATOR_MAPPING, TT_NOT_OP
from .tree_node import (BinaryOperatorExpressionTreeNode,
                        OperandExpressionTreeNode,
                        UnaryOperatorExpressionTreeNode)


class BooleanExpressionTree(object):

    """An expression tree for Boolean expressions.

    This class expects any input it receives to be well-formed; any tokenized
    lists you pass it directly (instead of from the attribute of the
    :class:`BooleanExpression <tt.expressions.bexpr.BooleanExpression>` class)
    will not be checked.

    """

    def __init__(self, postfix_tokens):
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
        """The root of the tree; this is ``None`` for an empty tree.

        :type: :class:`ExpressionTreeNode\
                       <tt.trees.tree_node.ExpressionTreeNode>`

        """
        return self._root

    def evaluate(self, input_dict):
        """Evaluate the expression held in this tree for specified inputs.

        :param input_dict: A dict mapping string variable names to the values
            for which they should be evaluated.
        :type input_dict: Dict{:class:`str <python:str>`: truthy}

        :returns: The result of the expression tree evaluation.
        :rtype: :class:`bool <python:bool>`

        .. note::

            This function does not check to ensure the validity of the
            ``input_dict`` argument in any way.

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
        if not self.postfix_tokens:
            self._root = None
            return

        stack = []
        operators = OPERATOR_MAPPING.keys()

        for token in self.postfix_tokens:
            if token in operators:
                if OPERATOR_MAPPING[token] == TT_NOT_OP:
                    node = UnaryOperatorExpressionTreeNode(
                        token, stack.pop())
                else:
                    node = BinaryOperatorExpressionTreeNode(
                        token, stack.pop(), stack.pop())
            else:
                node = OperandExpressionTreeNode(token)

            stack.append(node)

        self._root = stack.pop()

    def __str__(self):
        if self._root is None:
            return 'Empty!'
        else:
            return str(self._root)[:-1]
