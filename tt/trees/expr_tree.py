"""An expression tree implementation for Boolean expressions."""

from ..operators import OPERATOR_MAPPING, TT_NOT_OP
from .tree_node import (BinaryOperatorExpressionTreeNode,
                        OperandExpressionTreeNode,
                        UnaryOperatorExpressionTreeNode)


class BooleanExpressionTree(object):

    """An expression tree for Boolean expressions.

    Notes:
        This class expects any input it receives to be well-formed; any
        tokenized lists you pass it directly (instead of through the
        ``BooleanExpression`` class) will not be checked.

    Attributes:
        postfix_tokens (List[str]): The tokens in the expression from which to
            build the tree.
        root (tt.trees.ExpressionTreeNode): The root of the tree;
            ``None`` for an empty tree.

    """

    def __init__(self, postfix_tokens):
        self.postfix_tokens = postfix_tokens

        self.root = None
        self._build_tree()

    def _build_tree(self):
        """Iterate over the ``postfix_tokens``, constructing the tree.

        Notes:
            This method will populate this class's ``root`` attribute.

        """
        if not self.postfix_tokens:
            self.root = None
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

        self.root = stack.pop()

    def __str__(self):
        if self.root is None:
            return 'Empty!'
        else:
            return str(self.root)[:-1]
