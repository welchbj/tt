import unittest
from eqtools import transform_eq_to_generic_schema

class TestTransformEqToGenericSchema(unittest.TestCase):

    def transform_eq_to_generic_schema_helper(self, tt_schema_eq, logically_equivalent_eqs):
        for eq in logically_equivalent_eqs:
            transformed_eq = transform_eq_to_generic_schema(eq)
            self.assertEqual(tt_schema_eq, transformed_eq)

    # === No-throw tests ===============================================================================================
    def test_single_symbol_not_simple(self):
        tt_schema_eq = "F=1+A"
        logically_equivalent_eqs = ["F = NOT A",
                                    "F = not A",
                                    "F = ~A",
                                    "F = !A"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)
    
    def test_single_symbol_not_with_whitespace(self):
        tt_schema_eq = "F=1+A"
        logically_equivalent_eqs = ["F    =   NOT  A",
                                    "F=NOT     A",
                                    "F=   not  A  ",
                                    "F  =    ~   A",
                                    "F =          not A",
                                    "F=~A",
                                    "F = !    A   ",
                                    "F =      !A"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)
    
    def test_two_symbol_and_simple(self):
        tt_schema_eq = "F=A&B"
        logically_equivalent_eqs = ["F = A and B",
                                    "F = A AND B",
                                    "F = A & B",
                                    "F = A && B",
                                    "F = A /\\ B"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)
    
    def test_two_symbol_and_with_whitespaces(self):
        tt_schema_eq = "F=A&B"
        logically_equivalent_eqs = ["F=A and         B",
                                    "F =A         AND       B",
                                    "F =            A&B",
                                    "F=A&&            B",
                                    "F=A/\\B"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)

    def test_two_symbol_or_simple(self):
        tt_schema_eq = "F=A|B"
        logically_equivalent_eqs = ["F = A or B",
                                    "F = A OR B",
                                    "F = A | B",
                                    "F = A || B",
                                    "F = A \\/ B"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)
    
    def test_two_symbol_or_with_whitespaces(self):
        tt_schema_eq = "F=A|B"
        logically_equivalent_eqs = ["F= A     or              B",
                                    "F =    A OR    B",
                                    "F =               A|B",
                                    "F =A ||               B",
                                    "F =     A \\/       B"]
        self.transform_eq_to_generic_schema_helper(tt_schema_eq, logically_equivalent_eqs)
    
    # TODO: more tests

    # === Expect-throws tests ==========================================================================================

    # TODO: more tests

if __name__ == "__main__":
    unittest.main()