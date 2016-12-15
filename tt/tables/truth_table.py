"""Implementation of a truth table."""


class TruthTable(object):

    """A class represenitng a truth table.

    Attributes:
        expr (tt.expressions.BooleanExpression): The expression represented by
            this truth table.
        ordering (List[str], optional): An optional list of symbol names in the
            passed expression, specifying the order in which they should
            appear in the truth table (from left to right). If omitted, the
            ordering of the symbols will be consistent with the symbol's first
            occurrence in the passed expression.

    """

    def __init__(self, expr, ordering=None):
        self.expr = expr

    def __str__(self):
        pass
