"""Tests for expression evaluation."""

from ._helpers import ExpressionTestCase
from ....definitions import BOOLEAN_VALUES


class TestBooleanExpressionEvaluation(ExpressionTestCase):

    def test_single_operand(self):
        """Test evaluating an expression of a single operand."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'operand',
                expected_result=val,
                operand=val)

    def test_negated_single_operand(self):
        """Test evaluating an expression of a single negated operand."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                '!operand',
                expected_result=int(not val),
                operand=val)

    def test_doubly_negated_single_operand(self):
        """Test evaluating an expression that is negated twice.."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'not not op',
                expected_result=val,
                op=val)

    def test_basic_xor(self):
        """Test a basic expression with the Boolean XOR operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A xor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_iff(self):
        """Test a basic expression with the Boolean IFF operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            for operator in ('iff', 'IFF', '<->'):
                self.helper_test_evaluate(
                    'A {} B'.format(operator),
                    expected_result=output,
                    A=inputs[0],
                    B=inputs[1])

    def test_basic_implies(self):
        """Test a basic expression with the Boolean IMPLIES operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 1,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            for operator in ('impl', 'IMPL', '->'):
                self.helper_test_evaluate(
                    'A {} B'.format(operator),
                    expected_result=output,
                    A=inputs[0],
                    B=inputs[1])

    def test_basic_xnor(self):
        """Test a basic expression with the Boolean XNOR operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A xnor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_and(self):
        """Test a basic expression with the Boolean AND operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A and B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_nand(self):
        """Test a basic expression with the Boolean NAND operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A nand B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_or(self):
        """Test a basic expression with the Boolean OR operator."""
        cases = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 1
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A or B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_basic_nor(self):
        """Test a basic expression with the Boolean NOR operator."""
        cases = {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 0
        }

        for inputs, output in cases.items():
            self.helper_test_evaluate(
                'A nor B',
                expected_result=output,
                A=inputs[0],
                B=inputs[1])

    def test_single_constant_value(self):
        """Test an expression of only a single constant value."""
        self.helper_test_evaluate(
            '0',
            expected_result=0)

        self.helper_test_evaluate(
            '1',
            expected_result=1)

    def test_several_constant_values(self):
        """Test an expression of several constant values."""
        self.helper_test_evaluate(
            '(1 xor (0 or 1)) and 1',
            expected_result=0)

    def test_simple_mixed_constant_variable(self):
        """Test a simple expression mixing constant values and variables."""
        for val in BOOLEAN_VALUES:
            self.helper_test_evaluate(
                'operand xnor 1',
                expected_result=int(val == 1),
                operand=val)

            self.helper_test_evaluate(
                'operand xnor 0',
                expected_result=int(val == 0),
                operand=val)

    def test_mixed_constant_variable(self):
        """Test a non-trivial mix of constant values and variables."""
        self.helper_test_evaluate(
            '(A or (not(A and B) nand C)) and 1',
            expected_result=1,
            A=0,
            B=1,
            C=0)
