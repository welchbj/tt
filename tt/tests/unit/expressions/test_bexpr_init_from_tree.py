"""Test expression initialization from expression trees."""

import unittest

from tt.expressions import BooleanExpression
from tt.trees import BooleanExpressionTree


class TestBooleanExpressionInitFromTrees(unittest.TestCase):

    def _bexpr_from_postfix_tokens(self, postfix_tokens):
        return BooleanExpression(BooleanExpressionTree(postfix_tokens))

    def test_single_operand(self):
        """Test from a single operand tree."""
        for token in ('0', '1', 'operand'):
            b = self._bexpr_from_postfix_tokens([token])
            self.assertEqual(b.symbols, [] if token in {'0', '1'} else [token])
            self.assertEqual(b.tokens, [token])
            self.assertEqual(b.postfix_tokens, [token])
            self.assertEqual(b.raw_expr, token)
            self.assertTrue(b.tree is not None)

    def test_only_symbolic_unary_operators(self):
        """Test from trees containing only symbol unary operators."""
        b = self._bexpr_from_postfix_tokens(['A', '~'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['~', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', '~'])
        self.assertEqual(b.raw_expr, '~A')
        self.assertTrue(b.tree is not None)

        b = self._bexpr_from_postfix_tokens(['A', '~', '~'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['~', '~', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', '~', '~'])
        self.assertEqual(b.raw_expr, '~~A')
        self.assertTrue(b.tree is not None)

        b = self._bexpr_from_postfix_tokens(['A', '~', '~', '~'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['~', '~', '~', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', '~', '~', '~'])
        self.assertEqual(b.raw_expr, '~~~A')
        self.assertTrue(b.tree is not None)

    def test_only_plain_english_symbolic_unary_operators(self):
        """Test from trees containing only plain-English unary operators."""
        b = self._bexpr_from_postfix_tokens(['A', 'not'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['not', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', 'not'])
        self.assertEqual(b.raw_expr, 'not A')
        self.assertTrue(b.tree is not None)

        b = self._bexpr_from_postfix_tokens(['A', 'not', 'not'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['not', 'not', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', 'not', 'not'])
        self.assertEqual(b.raw_expr, 'not not A')
        self.assertTrue(b.tree is not None)

        b = self._bexpr_from_postfix_tokens(['A', 'not', 'not', 'not'])
        self.assertEqual(b.symbols, ['A'])
        self.assertEqual(b.tokens, ['not', 'not', 'not', 'A'])
        self.assertEqual(b.postfix_tokens, ['A', 'not', 'not', 'not'])
        self.assertEqual(b.raw_expr, 'not not not A')
        self.assertTrue(b.tree is not None)

    def test_unary_operator_applied_to_binary_operator(self):
        """Test applying a unary operator to exprs of binary operators."""
        b = self._bexpr_from_postfix_tokens(['A', 'B', '&', 'not'])
        self.assertEqual(b.symbols, ['A', 'B'])
        self.assertEqual(b.tokens, ['not', '(', 'A', '&', 'B', ')'])
        self.assertEqual(b.postfix_tokens, ['A', 'B', '&', 'not'])
        self.assertEqual(b.raw_expr, 'not (A & B)')
        self.assertTrue(b.tree is not None)

        b = self._bexpr_from_postfix_tokens(['A', 'B', '&', '~'])
        self.assertEqual(b.symbols, ['A', 'B'])
        self.assertEqual(b.tokens, ['~', '(', 'A', '&', 'B', ')'])
        self.assertEqual(b.postfix_tokens, ['A', 'B', '&', '~'])
        self.assertEqual(b.raw_expr, '~(A & B)')
        self.assertTrue(b.tree is not None)

    def test_negated_single_operand_clauses(self):
        """Test single-operand clauses that are negated several times."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'not', 'not', 'not', 'not',
             'B', '!',
             'C',
             'D', '~', '~',
             'or', 'or', 'or'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D'])
        self.assertEqual(
            b.tokens,
            ['not', 'not', 'not', 'not', 'A', 'or', '!', 'B', 'or', 'C', 'or',
             '~', '~', 'D'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'not', 'not', 'not', 'not',
             'B', '!',
             'C',
             'D', '~', '~',
             'or', 'or', 'or'])
        self.assertEqual(b.raw_expr, 'not not not not A or !B or C or ~~D')
        self.assertTrue(b.tree is not None)

    def test_parens_for_leading_chained_operator_clause(self):
        """Test paren insertion for a leading clause of chained operators."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'B', 'C', 'D', 'and', 'and', 'and',
             'E',
             'or'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['(', 'A', 'and', 'B', 'and', 'C', 'and', 'D', ')', 'or', 'E'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'B', 'C', 'D', 'and', 'and', 'and',
             'E',
             'or'])
        self.assertEqual(
            b.raw_expr,
            '(A and B and C and D) or E')
        self.assertTrue(b.tree is not None)

    def test_parens_for_trailing_chained_operator_clause(self):
        """Test paren insertion for a trailing clause of chained operators."""
        b = self._bexpr_from_postfix_tokens(
            ['A',
             'B', 'C', 'or',
             'D', 'E', 'F', 'or', 'or',
             'and', 'and'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E', 'F'])
        self.assertEqual(
            b.tokens,
            ['A', 'and', '(', 'B', 'or', 'C', ')', 'and',
             '(', 'D', 'or', 'E', 'or', 'F', ')'])
        self.assertEqual(
            b.postfix_tokens,
            ['A',
             'B', 'C', 'or',
             'D', 'E', 'F', 'or', 'or',
             'and', 'and'])
        self.assertEqual(b.raw_expr, 'A and (B or C) and (D or E or F)')
        self.assertTrue(b.tree is not None)

    def test_parens_for_sandwiched_chained_operator_clause(self):
        """Test paren insertion for a clause in the middle of an expression."""
        b = self._bexpr_from_postfix_tokens(
            ['A',
             'B', 'C', 'D', '&', '&',
             'E',
             '->', '->'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['A', '->', '(', 'B', '&', 'C', '&', 'D', ')', '->', 'E'])
        self.assertEqual(
            b.postfix_tokens,
            ['A',
             'B', 'C', 'D', '&', '&',
             'E',
             '->', '->'])
        self.assertEqual(b.raw_expr, 'A -> (B & C & D) -> E')
        self.assertTrue(b.tree is not None)

    def test_parens_for_negated_leading_chained_operator_clause(self):
        """Test paren insertion for negated leading clause."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'B', 'iff', '!',
             '0', '1', 'and',
             'and'])
        self.assertEqual(
            b.symbols,
            ['A', 'B'])
        self.assertEqual(
            b.tokens,
            ['!', '(', 'A', 'iff', 'B', ')', 'and', '0', 'and', '1'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'B', 'iff', '!',
             '0', '1', 'and',
             'and'])
        self.assertEqual(b.raw_expr, '!(A iff B) and 0 and 1')
        self.assertTrue(b.tree is not None)

    def test_parens_for_sandwiched_negated_chained_operator_clause(self):
        """Test paren insertion for negated sandwiched clause."""
        b = self._bexpr_from_postfix_tokens(
            ['A',
             'B', 'C', 'D', 'xor', 'xor', '~',
             'E',
             '->', '->'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['A', '->', '~', '(', 'B', 'xor', 'C', 'xor', 'D', ')', '->', 'E'])
        self.assertEqual(
            b.postfix_tokens,
            ['A',
             'B', 'C', 'D', 'xor', 'xor', '~',
             'E',
             '->', '->'])
        self.assertEqual(b.raw_expr, 'A -> ~(B xor C xor D) -> E')
        self.assertTrue(b.tree is not None)

    def test_parens_for_trailing_negated_chained_operator_clause(self):
        """Test paren insertion for negated trailing clause."""
        b = self._bexpr_from_postfix_tokens(
            ['A',
             'B',
             'C', 'D', 'E', 'and', 'and', 'not',
             'xnor', 'xnor'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['A', 'xnor', 'B', 'xnor',
             'not', '(', 'C', 'and', 'D', 'and', 'E', ')'])
        self.assertEqual(
            b.postfix_tokens,
            ['A',
             'B',
             'C', 'D', 'E', 'and', 'and', 'not',
             'xnor', 'xnor'])
        self.assertEqual(b.raw_expr, 'A xnor B xnor not (C and D and E)')
        self.assertTrue(b.tree is not None)

    def test_multiple_negated_chained_clauses(self):
        """Test clauses that are negated multiple times."""
        b = self._bexpr_from_postfix_tokens(
            ['A', '~', '~', '~',
             'B', 'C', 'D', '&', '&', '~', '~',
             'E', '~',
             '->', '->'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['~', '~', '~', 'A', '->',
             '~', '~', '(', 'B', '&', 'C', '&', 'D', ')', '->',
             '~', 'E'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', '~', '~', '~',
             'B', 'C', 'D', '&', '&', '~', '~',
             'E', '~',
             '->', '->'])
        self.assertEqual(b.raw_expr, '~~~A -> ~~(B & C & D) -> ~E')
        self.assertTrue(b.tree is not None)

    def test_parens_for_nested_chained_clause(self):
        """Test paren insertion for nested chained clauses."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'B', 'C', 'D', '->', '->', 'E', 'nand', 'xor', '~',
             'A', 'B', 'xor', '~', 'A', 'B', 'xnor', '!', 'C', 'or', 'nand',
             'iff'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['~', '(', 'A', 'xor', '(', '(', 'B', '->', 'C', '->', 'D', ')',
             'nand', 'E', ')', ')', 'iff', '(', '~', '(', 'A', 'xor', 'B', ')',
             'nand', '(', '!', '(', 'A', 'xnor', 'B', ')', 'or', 'C', ')',
             ')'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'B', 'C', 'D', '->', '->', 'E', 'nand', 'xor', '~',
             'A', 'B', 'xor', '~', 'A', 'B', 'xnor', '!', 'C', 'or', 'nand',
             'iff'])
        self.assertEqual(
            b.raw_expr,
            '~(A xor ((B -> C -> D) nand E)) iff (~(A xor B) nand '
            '(!(A xnor B) or C))')
        self.assertTrue(b.tree is not None)

    def test_parens_for_leading_single_operand_same_op_as_next(self):
        """Parens are omitted for a leading op the same as the next clause."""
        b = self._bexpr_from_postfix_tokens(
            ['A',
             'B', 'C', 'and',
             'and'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C'])
        self.assertEqual(
            b.tokens,
            ['A', 'and', 'B', 'and', 'C'])
        self.assertEqual(
            b.postfix_tokens,
            ['A',
             'B', 'C', 'and',
             'and'])
        self.assertEqual(
            b.raw_expr,
            'A and B and C')
        self.assertTrue(b.tree is not None)

    def test_parens_for_trailing_single_operand_same_op_as_prev(self):
        """Parens are omitted for a trailing op the same as the prev clause."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'B', 'and',
             'C',
             'and'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C'])
        self.assertEqual(
            b.tokens,
            ['A', 'and', 'B', 'and', 'C'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'B', 'and',
             'C',
             'and'])
        self.assertEqual(
            b.raw_expr,
            'A and B and C')
        self.assertTrue(b.tree is not None)

    def test_parens_for_sandwiched_single_operand_same_op_as_neighbors(self):
        """Parens are omitted for an op the same as the adjacent clauses."""
        b = self._bexpr_from_postfix_tokens(
            ['A', 'B', 'and',
             'C',
             'D', 'E', 'and',
             'and', 'and'])
        self.assertEqual(
            b.symbols,
            ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(
            b.tokens,
            ['A', 'and', 'B', 'and', 'C', 'and', 'D', 'and', 'E'])
        self.assertEqual(
            b.postfix_tokens,
            ['A', 'B', 'and',
             'C',
             'D', 'E', 'and',
             'and', 'and'])
        self.assertEqual(
            b.raw_expr,
            'A and B and C and D and E')
        self.assertTrue(b.tree is not None)
