"""A node, and related classes, for use in expression trees."""

from ..definitions import MAX_OPERATOR_STR_LEN, OPERATOR_MAPPING


_DEFAULT_INDENT_SIZE = MAX_OPERATOR_STR_LEN + 1


class ExpressionTreeNode(object):

    """A base class for expression tree nodes."""

    def __init__(self, symbol_name, l_child=None, r_child=None):
        self._symbol_name = symbol_name
        self._l_child = l_child
        self._r_child = r_child

    @property
    def symbol_name(self):
        """The string operator/operand name wrapped in this node.

        :type: :class:`str <python:str>`

        """
        return self._symbol_name

    @property
    def l_child(self):
        """ This node's left child; ``None`` indicates the absence of a child.

        :type: :class:`ExpressionTreeNode`, optional

        """
        return self._l_child

    @property
    def r_child(self):
        """ This node's left child; ``None`` indicates the absence of a child.

        :type: :class:`ExpressionTreeNode`, optional

        """
        return self._r_child

    def evaluate(self, input_dict):
        """Recursively evaluate this node.

        This is an interface that should be defined in sub-classes.

        :param input_dict: A dictionary mapping expression symbols to the value
            for which they should be subsituted in expression evaluation.
        :type input_dict: Dict{:class:`str <python:str>`: truthy}

        .. note::

            Node evaluation does no checking of the validity of inputs; they
            should be check before being passed here.

        :returns: The evaluation of the tree rooted at this node.
        :rtype: :class:`bool <python:bool>`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement `evaluate`.')

    def __str__(self, depth=0, indent_size=_DEFAULT_INDENT_SIZE, stem_list=[]):
        ret = ''

        if depth > 0:
            trunk = ('{}' + (indent_size - 1) * ' ') * (depth - 1)
            trunk = trunk.format(*stem_list)
            stem = '`' + (indent_size - 1) * '-'
            ret += trunk + stem + self._symbol_name
        else:
            ret += self._symbol_name

        ret += '\n'

        if self.r_child is not None:
            ret += self.r_child.__str__(
                depth=depth+1,
                indent_size=indent_size,
                stem_list=stem_list + ['|'])

        if self._l_child is not None:
            ret += self._l_child.__str__(
                depth=depth+1,
                indent_size=indent_size,
                stem_list=stem_list + [' '])

        return ret


class BinaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for binary operators."""

    def __init__(self, operator_str, l_child, r_child):
        super(BinaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child, r_child)

        self._operator = OPERATOR_MAPPING[operator_str]

    @property
    def operator(self):
        """The actual operator object wrapped in this node.

        :type: :class:`BooleanOperator\
                       <tt.definitions.operators.BooleanOperator>`

        """
        return self._operator

    def evaluate(self, input_dict):
        return self.operator.eval_func(
            self.l_child.evaluate(input_dict),
            self.r_child.evaluate(input_dict))


class UnaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for unary operators."""

    def __init__(self, operator_str, l_child):
        super(UnaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child)

        self._operator = OPERATOR_MAPPING[operator_str]

    @property
    def operator(self):
        """The actual operator object wrapped in this node.

        :type: :class:`BooleanOperator\
                       <tt.definitions.operators.BooleanOperator>`

        """
        return self._operator

    def evaluate(self, input_dict):
        return self.operator.eval_func(
            self.l_child.evaluate(input_dict))


class OperandExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for operands.

    Nodes of this type will always be leaves in an expression tree.

    """

    def __init__(self, operand_str):
        super(OperandExpressionTreeNode, self).__init__(operand_str)

    def evaluate(self, input_dict):
        if self.symbol_name == '0':
            return False
        elif self.symbol_name == '1':
            return True
        else:
            return input_dict[self.symbol_name]
