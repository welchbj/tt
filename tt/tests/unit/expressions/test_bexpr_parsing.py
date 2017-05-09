"""Tests for parsing/tokenization of well-formed expressions."""

from ._helpers import ExpressionTestCase
from ....definitions import OPERATOR_MAPPING, TT_NOT_OP


class TestBooleanExpressionParsing(ExpressionTestCase):

    def test_all_binary_operators(self):
        """Basic test for all binary operators, to ensure correct parsing."""
        binary_ops = [k for k, v in OPERATOR_MAPPING.items() if v != TT_NOT_OP]

        for op in binary_ops:
            self.helper_test_tokenization(
                '(A {0} ((B {0} C) {0} D)) {0} E'.format(op),
                expected_tokens=['(', 'A', op, '(', '(', 'B', op, 'C', ')', op,
                                 'D', ')', ')', op, 'E'],
                expected_postfix_tokens=['A', 'B', 'C', op, 'D', op, op, 'E',
                                         op],
                expected_symbols=['A', 'B', 'C', 'D', 'E'],
                expected_tree_str='\n'.join((
                    op,
                    '`----{}'.format(op),
                    '|    `----A',
                    '|    `----{}'.format(op),
                    '|         `----{}'.format(op),
                    '|         |    `----B',
                    '|         |    `----C',
                    '|         `----D',
                    '`----E')))

    def test_single_symbol(self):
        """Test an expression of a single variable."""
        self.helper_test_tokenization(
            'operand',
            expected_tokens=['operand'],
            expected_postfix_tokens=['operand'],
            expected_symbols=['operand'],
            expected_tree_str=(
                'operand'))

    def test_single_character_symbol(self):
        """Test an expression containing only an operand of one character."""
        self.helper_test_tokenization(
            'a',
            expected_tokens=['a'],
            expected_postfix_tokens=['a'],
            expected_symbols=['a'],
            expected_tree_str=(
                'a'))

    def test_single_constant(self):
        """Test an expression only containing a constant."""
        self.helper_test_tokenization(
            '0',
            expected_tokens=['0'],
            expected_postfix_tokens=['0'],
            expected_symbols=[],
            expected_tree_str=(
                '0'))

    def test_only_constants_symbolic_operators(self):
        """Test an expression of only constants and symbolic operators."""
        self.helper_test_tokenization(
            '1->((!0&&1||(~~0||~~1))&&((0\\/1)/\\!0))',
            expected_tokens=[
                '1', '->', '(', '(', '!', '0', '&&', '1', '||', '(', '~', '~',
                '0', '||', '~', '~', '1', ')', ')', '&&', '(', '(', '0', '\\/',
                '1', ')', '/\\', '!', '0', ')', ')'],
            expected_postfix_tokens=[
                '1', '0', '!', '1', '&&', '0', '~', '~', '1', '~', '~', '||',
                '||', '0', '1', '\\/', '0', '!', '/\\', '&&', '->'],
            expected_symbols=[],
            expected_tree_str='\n'.join((
                '->',
                '`----1',
                '`----&&',
                '     `----||',
                '     |    `----&&',
                '     |    |    `----!',
                '     |    |    |    `----0',
                '     |    |    `----1',
                '     |    `----||',
                '     |         `----~',
                '     |         |    `----~',
                '     |         |         `----0',
                '     |         `----~',
                '     |              `----~',
                '     |                   `----1',
                '     `----/\\',
                '          `----\\/',
                '          |    `----0',
                '          |    `----1',
                '          `----!',
                '               `----0')))

    def test_only_constants_plain_english_operators(self):
        """Test an expression of only constants and plain English operators."""
        self.helper_test_tokenization(
            'not 0 and 1 or (not not 0 or not not 1) and 0 or 1 and 0',
            expected_tokens=['not', '0', 'and', '1', 'or', '(', 'not', 'not',
                             '0', 'or', 'not', 'not', '1', ')', 'and', '0',
                             'or', '1', 'and', '0'],
            expected_postfix_tokens=['0', 'not', '1', 'and', '0', 'not', 'not',
                                     '1', 'not', 'not', 'or', '0', 'and', '1',
                                     '0', 'and', 'or', 'or'],
            expected_symbols=[],
            expected_tree_str='\n'.join((
                'or',
                '`----and',
                '|    `----not',
                '|    |    `----0',
                '|    `----1',
                '`----or',
                '     `----and',
                '     |    `----or',
                '     |    |    `----not',
                '     |    |    |    `----not',
                '     |    |    |         `----0',
                '     |    |    `----not',
                '     |    |         `----not',
                '     |    |              `----1',
                '     |    `----0',
                '     `----and',
                '          `----1',
                '          `----0')))

    def test_many_symbolic_impl_iff(self):
        """Test a combination of many <-> and -> symbolic operators."""
        self.helper_test_tokenization(
            'A->B<->C->(D->(E<->F))<->G',
            expected_tokens=[
                'A', '->', 'B', '<->', 'C', '->', '(', 'D', '->', '(', 'E',
                '<->', 'F', ')', ')', '<->', 'G'],
            expected_postfix_tokens=[
                'A', 'B', 'C', 'D', 'E', 'F', '<->', '->', 'G', '<->', '->',
                '<->', '->'],
            expected_symbols=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            expected_tree_str='\n'.join((
                '->',
                '`----A',
                '`----<->',
                '     `----B',
                '     `----->',
                '          `----C',
                '          `----<->',
                '               `----->',
                '               |    `----D',
                '               |    `----<->',
                '               |         `----E',
                '               |         `----F',
                '               `----G')))

    def test_superfluous_parentheses_symbolic_operators(self):
        """Test symbolic operators with unnecessary parentheses."""
        self.helper_test_tokenization(
            '((A)||(B))&&(C)',
            expected_tokens=['(', '(', 'A', ')', '||', '(', 'B', ')', ')',
                             '&&', '(', 'C', ')'],
            expected_postfix_tokens=['A', 'B', '||', 'C', '&&'],
            expected_symbols=['A', 'B', 'C'],
            expected_tree_str='\n'.join((
                '&&',
                '`----||',
                '|    `----A',
                '|    `----B',
                '`----C')))

    def test_superfluous_parentheses_plain_english_operators(self):
        """Test plain English operators with unnecessary parentheses."""
        self.helper_test_tokenization(
            '((A)and(B))or(C)',
            expected_tokens=['(', '(', 'A', ')', 'and', '(', 'B', ')', ')',
                             'or', '(', 'C', ')'],
            expected_postfix_tokens=['A', 'B', 'and', 'C', 'or'],
            expected_symbols=['A', 'B', 'C'],
            expected_tree_str='\n'.join((
                'or',
                '`----and',
                '|    `----A',
                '|    `----B',
                '`----C')))

    def test_symbolic_operators_without_spaces(self):
        """Test using symbolic operators without spaces before operands."""
        self.helper_test_tokenization(
            '(A&&B||(C&D))|(!E\\/(~F))',
            expected_tokens=['(', 'A', '&&', 'B', '||', '(', 'C', '&', 'D',
                             ')', ')', '|', '(', '!', 'E', '\\/', '(', '~',
                             'F', ')', ')'],
            expected_postfix_tokens=['A', 'B', '&&', 'C', 'D', '&', '||', 'E',
                                     '!', 'F', '~', '\\/', '|'],
            expected_symbols=['A', 'B', 'C', 'D', 'E', 'F'],
            expected_tree_str='\n'.join((
                '|',
                '`----||',
                '|    `----&&',
                '|    |    `----A',
                '|    |    `----B',
                '|    `----&',
                '|         `----C',
                '|         `----D',
                '`----\\/',
                '     `----!',
                '     |    `----E',
                '     `----~',
                '          `----F')))

    def test_several_nots(self):
        """Test several consecutive unary not operators."""
        self.helper_test_tokenization(
            '~!~!! not not ~ !!!! operand',
            expected_tokens=['~', '!', '~', '!', '!', 'not', 'not', '~', '!',
                             '!', '!', '!', 'operand'],
            expected_postfix_tokens=['operand', '!', '!', '!', '!', '~', 'not',
                                     'not', '!', '!', '~', '!', '~'],
            expected_symbols=['operand'],
            expected_tree_str='\n'.join((
                '~',
                '`----!',
                '     `----~',
                '          `----!',
                '               `----!',
                '                    `----not',
                '                         `----not',
                '                              `----~',
                '                                   `----!',
                '                                        `----!',
                '                                             `----!',
                '                                                  `----!',
                '                                                       `----operand')))  # noqa

    def test_concentric_parentheses(self):
        """Test many grouped parentheses."""
        self.helper_test_tokenization(
            '(((op1)))and(((((op2)))))or(1)',
            expected_tokens=['(', '(', '(', 'op1', ')', ')', ')', 'and',
                             '(', '(', '(', '(', '(', 'op2', ')', ')', ')',
                             ')', ')', 'or', '(', '1', ')'],
            expected_postfix_tokens=['op1', 'op2', 'and', '1', 'or'],
            expected_symbols=['op1', 'op2'],
            expected_tree_str='\n'.join((
                'or',
                '`----and',
                '|    `----op1',
                '|    `----op2',
                '`----1')))
