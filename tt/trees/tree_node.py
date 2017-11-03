"""A node, and related classes, for use in expression trees."""

import itertools

from collections import deque

from tt.definitions import (
    MAX_OPERATOR_STR_LEN,
    OPERATOR_MAPPING,
    SYMBOLIC_OPERATOR_MAPPING,
    TT_AND_OP,
    TT_IMPL_OP,
    TT_NAND_OP,
    TT_NOR_OP,
    TT_NOT_OP,
    TT_OR_OP,
    TT_XOR_OP,
    TT_XNOR_OP)
from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError,
    RequiresNormalFormError)


_DEFAULT_INDENT_SIZE = MAX_OPERATOR_STR_LEN + 1


class ExpressionTreeNode(object):

    """A base class for expression tree nodes.

    This class is extended within tt and is not meant to be used
    directly.

    If you plan to extend it, note that descendants of this class
    must compute the ``_is_cnf``, ``_is_dnf``, and ``_is_really_unary`` boolean
    attributes and the ``_non_negated_symbol_set`` and ``_negated_symbol_set``
    set attributes within their initialization. Additionally, descendants of
    this class must implemented the ``__eq__`` magic method (but not
    ``__ne__``) as well as the private ``_copy`` transformation.

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

        :type: :class:`ExpressionTreeNode` or ``None``

        """
        return self._l_child

    @property
    def r_child(self):
        """This node's left child; ``None`` indicates the absence of a child.

        :type: :class:`ExpressionTreeNode` or ``None``

        """
        return self._r_child

    @property
    def is_cnf(self):
        """Whether the tree rooted at this node is in conjunctive normal form.

        :type: :class:`bool <python:bool>`

        """
        return self._is_cnf

    @property
    def is_dnf(self):
        """Whether the tree rooted at this node is in disjunctive normal form.

        :type: :class:`bool <python:bool>`

        """
        return self._is_dnf

    @property
    def non_negated_symbol_set(self):
        """A set of the non-negated symbols present in the tree rooted here.

        :type: Set[:class:`str <python:str>`]

        """
        return self._non_negated_symbol_set

    @property
    def negated_symbol_set(self):
        """A set of the negated symbols present in the tree rooted here.

        :type: Set[:class:`str <python:str>`]

        """
        return self._negated_symbol_set

    @property
    def is_really_unary(self):
        """Whether the tree rooted at this node contains no binary operators.

        :type: :class:`bool <python:bool>`

        """
        return self._is_really_unary

    @staticmethod
    def build_tree(postfix_tokens):
        """Build a tree from a list of expression tokens in postfix order.

        This method does not check that the tokens are indeed in postfix order;
        undefined behavior will ensue if you pass tokens in an order other than
        postfix.

        :param postfix_tokens: A list of string tokens from which to construct
            the tree of expression nodes.
        :type postfix_tokens: List[:class:`str <python:str>`]

        :returns: The root node of the constructed tree.
        :rtype: :class:`ExpressionTreeNode`

        :raises InvalidArgumentTypeError: If ``postfix_tokens`` is not a list
            of strings.
        :raises InvalidArgumentValueError: If ``postfix_tokens`` is empty.

        """
        if (not isinstance(postfix_tokens, list) or
                not all(isinstance(elt, str) for elt in postfix_tokens)):
            raise InvalidArgumentTypeError(
                'postfix_tokens must be a list of strings')
        elif not postfix_tokens:
            raise InvalidArgumentValueError('postfix_tokens cannot be empty')

        stack = []
        operators = OPERATOR_MAPPING.keys()

        for token in postfix_tokens:
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

        return stack.pop()

    def iter_clauses(self):
        """Iterate the clauses in the expression tree rooted at this node.

        If the normal form of the expression is ambiguous, then precedence will
        be given to conjunctive normal form.

        :returns: Iterator of each CNF or DNF clause, rooted by a tree node,
            contained within the expression tree rooted at this node.
        :rtype: Iterator[:class:`ExpressionTreeNode`]

        :raises RequiresNormalFormError: If this expression is  not in
            conjunctive or disjunctive normal form.

        """
        if self._is_cnf:
            for node in self.iter_cnf_clauses():
                yield node
        elif self._is_dnf:
            for node in self.iter_dnf_clauses():
                yield node
        else:
            raise RequiresNormalFormError(
                'Must be in conjunctive or disjunctive normal form to '
                'iterate clauses')

    def iter_cnf_clauses(self):
        """Iterate the clauses in conjunctive normal form order.

        :returns: Iterator of each CNF clause, rooted by a tree node, contained
            within the expression tree rooted at this node.
        :rtype: Iterator[:class:`ExpressionTreeNode`]

        :raises RequiresNormalFormError: If the expression tree rooted at this
            node is not in conjunctive normal form.

        """
        if not self._is_cnf:
            raise RequiresNormalFormError(
                'Must be in conjunctive normal form to iterate CNF clauses')
        elif (isinstance(self, BinaryOperatorExpressionTreeNode) and
                self._operator == TT_AND_OP):
            child_iter = itertools.chain(
                self._l_child.iter_cnf_clauses(),
                self._r_child.iter_cnf_clauses())
            for node in child_iter:
                yield node
        else:
            yield self

    def iter_dnf_clauses(self):
        """Iterate the clauses in disjunctive normal form order.

        :returns: Iterator of each DNF clause, rooted by a tree node, contained
            within the expression tree rooted at this node.
        :rtype: Iterator[:class:`ExpressionTreeNode`]

        :raises RequiresNormalFormError: If the expression tree rooted at this
            node is not in disjunctive normal form.

        """
        if not self._is_dnf:
            raise RequiresNormalFormError(
                'Must be in conjunctive normal form to iterate DNF clauses')
        elif (isinstance(self, BinaryOperatorExpressionTreeNode) and
                self._operator == TT_OR_OP):
            child_iter = itertools.chain(
                self._l_child.iter_dnf_clauses(),
                self._r_child.iter_dnf_clauses())
            for node in child_iter:
                yield node
        else:
            yield self

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
            'Expression tree nodes must implement evaluate().')

    def _copy(self):
        """Recursively return a copy of the tree rooted at this node."""
        raise NotImplementedError(
            'Expression tree nodes must implement _copy()')

    def to_cnf(self):
        """Return a transformed node, in conjunctive normal form.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all operators transformed to
            consist only of NOTs, ANDs, and ORs.
        :rtype: :class:`ExpressionTreeNode`

        """
        prev_node = self.to_primitives()
        if prev_node.is_cnf:
            return prev_node

        next_node = prev_node
        while True:
            prev_node = next_node
            next_node = next_node.apply_de_morgans()
            if next_node == prev_node:
                break

        prev_node = next_node.coalesce_negations()
        while True:
            prev_node = next_node
            next_node = next_node.distribute_ors()
            if next_node == prev_node:
                break

        while True:
            prev_node = next_node
            next_node = prev_node.apply_inverse_law()
            if next_node == prev_node:
                break

        while True:
            prev_node = next_node
            next_node = prev_node.apply_idempotent_law()
            if next_node == prev_node:
                break

        while True:
            prev_node = next_node
            next_node = prev_node.apply_identity_law()
            if next_node == prev_node:
                break

        while True:
            prev_node = next_node
            next_node = prev_node.apply_idempotent_law()
            if next_node == prev_node:
                break

        while True:
            prev_node = next_node
            next_node = prev_node.coalesce_negations()
            if next_node == prev_node:
                break

        return next_node

    def to_primitives(self):
        """Return a transformed node, containing only NOTs, ANDs, and ORs.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all operators transformed to
            consist only of NOTs, ANDs, and ORs.
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement to_primitives()')

    def coalesce_negations(self):
        """Return a transformed node, with consecutive negations coalesced.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all consecutive negations
            compressed into the minimal number of equivalent negations (either
            one or none).
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement coalesce_negations()')

    def apply_de_morgans(self):
        """Return a transformed node, with De Morgan's Law applied.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all negated AND and OR operators
            transformed, following De Morgan's Law.
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement apply_de_morgans()')

    def apply_identity_law(self):
        """Return a transformed node, with the Identity Law applied.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        This transformation will achieve the following effects by applying the
        Inverse Law to the *AND* and *OR* operators::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('A and 1').tree
            >>> print(tree.apply_identity_law())
            A
            >>> tree = BooleanExpression('0 or B').tree
            >>> print(tree.apply_identity_law())
            B

        It should also be noted that this transformation will also apply
        the annihilator properties of the logical *AND* and *OR* operators. For
        example::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('A and 0').tree
            >>> print(tree.apply_identity_law())
            0
            >>> tree = BooleanExpression('1 or B').tree
            >>> print(tree.apply_identity_law())
            1

        :returns: An expression tree node with AND and OR identities
            simplified.
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement apply_identity_law()')

    def apply_idempotent_law(self):
        """Returns a transformed node, with the Idempotent Law applied.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects

        :returns: An expression tree node with the Idempotent Law applied to
            *AND* and *OR* operators.
        :rtype: :class:`ExpressionTreeNode`

        This transformation will apply the Idempotent Law to *AND* and *OR*
        expressions involving repeated operands. Here are a few examples::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('A and A').tree
            >>> print(tree.apply_idempotent_law())
            A
            >>> tree = BooleanExpression('~B or ~~~B').tree
            >>> print(tree.apply_idempotent_law())
            ~
            `----B

        In the latter of the two above examples, we see that this
        transformation will compare operands with negations condensed. This
        transformation will also prune redundant operands from CNF and DNF
        clauses. Let's take a look::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('A and B and B and C and ~C and ~~C \
and D').tree
            >>> print(tree.apply_idempotent_law())
            and
            `----and
            |    `----and
            |    |    `----and
            |    |    |    `----A
            |    |    |    `----B
            |    |    `----C
            |    `----~
            |         `----C
            `----D

        """
        raise NotImplementedError(
            'Expression tree nodes must implement apply_idempotent_law()')

    def apply_inverse_law(self):
        """Return a transformed node, with the Inverse Law applied.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with the Inverse Law applied to
            applicable clauses.
        :rtype: :class:`ExpressionTreeNode`

        This transformation will apply the Inverse Law to *AND* and *OR*
        expressions involving the negated and non-negated forms of a variable.
        Here are a few examples::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('~A and A').tree
            >>> print(tree.apply_inverse_law())
            0
            >>> tree = BooleanExpression('B or !B').tree
            >>> print(tree.apply_inverse_law())
            1

        Note that this transformation will **not** reduce expressions of
        constants; the transformation :func:`apply_identity_law \
        <tt.trees.tree_node.ExpressionTreeNode.apply_identity_law>` will
        probably do what you want in this case, though.

        This transformation will also reduce expressions in CNF or DNF that
        contain negated and non-negated forms of the same symbol. Let's take a
        look::

            >>> from tt import BooleanExpression
            >>> tree = BooleanExpression('A or B or C or ~B').tree
            >>> print(tree.apply_inverse_law())
            1
            >>> tree = BooleanExpression('A and B and C and !B').tree
            >>> print(tree.apply_inverse_law())
            0

        """
        raise NotImplementedError(
            'Expression tree nodes must implement apply_inverse_law()')

    def distribute_ands(self):
        """Return a transformed nodes, with ANDs recursively distributed across
        ORed sub-expressions.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all applicable AND operators
            distributed across ORed sub-expressions.
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement distribute_ands()')

    def distribute_ors(self):
        """Return a transformed nodes, with ORs recursively distributed across
        ANDed sub-expressions.

        Since nodes are immutable, the returned node, and all descendants, are
        new objects.

        :returns: An expression tree node with all applicable OR operators
            distributed across ANDed sub-expressions.
        :rtype: :class:`ExpressionTreeNode`

        """
        raise NotImplementedError(
            'Expression tree nodes must implement distribute_ors()')

    def __eq__(self, other):
        raise NotImplementedError(
            'Expression tree nodes must implement __eq__')

    def __ne__(self, other):
        return not (self == other)

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

    def _get_op_strs(self, *ops):
        """Get the appropriate operator strings for the passed operators."""
        if self.symbol_name in SYMBOLIC_OPERATOR_MAPPING:
            return tuple(op.default_symbol_str for op in ops)
        else:
            return tuple(op.default_plain_english_str for op in ops)


class BinaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for binary operators."""

    def __init__(self, operator_str, l_child, r_child):
        super(BinaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child, r_child)

        self._operator = OPERATOR_MAPPING[operator_str]
        self._is_cnf = self._cnf_status()
        self._is_dnf = self._dnf_status()
        self._is_really_unary = False
        self._non_negated_symbol_set = \
            l_child._non_negated_symbol_set | r_child._non_negated_symbol_set
        self._negated_symbol_set = \
            l_child._negated_symbol_set | r_child._negated_symbol_set

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

    def _copy(self):
        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child._copy(),
            self._r_child._copy())

    def to_primitives(self):
        not_str, and_str, or_str = self._get_op_strs(
            TT_NOT_OP, TT_AND_OP, TT_OR_OP)

        if self._operator == TT_IMPL_OP:
            return BinaryOperatorExpressionTreeNode(
                or_str,
                UnaryOperatorExpressionTreeNode(
                    not_str, self._l_child.to_primitives()),
                self._r_child.to_primitives())
        elif self._operator == TT_XOR_OP:
            new_l_child = self._l_child.to_primitives()
            new_r_child = self._r_child.to_primitives()

            return BinaryOperatorExpressionTreeNode(
                or_str,
                BinaryOperatorExpressionTreeNode(
                    and_str,
                    new_l_child,
                    UnaryOperatorExpressionTreeNode(not_str, new_r_child)),
                BinaryOperatorExpressionTreeNode(
                    and_str,
                    UnaryOperatorExpressionTreeNode(not_str, new_l_child),
                    new_r_child))
        elif self._operator == TT_XNOR_OP:
            new_l_prim = self._l_child.to_primitives()
            new_r_prim = self._r_child.to_primitives()

            return BinaryOperatorExpressionTreeNode(
                or_str,
                BinaryOperatorExpressionTreeNode(
                    and_str,
                    new_l_prim,
                    new_r_prim),
                BinaryOperatorExpressionTreeNode(
                    and_str,
                    UnaryOperatorExpressionTreeNode(not_str, new_l_prim),
                    UnaryOperatorExpressionTreeNode(not_str, new_r_prim)))
        elif self._operator == TT_AND_OP:
            return BinaryOperatorExpressionTreeNode(
                and_str,
                self._l_child.to_primitives(), self._r_child.to_primitives())
        elif self._operator == TT_NAND_OP:
            new_l_child = self._l_child.to_primitives()
            new_r_child = self._r_child.to_primitives()

            return BinaryOperatorExpressionTreeNode(
                or_str,
                UnaryOperatorExpressionTreeNode(not_str, new_l_child),
                UnaryOperatorExpressionTreeNode(not_str, new_r_child))
        elif self._operator == TT_OR_OP:
            return BinaryOperatorExpressionTreeNode(
                or_str,
                self._l_child.to_primitives(), self._r_child.to_primitives())
        elif self._operator == TT_NOR_OP:
            new_l_child = self._l_child.to_primitives()
            new_r_child = self._r_child.to_primitives()

            return BinaryOperatorExpressionTreeNode(
                and_str,
                UnaryOperatorExpressionTreeNode(not_str, new_l_child),
                UnaryOperatorExpressionTreeNode(not_str, new_r_child))

    def coalesce_negations(self):
        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.coalesce_negations(),
            self._r_child.coalesce_negations())

    def apply_de_morgans(self):
        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_de_morgans(),
            self._r_child.apply_de_morgans())

    def apply_identity_law(self):
        op_is_and = self._operator == TT_AND_OP
        op_is_or = self._operator == TT_OR_OP

        new_l_child = self._l_child.apply_identity_law()
        if new_l_child.symbol_name == '1':
            if op_is_and:
                return self._r_child.apply_identity_law()
            elif op_is_or:
                return OperandExpressionTreeNode('1')
        elif new_l_child.symbol_name == '0':
            if op_is_and:
                return OperandExpressionTreeNode('0')
            elif op_is_or:
                return self._r_child.apply_identity_law()

        new_r_child = self._r_child.apply_identity_law()
        if new_r_child.symbol_name == '1':
            if op_is_and:
                return new_l_child
            elif op_is_or:
                return OperandExpressionTreeNode('1')
        elif new_r_child.symbol_name == '0':
            if op_is_and:
                return OperandExpressionTreeNode('0')
            elif op_is_or:
                return new_l_child

        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            new_l_child,
            new_r_child)

    def apply_idempotent_law(self):
        negations_applied = self.coalesce_negations()
        if negations_applied._is_cnf and negations_applied._is_dnf:
            negated_symbols_added = set()
            non_negated_symbols_added = set()
            filtered_clauses = deque()

            total_clause_count = 0
            clause_iter = (negations_applied.iter_cnf_clauses() if
                           self._operator == TT_AND_OP else
                           negations_applied.iter_dnf_clauses())
            for clause in clause_iter:
                total_clause_count += 1
                if isinstance(clause, OperandExpressionTreeNode):
                    if clause.symbol_name in non_negated_symbols_added:
                        continue
                    non_negated_symbols_added |= clause.non_negated_symbol_set
                    filtered_clauses.append(clause._copy())
                elif clause._l_child.symbol_name not in negated_symbols_added:
                    negated_symbols_added |= clause.negated_symbol_set
                    filtered_clauses.append(clause._copy())

            if len(filtered_clauses) == total_clause_count:
                # no redundant operands were pruned
                return self._copy()

            while len(filtered_clauses) > 1:
                filtered_clauses.appendleft(
                    BinaryOperatorExpressionTreeNode(
                        self.symbol_name,
                        filtered_clauses.popleft(),
                        filtered_clauses.popleft()))
            return filtered_clauses.pop()

        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_idempotent_law(),
            self._r_child.apply_idempotent_law())

    def apply_inverse_law(self):
        negations_applied = self.coalesce_negations()
        if negations_applied._is_cnf and negations_applied._is_dnf:
            if self._negated_symbol_set & self._non_negated_symbol_set:
                return OperandExpressionTreeNode(
                    '1' if self._operator == TT_OR_OP else '0')
        elif self._is_cnf:
            and_str = self.symbol_name
            inverted_clause_count = 0
            transformed_clauses = deque()
            for clause in self.iter_cnf_clauses():
                if clause.negated_symbol_set & clause.non_negated_symbol_set:
                    inverted_clause_count += 1
                    transformed_clauses.append(OperandExpressionTreeNode('1'))
                else:
                    transformed_clauses.append(clause._copy())

            if not inverted_clause_count:
                # we didn't change anything, so just return ourselves
                return self._copy()

            while len(transformed_clauses) > 1:
                transformed_clauses.append(
                    BinaryOperatorExpressionTreeNode(
                        and_str,
                        transformed_clauses.popleft(),
                        transformed_clauses.popleft()))
            return transformed_clauses.pop()
        elif self._is_dnf:
            or_str = self.symbol_name
            inverted_clause_count = 0
            transformed_clauses = deque()
            for clause in self.iter_dnf_clauses():
                if clause.negated_symbol_set & clause.non_negated_symbol_set:
                    inverted_clause_count += 1
                    transformed_clauses.append(OperandExpressionTreeNode('0'))
                else:
                    transformed_clauses.append(clause._copy())

            if not inverted_clause_count:
                # we didn't change anything, so just return ourselves
                return self._copy()

            while len(transformed_clauses) > 1:
                transformed_clauses.append(
                    BinaryOperatorExpressionTreeNode(
                        or_str,
                        transformed_clauses.popleft(),
                        transformed_clauses.popleft()))
            return transformed_clauses.pop()

        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_inverse_law(),
            self._r_child.apply_inverse_law())

    def distribute_ands(self):
        if self._operator == TT_AND_OP:
            (or_str,) = self._get_op_strs(TT_OR_OP)
            and_str = self.symbol_name

            if (isinstance(self._r_child, BinaryOperatorExpressionTreeNode) and
                    self._r_child.operator == TT_OR_OP):
                child_to_distribute = self._l_child.distribute_ands()
                child_distributed_upon = \
                    self._r_child._l_child.distribute_ands()
                child_to_be_distributed_upon = \
                    self._r_child._r_child.distribute_ands()

                return BinaryOperatorExpressionTreeNode(
                    or_str,
                    BinaryOperatorExpressionTreeNode(
                        and_str,
                        child_to_distribute,
                        child_distributed_upon).distribute_ands(),
                    BinaryOperatorExpressionTreeNode(
                        and_str,
                        child_to_distribute,
                        child_to_be_distributed_upon).distribute_ands())
            elif (isinstance(self._l_child, BinaryOperatorExpressionTreeNode)
                    and self._l_child.operator == TT_OR_OP):
                child_to_distribute = self._r_child.distribute_ands()
                child_distributed_upon = \
                    self._l_child._l_child.distribute_ands()
                child_to_be_distributed_upon = \
                    self._l_child._r_child.distribute_ands()

                return BinaryOperatorExpressionTreeNode(
                    or_str,
                    BinaryOperatorExpressionTreeNode(
                        and_str,
                        child_distributed_upon,
                        child_to_distribute).distribute_ands(),
                    BinaryOperatorExpressionTreeNode(
                        and_str,
                        child_to_be_distributed_upon,
                        child_to_distribute).distribute_ands())

        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.distribute_ands(),
            self._r_child.distribute_ands())

    def distribute_ors(self):
        if self._operator == TT_OR_OP:
            (and_str,) = self._get_op_strs(TT_AND_OP)
            or_str = self.symbol_name

            if (isinstance(self._r_child, BinaryOperatorExpressionTreeNode) and
                    self._r_child.operator == TT_AND_OP):
                child_to_distribute = self._l_child.distribute_ors()
                child_distributed_upon = \
                    self._r_child._l_child.distribute_ors()
                child_to_be_distributed_upon = \
                    self._r_child._r_child.distribute_ors()

                return BinaryOperatorExpressionTreeNode(
                    and_str,
                    BinaryOperatorExpressionTreeNode(
                        or_str,
                        child_to_distribute,
                        child_distributed_upon).distribute_ors(),
                    BinaryOperatorExpressionTreeNode(
                        or_str,
                        child_to_distribute,
                        child_to_be_distributed_upon).distribute_ors())
            elif (isinstance(self._l_child, BinaryOperatorExpressionTreeNode)
                    and self._l_child.operator == TT_AND_OP):
                child_to_distribute = self._r_child.distribute_ors()
                child_distributed_upon = \
                    self._l_child._l_child.distribute_ors()
                child_to_be_distributed_upon = \
                    self._l_child._r_child.distribute_ors()

                return BinaryOperatorExpressionTreeNode(
                    and_str,
                    BinaryOperatorExpressionTreeNode(
                        or_str,
                        child_distributed_upon,
                        child_to_distribute).distribute_ors(),
                    BinaryOperatorExpressionTreeNode(
                        or_str,
                        child_to_be_distributed_upon,
                        child_to_distribute).distribute_ors())

        return BinaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.distribute_ors(),
            self._r_child.distribute_ors())

    def __eq__(self, other):
        if isinstance(other, BinaryOperatorExpressionTreeNode):
            return (self._operator == other._operator and
                    self._l_child == other._l_child and
                    self._r_child == other._r_child)
        elif isinstance(other, ExpressionTreeNode):
            return False
        else:
            return NotImplemented

    def _cnf_status(self):
        """Helper to determine CNF status of the tree rooted at this node.

        :returns: True if the tree rooted at this node is in conjunctive
            normal form, otherwise False.
        :rtype: :class:`bool <python:bool>`

        """
        if not self._l_child.is_cnf or not self._r_child.is_cnf:
            return False

        if self._operator != TT_AND_OP and self._operator != TT_OR_OP:
            return False

        if self._operator == TT_OR_OP:
            if isinstance(self._l_child, BinaryOperatorExpressionTreeNode):
                if self._l_child._operator != TT_OR_OP:
                    return False

            if isinstance(self._r_child, BinaryOperatorExpressionTreeNode):
                if self._r_child.operator != TT_OR_OP:
                    return False

        return True

    def _dnf_status(self):
        """Helper to determine DNF status of the tree rooted at this node.

        :returns: True if the tree rooted at this node is in disjunctive
            normal form, otherwise False.
        :rtype: :class:`bool <python:bool>`

        """
        if not self._l_child.is_dnf or not self._r_child.is_dnf:
            return False

        if self._operator != TT_AND_OP and self._operator != TT_OR_OP:
            return False

        if self._operator == TT_AND_OP:
            if isinstance(self._l_child, BinaryOperatorExpressionTreeNode):
                if self._l_child._operator != TT_AND_OP:
                    return False

            if isinstance(self._r_child, BinaryOperatorExpressionTreeNode):
                if self._r_child.operator != TT_AND_OP:
                    return False

        return True


class UnaryOperatorExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for unary operators."""

    def __init__(self, operator_str, l_child):
        super(UnaryOperatorExpressionTreeNode, self).__init__(
            operator_str, l_child)

        self._operator = OPERATOR_MAPPING[operator_str]
        self._is_cnf = isinstance(self.l_child, OperandExpressionTreeNode)
        self._is_dnf = self._is_cnf
        self._is_really_unary = l_child._is_really_unary

        if self._is_really_unary:
            # this node has the opposite of its children
            self._non_negated_symbol_set, self._negated_symbol_set = (
                set(l_child._negated_symbol_set),
                set(l_child._non_negated_symbol_set))
        else:
            self._non_negated_symbol_set, self._negated_symbol_set = (
                set(l_child._non_negated_symbol_set),
                set(l_child._negated_symbol_set))

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

    def _copy(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name, self._l_child._copy())

    def to_primitives(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name, self._l_child.to_primitives())

    def coalesce_negations(self):
        if isinstance(self._l_child, UnaryOperatorExpressionTreeNode):
            return self._l_child._l_child.coalesce_negations()
        elif self._l_child.symbol_name == '0':
            return OperandExpressionTreeNode('1')
        elif self._l_child.symbol_name == '1':
            return OperandExpressionTreeNode('0')
        else:
            return UnaryOperatorExpressionTreeNode(
                self.symbol_name,
                self._l_child.coalesce_negations())

    def apply_de_morgans(self):
        if isinstance(self._l_child, BinaryOperatorExpressionTreeNode):
            binary_node = self._l_child
            op = binary_node._operator
            not_str, and_str, or_str = self._get_op_strs(
                TT_NOT_OP, TT_AND_OP, TT_OR_OP)

            notted_l_child = UnaryOperatorExpressionTreeNode(
                not_str, binary_node._l_child).apply_de_morgans()
            notted_r_child = UnaryOperatorExpressionTreeNode(
                not_str, binary_node._r_child).apply_de_morgans()

            if op == TT_AND_OP:
                return BinaryOperatorExpressionTreeNode(
                    or_str, notted_l_child, notted_r_child)
            elif op == TT_OR_OP:
                return BinaryOperatorExpressionTreeNode(
                    and_str, notted_l_child, notted_r_child)

        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_de_morgans())

    def apply_identity_law(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_identity_law())

    def apply_idempotent_law(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_idempotent_law())

    def apply_inverse_law(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.apply_inverse_law())

    def distribute_ands(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.distribute_ands())

    def distribute_ors(self):
        return UnaryOperatorExpressionTreeNode(
            self.symbol_name,
            self._l_child.distribute_ors())

    def __eq__(self, other):
        if isinstance(other, UnaryOperatorExpressionTreeNode):
            return self._l_child == other._l_child
        elif isinstance(other, ExpressionTreeNode):
            return False
        else:
            return NotImplemented


class OperandExpressionTreeNode(ExpressionTreeNode):

    """An expression tree node for operands.

    Nodes of this type will always be leaves in an expression tree.

    """

    def __init__(self, operand_str):
        super(OperandExpressionTreeNode, self).__init__(operand_str)
        self._is_cnf = True
        self._is_dnf = True
        self._is_really_unary = True
        self._non_negated_symbol_set = {self.symbol_name}
        self._negated_symbol_set = set()

    def evaluate(self, input_dict):
        if self.symbol_name == '0':
            return False
        elif self.symbol_name == '1':
            return True
        else:
            return input_dict[self.symbol_name]

    def _copy(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def to_primitives(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def coalesce_negations(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def apply_de_morgans(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def apply_identity_law(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def apply_idempotent_law(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def apply_inverse_law(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def distribute_ands(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def distribute_ors(self):
        return OperandExpressionTreeNode(self.symbol_name)

    def __eq__(self, other):
        if isinstance(other, OperandExpressionTreeNode):
            return self.symbol_name == other.symbol_name
        elif isinstance(other, ExpressionTreeNode):
            return False
        else:
            return NotImplemented
