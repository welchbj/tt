"""An expression tree implementation for Boolean expressions."""


class BooleanExpressionTree(object):

    """An expression tree for Boolean expressions.

    Notes:
        This class expects any input it receives to be well-formed; any
        tokenized lists you pass it directly (instead of through the
        ``BooleanExpression`` class) will not be checked.

    Attributes:
        root (tt.trees.BooleanExpressionTreeNode): The root of the tree;
            ``None`` for an empty tree.
        postfix_tokens (List[str]): The tokens in the expression from which to
            build the tree.

    """

    def __init__(self, postfix_tokens):
        self.postfix_tokens = postfix_tokens

    def __str__(self):
        # TODO
        pass
