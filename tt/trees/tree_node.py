"""A node, and related classes, for use in expression trees."""

from ..definitions import (MAX_OPERATOR_STR_LEN, OPERATOR_MAPPING, TT_AND_OP,
                           TT_OR_OP)


_DEFAULT_INDENT_SIZE = MAX_OPERATOR_STR_LEN + 1


class ExpressionTreeNode(object):

    """A base class for expression tree nodes.

    This class is extended within tt and is not meant to be used
    directly. If you plan to extend it, note that descendants of this class
    must compute the ``_is_cnf`` boolean attribute within their initialization.

    """

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
        """This node's left child; ``None`` indicates the absence of a child.

        :type: :class:`ExpressionTreeNode`, optional

        """
        return self._l_child

    @property
    def r_child(self):
        """This node's left child; ``None`` indicates the absence of a child.

        :type: :class:`ExpressionTreeNode`, optional

        """
        return self._r_child

    @property
    def is_cnf(self):
        """Whether the tree rooted at this node is in cnf form.

        :type: :class:`bool <python:bool>`

        """
        return self._is_cnf

    def evaluate(self, input_dict):
        """Recursively evaluate this node.

        This is an interface that should be defined in sub-classes. Node
        evaluation does no checking of the validity of inputs; they should be
        check before being passed here.

        :param input_dict: A dictionary mapping expression symbols to the value
            for which they should be subsituted in expression evaluation.
        :type input_dict: Dict{:class:`str <python:str>`: truthy

        :returns: The evaluation of the tree rooted at this node.
        :rtype: :class:`bool <python:bool>`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement `evaluate`.')

    def __str__(self):
        return self._str_helper()[:-1]

    def _str_helper(self, depth=0, indent_size=_DEFAULT_INDENT_SIZE,
                    stem_list=[]):
        """Helper method for __str__."""
        ret = ''

        if depth > 0:
            trunk = ('{}' + (indent_size - 1) * ' ') * (depth - 1)
            trunk = trunk.format(*stem_list)
            stem = '`' + (indent_size - 1) * '-'
            ret += trunk + stem + self._symbol_name
        else:
            ret += self._symbol_name

        ret += '\n'

        l_child_stem = '|' if self._r_child is not None else ' '

        if self._l_child is not None:
            ret += self._l_child._str_helper(
                depth=depth+1,
                indent_size=indent_size,
                stem_list=stem_list + [l_child_stem])

        if self.r_child is not None:
            ret += self.r_child._str_helper(
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
        self._is_cnf = self._cnf_status()

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

    def _cnf_status(self):
        """Helper to determine cnf status of tree rooted at this node.

        :returns: True if the tree rooted at this node is in cnf form,
            otherwise False.
        :rtype: :class:`bool <python:bool>`

        """
        if self._operator != TT_AND_OP and self._operator != TT_OR_OP:
            return False

        if not self.l_child.is_cnf or not self.r_child.is_cnf:
            return False

        if self._operator == TT_AND_OP:
            if isinstance(self.l_child, BinaryOperatorExpressionTreeNode):
                if self.l_child.operator != TT_OR_OP:
                    return False

        if self._operator == TT_OR_OP:
            if isinstance(self.l_child, BinaryOperatorExpressionTreeNode):
                return False

            if isinstance(self.r_child, BinaryOperatorExpressionTreeNode):
                if self.r_child.operator != TT_OR_OP:
                    return False

        return True


class UnaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for unary operators."""

    def __init__(self, operator_str, l_child):
        super(UnaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child)

        self._operator = OPERATOR_MAPPING[operator_str]
        self._is_cnf = isinstance(self.l_child, OperandExpressionTreeNode)

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
        self._is_cnf = True

    def evaluate(self, input_dict):
        if self.symbol_name == '0':
            return False
        elif self.symbol_name == '1':
            return True
        else:
            return input_dict[self.symbol_name]
