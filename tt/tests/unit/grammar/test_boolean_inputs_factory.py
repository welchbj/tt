"""Tests for boolean_inputs_factory method."""

import unittest

from ....definitions import boolean_variables_factory


class TestBooleanInputsFactory(unittest.TestCase):

    def test_str_methods(self):
        """Test converting to string via __str__ and __repr__."""
        factory = boolean_variables_factory(['A', 'B', 'C', 'D'])
        instance = factory(A=1, B=False, C=True, D=0)
        self.assertEqual(str(instance), 'A=1, B=0, C=1, D=0')
        self.assertEqual(repr(instance),
                         '<BooleanValues [A=1, B=0, C=1, D=0]>')

    def test_attr_access(self):
        """Test attribute access."""
        factory = boolean_variables_factory(['op1', 'op2', 'op3'])
        instance = factory(op1=1, op2=False, op3=True)
        self.assertEqual(instance.op1, 1)
        self.assertEqual(instance.op2, False)
        self.assertEqual(instance.op3, True)
