"""Tools for interacting with Boolean expressions."""

import re

from contextlib import contextmanager

from tt._assertions import (
    assert_all_valid_keys,
    assert_iterable_contains_all_expr_symbols)
from tt.definitions import (
    boolean_variables_factory,
    CONSTANT_VALUES,
    DELIMITERS,
    is_valid_identifier,
    OPERATOR_MAPPING,
    SYMBOLIC_OPERATOR_MAPPING,
    TT_NOT_OP)
from tt.errors import (
    AlreadyConstrainedSymbolError,
    BadParenPositionError,
    EmptyExpressionError,
    ExpressionOrderError,
    InvalidArgumentTypeError,
    InvalidArgumentValueError,
    InvalidIdentifierError,
    NoEvaluationVariationError,
    UnbalancedParenError)
from tt.satisfiability import (
    picosat)
from tt.trees import (
    BinaryOperatorExpressionTreeNode,
    ExpressionTreeNode,
    OperandExpressionTreeNode,
    UnaryOperatorExpressionTreeNode)


class BooleanExpression(object):

    """An interface for interacting with a Boolean expression.

    Instances of ``BooleanExpression`` are meant to be immutable and can be
    instantiated from a few different representations of expressions. The
    simplest way to make an expression object is from a string::

        >>> from tt import BooleanExpression
        >>> BooleanExpression('(A or B) iff (C and D)')
        <BooleanExpression "(A or B) iff (C and D)">

    If you already have an instance of :class:`ExpressionTreeNode \
    <tt.trees.tree_node.ExpressionTreeNode>` laying around, you can make a
    new expression object from that, too::

        >>> from tt import ExpressionTreeNode
        >>> tree_root = ExpressionTreeNode.build_tree(
        ...     ['A', 'B', 'or',
        ...      'C', 'D', 'and',
        ...      'iff'])
        >>> BooleanExpression(tree_root)
        <BooleanExpression "(A or B) iff (C and D)">

    Additionally, any sub-tree node can be used to build an expression object.
    Continuing from above, let's make a new expression object for each of the
    sub-expressions wrapped in parentheses::

        >>> BooleanExpression(tree_root.l_child)
        <BooleanExpression "A or B">
        >>> BooleanExpression(tree_root.r_child)
        <BooleanExpression "C and D">

    Expressions also implement the equality and inequality operators (``==``
    and ``!=``). Equality is determined by the same semantic structure and the
    same operand names; the string used to represent the operators in two
    expressions is not taken into account. Here's a few examples::

        >>> from tt import BooleanExpression as be
        >>> be('A or B or C') == be('A or B or C')
        True
        >>> be('A or B or C') == be('A || B || C')
        True
        >>> be('A or B or C') == be('A or C or B')
        False

    :param expr: The expression representation from which this object is
        derived.
    :type expr: :class:`str <python:str>` or :class:`ExpressionTreeNode \
        <tt.trees.tree_node.ExpressionTreeNode>`

    :raises BadParenPositionError: If the passed expression contains a
        parenthesis in an invalid position.
    :raises EmptyExpressionError: If the passed expressions contains nothing
        other than whitespace.
    :raises ExpressionOrderError: If the expression contains invalid
        consecutive operators or operands.
    :raises InvalidArgumentTypeError: If ``expr`` is not an acceptable type.
    :raises InvalidIdentifierError: If any parsed variable symbols in the
        expression are invalid identifiers.
    :raises UnbalancedParenError: If any parenthesis pairs remain unbalanced.

    It is important to note that aside from :exc:`InvalidArgumentTypeError \
    <tt.errors.arguments.InvalidArgumentTypeError>`, all exceptions raised in
    expression initialization will be descendants of :exc:`GrammarError \
    <tt.errors.grammar.GrammarError>`.

    """

    def __init__(self, expr):
        if not isinstance(expr, (str, ExpressionTreeNode)):
            raise InvalidArgumentTypeError(
                'expr must be a str or ExpressionTreeNode')

        self._symbols = []
        self._symbol_set = set()
        self._tokens = []
        self._postfix_tokens = []

        if isinstance(expr, str):
            self._init_from_str(expr)
        elif isinstance(expr, ExpressionTreeNode):
            self._init_from_expr_node(expr)

        self._symbol_vals_factory = boolean_variables_factory(self._symbols)
        self._tree = ExpressionTreeNode.build_tree(self._postfix_tokens)
        self._constraints = {}
        self._constrained_symbol_set = set()

    def _init_from_expr_node(self, expr_node):
        """Initalize this object from an expression node."""
        self._raw_expr = ''

        with self._symbol_set_includes_constant_values():
            self._init_from_expr_node_recursive_helper(expr_node)

    def _init_from_expr_node_recursive_helper(self, expr_node, parent=None):
        """Recursive helper for initializing from an expression node.

        This method will populate the ``_symbols``, ``_symbol_set``,
        ``_postfix_tokens``, ``_tokens``, and ``_raw_expr`` attributes of this
         object.

        """
        if isinstance(expr_node, OperandExpressionTreeNode):
            operand_str = expr_node.symbol_name

            self._tokens.append(operand_str)
            self._postfix_tokens.append(operand_str)
            self._raw_expr += operand_str
            if operand_str not in self._symbol_set:
                self._symbols.append(operand_str)
                self._symbol_set.add(operand_str)
        elif isinstance(expr_node, UnaryOperatorExpressionTreeNode):
            operator_str = expr_node.symbol_name

            self._tokens.append(operator_str)

            self._raw_expr += operator_str
            if operator_str not in SYMBOLIC_OPERATOR_MAPPING:
                self._raw_expr += ' '

            self._init_from_expr_node_recursive_helper(
                expr_node.l_child, parent=expr_node)
            self._postfix_tokens.append(operator_str)
        elif isinstance(expr_node, BinaryOperatorExpressionTreeNode):
            operator_str = expr_node.symbol_name
            include_parens = True

            if parent is None:
                include_parens = False
            elif isinstance(parent, BinaryOperatorExpressionTreeNode):
                this_operator = OPERATOR_MAPPING[operator_str]
                parent_operator = OPERATOR_MAPPING[parent.symbol_name]
                if (expr_node is parent.r_child and
                        this_operator == parent_operator):
                    include_parens = False
                elif (expr_node is parent.l_child and
                        this_operator == parent_operator and
                        (parent.r_child.is_really_unary or
                            this_operator == parent.r_child.operator)):
                    include_parens = False

            if include_parens:
                self._tokens.append('(')
                self._raw_expr += '('

            self._init_from_expr_node_recursive_helper(
                expr_node.l_child, parent=expr_node)

            self._tokens.append(operator_str)
            self._raw_expr += (' ' + operator_str + ' ')

            self._init_from_expr_node_recursive_helper(
                expr_node.r_child, parent=expr_node)

            if include_parens:
                self._tokens.append(')')
                self._raw_expr += ')'

            self._postfix_tokens.append(operator_str)

    def _init_from_str(self, raw_expr_str):
        """Initalize this object from a raw expression string."""
        self._raw_expr = raw_expr_str

        with self._symbol_set_includes_constant_values():
            self._tokenize()
            self._to_postfix()

    @property
    def is_cnf(self):
        """Whether this expression is in conjunctive norma form or not.

        :type: :class:`bool <python:bool>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A or ~B) and (~C or D or E) and F')
            >>> b.is_cnf
            True
            >>> b = BooleanExpression('A nand B')
            >>> b.is_cnf
            False

        """
        return self._tree.is_cnf

    @property
    def is_dnf(self):
        """Whether this expression is in conjunctive normal form or not.

        :type: :class:`bool <python:bool>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A and B) or (~C and D)')
            >>> b.is_dnf
            True
            >>> b = BooleanExpression('(op1 or !op2) and (op3 or op4)')
            >>> b.is_dnf
            False

        """
        return self._tree.is_dnf

    @property
    def raw_expr(self):
        """The raw string expression, parsed upon initialization.

        This is what you pass into the ``BooleanExpression`` constructor; it is
        kept on the object as an attribute for convenience.

        :type: :class:`str <python:str>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A nand B')
            >>> b.raw_expr
            'A nand B'

        """
        return self._raw_expr

    @property
    def symbols(self):
        """The list of unique symbols present in this expression.

        The order of the symbols in this list matches the order of symbol
        appearance in the original expression.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.symbols
            ['A', 'B', 'C']

        """
        return self._symbols

    @property
    def tokens(self):
        """The parsed, non-whitespace tokens of an expression.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.tokens
            ['A', 'xor', '(', 'B', 'or', 'C', ')']

        """
        return self._tokens

    @property
    def postfix_tokens(self):
        """Similar to the ``tokens`` attribute, but in postfix order.

        :type: List[:class:`str <python:str>`]

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> b.postfix_tokens
            ['A', 'B', 'C', 'or', 'xor']

        """
        return self._postfix_tokens

    @property
    def tree(self):
        """The tree node representing the root of the tree of this expression.

        :type: :class:`ExpressionTreeNode \
            <tt.trees.tree_node.ExpressionTreeNode>`

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor (B or C)')
            >>> print(b.tree)
            xor
            `----A
            `----or
                 `----B
                 `----C

        """
        return self._tree

    def __eq__(self, other):
        if isinstance(other, BooleanExpression):
            return self._tree == other._tree
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self._raw_expr

    def __repr__(self):
        return '<BooleanExpression "{}">'.format(self._raw_expr)

    @contextmanager
    def constrain(self, **kwargs):
        """A context manager to impose satisfiability constraints.

        This is the interface for adding assumptions to the satisfiability
        solving functionality provided through the :func:`sat_one` and
        :func:`sat_all` methods.

        It should be noted that this context manager is only designed to work
        with the satisfiability-related functionality of this class.
        Constrained symbol values will not have an effect on non-sat methods of
        this class. For example::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A or B) and (C or D)')
            >>> with b.constrain(A=1):
            ...     b.evaluate(A=0, B=1, C=1, D=0)
            ...
            True

        This context manager returns a reference to the same object upon which
        it is called. This behavior is designed with the following use case in
        mind::

            >>> from tt import BooleanExpression
            >>> with BooleanExpression('A or B').constrain(A=1, B=0) as b:
            ...     b.sat_one()
            ...
            <BooleanValues [A=1, B=0]>

        :param kwargs: Keys are names of symbols in this expression; the
            specified value for each of these keys will be added to the
            ``constraints`` attribute of this object for the duration of the
            context manager.

        :returns: A reference to the same object that called this method
            (i.e., ``self`` in the context of this method).
        :rtype: :class:`BooleanExpression`

        :raises AlreadyConstrainedSymbolError: If trying to constrain this
            expression with multiple context managers.
        :raises ExtraSymbolError: If a symbol not in this expression is passed
            through ``kwargs``.
        :raises InvalidArgumentValueError: If no contraints are specified
            (i.e., ``kwargs`` is empty).
        :raises InvalidBooleanValueError: If any values from ``kwargs`` are not
            valid Boolean inputs.

        """
        if not kwargs:
            raise InvalidArgumentValueError(
                'Must specify at least one constraint')

        assert_all_valid_keys(kwargs, self._symbol_set)

        kwarg_key_set = set(kwargs.keys())
        conflicts = self._constrained_symbol_set & kwarg_key_set
        if conflicts:
            symbols_str = ', '.join('"{}"'.format(s) for s in
                                    sorted(conflicts))
            raise AlreadyConstrainedSymbolError(
                'Symbol' + (' ' if len(conflicts) == 1 else 's ') +
                symbols_str + ' cannot be constrained multiple times')

        self._constraints.update(kwargs)
        self._constrained_symbol_set |= kwarg_key_set
        yield self
        self._constrained_symbol_set -= kwarg_key_set
        self._constraints = {}

    def sat_one(self):
        """Find a combination of inputs that satisfies this expression.

        Under the hood, this method is using the functionality exposed in tt's
        :mod:`satisfiability.picosat <tt.satisfiability.picosat>` module.

        Here's a simple example of satisfying an expression::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A xor 1')
            >>> b.sat_one()
            <BooleanValues [A=0]>

        Don't forget about the utility provided by the :func:`constrain`
        context manager::

            >>> b = BooleanExpression('(A nand B) iff C')
            >>> with b.constrain(A=1, C=1):
            ...     b.sat_one()
            ...
            <BooleanValues [A=1, B=0, C=1]>

        Finally, here's an example when the expression cannot be satisfied::

            >>> with BooleanExpression('A xor 1').constrain(A=1) as b:
            ...     b.sat_one() is None
            ...
            True

        :returns: :func:`namedtuple <python:collections.namedtuple>`-like
            object representing a satisfying set of values (see
            :func:`boolean_variables_factory \
            <tt.definitions.operands.boolean_variables_factory>` for more
            information about the type of object returned); ``None``
            will be returned if no satisfiable set of inputs exists.
        :rtype: :func:`namedtuple <python:collections.namedtuple>`-like object
            or ``None``

        :raises NoEvaluationVariationError: If this is an expression of only
            constants.

        """
        if not self._symbols:
            raise NoEvaluationVariationError(
                'Cannot attempt to satisfy an expression of only constants')

        if not (self._symbol_set - self._constrained_symbol_set):
            # shortcut if all symbols are constrained
            if self.evaluate_unchecked(**self._constraints):
                return self._symbol_vals_factory(**self._constraints)
            else:
                return None

        clauses, assumptions, symbol_to_index_map, index_to_symbol_map = \
            self._to_picosat_clauses_assumptions_and_symbol_mappings()
        if not assumptions:
            # cannot pass empty list of assumptions to picosat
            assumptions = None

        picosat_result = picosat.sat_one(clauses, assumptions=assumptions)
        if picosat_result is None:
            return None

        result_dict = self._picosat_result_as_dict(
            picosat_result, symbol_to_index_map, index_to_symbol_map)
        return self._symbol_vals_factory(**result_dict)

    def sat_all(self):
        """Find all combinations of inputs that satisfy this expression.

        Under the hood, this method is using the functionality exposed in tt's
        :mod:`satisfiability.picosat <tt.satisfiability.picosat>` module.

        Here's a simple example of iterating through a few SAT solutions::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A xor B) and (C xor D)')
            >>> for solution in b.sat_all():
            ...     print(solution)
            ...
            A=0, B=1, C=0, D=1
            A=0, B=1, C=1, D=0
            A=1, B=0, C=1, D=0
            A=1, B=0, C=0, D=1

        We can also constrain away a few of those solutions::

            >>> with b.constrain(A=1, C=0):
            ...     for solution in b.sat_all():
            ...         print(solution)
            ...
            A=1, B=0, C=0, D=1

        :returns: An iterator of
            :func:`namedtuple <python:collections.namedtuple>`-like objects
            representing satisfying combinations of inputs; if no satisfying
            solutions exist, the iterator will be empty.
        :rtype: Iterator[:func:`namedtuple <python:collections.namedtuple>`
            -like objects]

        :raises NoEvaluationVariationError: If this is an expression of only
            constants.

        """
        if not self._symbols:
            raise NoEvaluationVariationError(
                'Cannot attempt to satisfy an expression of only constants')

        if not (self._symbol_set - self._constrained_symbol_set):
            # shortcut if all symbols are constrained
            if self.evaluate_unchecked(**self._constraints):
                yield self._symbol_vals_factory(**self._constraints)
            else:
                # empty iterator
                while False:
                    yield None
            return

        clauses, assumptions, symbol_to_index_map, index_to_symbol_map = \
            self._to_picosat_clauses_assumptions_and_symbol_mappings()
        if not assumptions:
            # cannot pass empty list of assumptions to picosat
            assumptions = None

        for picosat_sol in picosat.sat_all(clauses, assumptions=assumptions):
            result_dict = self._picosat_result_as_dict(
                picosat_sol, symbol_to_index_map, index_to_symbol_map)
            yield self._symbol_vals_factory(**result_dict)

    def _picosat_result_as_dict(self, results, symbol_to_index_map,
                                index_to_symbol_map):
        """Convert a PicoSAT result into a BooleanValues tuple."""
        result_dict = {}
        signed_symbol_indices = (index for index in results if abs(index) in
                                 index_to_symbol_map)
        for index in signed_symbol_indices:
            symbol_name = index_to_symbol_map[abs(index)]
            result_dict[symbol_name] = index > 0

        return result_dict

    def _to_picosat_clauses_assumptions_and_symbol_mappings(self):
        """Return a PicoSAT-compatible representation and helpful metadata."""
        cnf_tree = self.tree if self.is_cnf else self.tree.to_cnf()
        index = 1
        symbol_to_index_map = {}
        index_to_symbol_map = {}
        clauses = []
        assumptions = []

        for clause_root in cnf_tree.iter_cnf_clauses():
            clause_indices = []
            for node in clause_root.iter_dnf_clauses():
                is_negated = isinstance(node, UnaryOperatorExpressionTreeNode)
                symbol_str = (node.l_child.symbol_name if is_negated else
                              node.symbol_name)

                if symbol_str in symbol_to_index_map:
                    pos = symbol_to_index_map[symbol_str]
                    if is_negated:
                        clause_indices.append(-pos)
                    else:
                        clause_indices.append(pos)
                elif symbol_str == '0':
                    clause_indices.append(index)
                    if is_negated:
                        assumptions.append(index)
                    else:
                        assumptions.append(-index)
                    index += 1
                elif symbol_str == '1':
                    clause_indices.append(index)
                    if is_negated:
                        assumptions.append(-index)
                    else:
                        assumptions.append(index)
                    index += 1
                else:
                    symbol_to_index_map[symbol_str] = index
                    index_to_symbol_map[index] = symbol_str
                    if is_negated:
                        clause_indices.append(-index)
                    else:
                        clause_indices.append(index)
                    index += 1

            clauses.append(clause_indices)

        for symbol_str, assumed_val in self._constraints.items():
            index = symbol_to_index_map[symbol_str]
            if assumed_val:
                assumptions.append(index)
            else:
                assumptions.append(-index)

        return clauses, assumptions, symbol_to_index_map, index_to_symbol_map

    def evaluate(self, **kwargs):
        """Evaluate the Boolean expression for the passed keyword arguments.

        This is a checked wrapper around the :func:`evaluate_unchecked`
        function.

        :param kwargs: Keys are names of symbols in this expression; the
            specified value for each of these keys will be substituted into the
            expression for evaluation.

        :returns: The result of evaluating the expression.
        :rtype: :class:`bool <python:bool>`

        :raises ExtraSymbolError: If a symbol not in this expression is passed
            through ``kwargs``.
        :raises MissingSymbolError: If any symbols in this expression are not
            passed through ``kwargs``.
        :raises InvalidBooleanValueError: If any values from ``kwargs`` are not
            valid Boolean inputs.
        :raises InvalidIdentifierError: If any symbol names are invalid
            identifiers.

        Usage::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('A or B')
            >>> b.evaluate(A=0, B=0)
            False
            >>> b.evaluate(A=1, B=0)
            True

        """
        assert_all_valid_keys(kwargs, self._symbol_set)
        assert_iterable_contains_all_expr_symbols(
            kwargs.keys(), self._symbol_set)

        return self.evaluate_unchecked(**kwargs)

    def evaluate_unchecked(self, **kwargs):
        """Evaluate the Boolean expression without checking the input.

        This is used for evaluation by the :func:`evaluate` method, which
        validates the input ``kwargs`` before passing them to this method.

        :param kwargs: Keys are names of symbols in this expression; the
            specified value for each of these keys will be substituted into the
            expression for evaluation.

        :returns: The Boolean result of evaluating the expression.
        :rtype: :class:`bool <python:bool>`

        """
        truthy = self._tree.evaluate(kwargs)
        return bool(truthy)

    def iter_clauses(self):
        """Iterate over the clauses in this expression.

        An expression must be in conjunctive normal form (CNF) or disjunctive
        normal form (DNF) in order to iterate over its clauses. Here's a simple
        example::

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(~A or B) and (C or D) and (~E or ~F)')
            >>> for clause in b.iter_clauses():
            ...     clause
            ...
            <BooleanExpression "~A or B">
            <BooleanExpression "C or D">
            <BooleanExpression "~E or ~F">

        In the case of an ambiguous expression form (between CNF and DNF), the
        clauses will be interpreted to be in CNF form. For example::

            >>> b = BooleanExpression('A and ~B and C')
            >>> b.is_cnf
            True
            >>> b.is_dnf
            True
            >>> print(', '.join(str(clause) for clause in b.iter_clauses()))
            A, ~B, C

        If you want to enforce a specific CNF or DNF interpretation of the
        clauses, take a look at :func:`iter_cnf_clauses` and
        :func:`iter_dnf_clauses`.

        :returns: An iterator of expression objects, each representing a
            separate clause of this expression.
        :rtype: Iterator[:class:`BooleanExpression`]

        :raises RequiresNormalFormError: If this expression is not in
            conjunctive or disjunctive normal form.

        """
        for node in self._tree.iter_clauses():
            yield BooleanExpression(node)

    def iter_cnf_clauses(self):
        """Iterate over the CNF clauses in this expression.

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A or B) and ~C')
            >>> for clause in b.iter_cnf_clauses():
            ...     print(clause)
            ...
            A or B
            ~C

        :returns: An iterator of expression objects, each representing a
            separate CNF clause of this expression.
        :rtype: Iterator[:class:`BooleanExpression`]

        :raises RequiresNormalFormError: If this expression is not in
            conjunctive normal form.

        """
        for node in self._tree.iter_cnf_clauses():
            yield BooleanExpression(node)

    def iter_dnf_clauses(self):
        """Iterate over the DNF clauses in this expression.

        .. code-block:: python

            >>> from tt import BooleanExpression
            >>> b = BooleanExpression('(A and ~B) or (C and D and E)')
            >>> for clause in b.iter_dnf_clauses():
            ...     print(clause)
            ...
            A and ~B
            C and D and E

        :returns: An iterator of expression objects, each representing a
            separate DNF clause of this expression.
        :rtype: Iterator[:class:`BooleanExpression`]

        :raises RequiresNormalFormError: If this expression is not in
            disjunctive normal form.

        """
        for node in self._tree.iter_dnf_clauses():
            yield BooleanExpression(node)

    def _tokenize(self):
        """Make the first pass through the expression, tokenizing it.

        This method is a helper for initializing an expression object from a
        string and will populate the ``_symbols``, ``_symbol_set``, and
        ``_tokens`` attributes of this object.

        :raises GrammarError: If a malformed expression is received.

        """
        operator_strs = [k for k in OPERATOR_MAPPING.keys()]
        is_symbolic = {op: not op[0].isalpha() for op in operator_strs}
        operator_search_list = sorted(operator_strs, key=len, reverse=True)
        delimiters = DELIMITERS | set(k[0] for k, v in is_symbolic.items()
                                      if v)
        EXPECTING_OPERAND = 1
        EXPECTING_OPERATOR = 2
        grammar_state = EXPECTING_OPERAND

        idx = 0
        open_paren_count = 0
        num_chars = len(self._raw_expr)

        while idx < num_chars:
            c = self._raw_expr[idx].strip()

            if not c:
                # do nothing
                idx += 1
            elif c == '(':
                if grammar_state != EXPECTING_OPERAND:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self._raw_expr, idx)

                open_paren_count += 1
                self._tokens.append(c)
                idx += 1
            elif c == ')':
                if grammar_state != EXPECTING_OPERATOR:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self._raw_expr, idx)
                elif not open_paren_count:
                    raise UnbalancedParenError('Unbalanced parenthesis',
                                               self._raw_expr, idx)

                open_paren_count -= 1
                self._tokens.append(c)
                idx += 1
            else:
                is_operator = False
                num_chars_remaining = num_chars - idx

                matching_operators = [
                    operator for operator in operator_search_list
                    if len(operator) <= num_chars_remaining and
                    self._raw_expr[idx:(idx+len(operator))] == operator]

                if matching_operators:
                    match = matching_operators[0]
                    match_length = len(match)
                    next_c_pos = idx + match_length
                    next_c = (None if next_c_pos >= num_chars else
                              self._raw_expr[idx + match_length])

                    if next_c is None:
                        # trailing operator
                        raise ExpressionOrderError(
                            'Unexpected operator "{}"'.format(match),
                            self._raw_expr, idx)

                    if next_c in delimiters or is_symbolic[match]:
                        if OPERATOR_MAPPING[match] == TT_NOT_OP:
                            if grammar_state != EXPECTING_OPERAND:
                                raise ExpressionOrderError(
                                    'Unexpected unary operator "{}"'.format(
                                        match), self._raw_expr, idx)
                        else:
                            if grammar_state != EXPECTING_OPERATOR:
                                raise ExpressionOrderError(
                                    'Unexpected binary operator "{}"'.format(
                                        match), self._raw_expr, idx)
                            grammar_state = EXPECTING_OPERAND

                        is_operator = True
                        self._tokens.append(match)
                        idx += match_length

                if not is_operator:
                    if grammar_state != EXPECTING_OPERAND:
                        raise ExpressionOrderError('Unexpected operand',
                                                   self._raw_expr, idx)

                    operand_end_idx = idx + 1
                    while (operand_end_idx < num_chars and
                           self._raw_expr[operand_end_idx] not in delimiters):
                        operand_end_idx += 1

                    operand = self._raw_expr[idx:operand_end_idx]
                    if (operand not in CONSTANT_VALUES and
                            not is_valid_identifier(operand)):
                        raise InvalidIdentifierError(
                            'Invalid operand name "{}"'.format(operand),
                            self._raw_expr, idx)

                    self._tokens.append(operand)
                    if operand not in self._symbol_set:
                        self._symbols.append(operand)
                        self._symbol_set.add(operand)

                    idx = operand_end_idx
                    grammar_state = EXPECTING_OPERATOR

        if open_paren_count:
            left_paren_positions = [m.start() for m in
                                    re.finditer(r'\(', self._raw_expr)]
            raise UnbalancedParenError(
                'Unbalanced left parenthesis', self._raw_expr,
                left_paren_positions[open_paren_count-1])

        if not self._tokens:
            raise EmptyExpressionError('Empty expression is invalid')

    def _to_postfix(self):
        """Populate the ``_postfix_tokens`` attribute."""
        stack = []

        for token in self._tokens:
            if token in self._symbol_set:
                self._postfix_tokens.append(token)
            elif token == '(':
                stack.append(token)
            elif token in OPERATOR_MAPPING.keys():
                if not stack:
                    stack.append(token)
                else:
                    while (stack and stack[-1] != '(' and
                            OPERATOR_MAPPING[stack[-1]].precedence >
                            OPERATOR_MAPPING[token].precedence):
                        self._postfix_tokens.append(stack.pop())
                    stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    self._postfix_tokens.append(stack.pop())
                stack.pop()

        for token in reversed(stack):
            self._postfix_tokens.append(token)

    @contextmanager
    def _symbol_set_includes_constant_values(self):
        """Context manager to include CONSTANT_VALUES in _symbol_set."""
        self._symbol_set |= CONSTANT_VALUES
        yield
        self._symbol_set -= CONSTANT_VALUES
