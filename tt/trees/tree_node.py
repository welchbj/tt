"""A node for use in expression trees."""

from ..operators import CONSTANT_VALUES, OPERATOR_MAPPING


class ExpressionTreeNode(object):

    """A base class for expression tree nodes.

    Attributes:
        symbol_name (str): The string operator/operand name of wrapped in this
            node.
        l_child (tt.trees.ExpressionTreeNode, optional): This node's left
            child.
        right_child (tt.trees.ExpressionTreeNode, optional): This node's right
            child.

    """

    def __init__(self, symbol_name, l_child=None, r_child=None):
        self.symbol_name = symbol_name
        self.l_child = l_child
        self.r_child = r_child

    def evaluate(self, input_dict):
        raise NotImplementedError(
            'Expression tree nodes must implement `evaluate`.')

    def __str__(self, depth=0, indent_size=5, stem_list=[]):
        ret = ''

        if depth > 0:
            trunk = ('{}' + (indent_size - 1) * ' ') * (depth - 1)
            trunk = trunk.format(*stem_list)
            stem = '`' + (indent_size - 1) * '-'
            ret += trunk + stem + self.symbol_name
        else:
            ret += self.symbol_name

        ret += '\n'

        if self.r_child is not None:
            ret += self.r_child.__str__(
                depth=depth+1,
                indent_size=indent_size,
                stem_list=stem_list + ['|'])

        if self.l_child is not None:
            ret += self.l_child.__str__(
                depth=depth+1,
                indent_size=indent_size,
                stem_list=stem_list + [' '])

        return ret


class BinaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for binary operators.

    Attributes:
        operator (tt.operators.BooleanOperator): The actual operator wrapped
            in this node.

    """

    def __init__(self, operator_str, l_child, r_child):
        super(BinaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child, r_child)

        self.operator_str = operator_str
        self.operator = OPERATOR_MAPPING[operator_str]

    def evaluate(self, input_dict):
        # TODO
        pass


class UnaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for unary operators."""

    def __init__(self, operator_str, l_child):
        super(UnaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child)

        self.operator = OPERATOR_MAPPING[operator_str]

    def evaluate(self, input_dict):
        # TODO
        pass


class OperandExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for operands."""

    def __init__(self, operand_str):
        super(OperandExpressionTreeNode, self).__init__(operand_str)

    def evaluate(self, input_dict):
        # TODO
        pass
