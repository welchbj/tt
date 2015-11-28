import unittest
from tt.eqtools import transform_eq_to_generic_schema

class TestTransformEqToGenericSchema(unittest.TestCase):

    def test_single_symbol_not_simple(self):
        logically_equivalent_eqs = ["F = NOT A",
                                    "F = not A",
                                    "F = ~A",
                                    "F = !A"]
        tt_schema_eq = "F=~A"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def test_single_symbol_not_with_whitespace(self):
        logically_equivalent_eqs = ["F    =   NOT  A",
                                    "F=NOT     A",
                                    "F=   not  A  ",
                                    "F  =    ~   A",
                                    "F =          not A",
                                    "F=~A",
                                    "F = !    A   ",
                                    "F =      !A"]
        tt_schema_eq = "F=~A"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def test_two_symbol_and_simple(self):
        logically_equivalent_eqs = ["F = A and B",
                                    "F = A AND B",
                                    "F = A & B",
                                    "F = A && B",
                                    "F = A /\\ B"]
        tt_schema_eq = "F=A&B"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def test_two_symbol_and_with_whitespaces(self):
        logically_equivalent_eqs = ["F=A and         B",
                                    "F =A         AND       B",
                                    "F =            A&B",
                                    "F=A&&            B",
                                    "F=A/\\B"]
        tt_schema_eq = "F=A&B"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def test_two_symbol_or_simple(self):
        logically_equivalent_eqs = ["F = A or B",
                                    "F = A OR B",
                                    "F = A | B",
                                    "F = A || B",
                                    "F = A \\/ B"]
        tt_schema_eq = "F=A|B"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def test_two_symbol_or_with_whitespaces(self):
        logically_equivalent_eqs = ["F= A     or              B",
                                    "F =    A OR    B",
                                    "F =               A|B",
                                    "F =A ||               B",
                                    "F =     A \\/       B"]
        tt_schema_eq = "F=A|B"
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(transformed_eq, tt_schema_eq)
    
    def dtest_three_symbol_eq_simple(self):
        pass
    
    def dtest_three_symbol_eq_with_parens(self):
        pass
    
    def dtest_three_symbol_eq_with_whitespaces(self):
        pass
    
    def dtest_four_symbol_eq_simple(self):
        pass
    
    def dtest_four_symbol_eq_with_parens(self):
        pass
    
    def dtest_four_symbol_eq_with_whitespaces(self):
        pass
    
if __name__ == "__main__":
    unittest.main()