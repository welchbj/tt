import unittest

import tt.fmttools.ttfmt as ttfmt

class TestTtFmt(unittest.TestCase):

    def test_get_vars(self):
        data_provider = {
                         # Simple test cases
                         "F = A and B" : ["F", "A", "B"],
                         "F = A and B or C" : ["F", "A", "B", "C"],
                         }
        
        for eq in data_provider:
            self.assertListEqual(data_provider[eq], ttfmt.get_vars(eq))

if __name__ == "__main__":
    unittest.main()