"""A node for use in expression trees."""


class BooleanExpressionTreeNode(object):

    """A node for use in a Boolean expression tree.

    Attributes:
        operator_str (str): The string representing the operator held by this
            node.
        operand_a (str|BooleanExpressionTreeNode): Either the name of the first
            operand or another node in the tree.
        operand_b (str|BooleanExpressionTreeNode|None): Either the name of the
            second operand, another node in the tree, or ``None``, if this node
            holds a unary operator.

    """

    def __init__(self):
        pass
