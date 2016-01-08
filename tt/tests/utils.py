"""Utility methods/classes used in the testing pipeline.
"""

import sys
import unittest

from contextlib import contextmanager
from io import StringIO

from tt.core import main


# === stdout/stderr interaction ===============================================
@contextmanager
def redirected_stream(stream_name):
    orig_stream = getattr(sys, stream_name)
    setattr(sys, stream_name, StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stream)


# === Generalized test cases ==================================================
class FunctionalTestCase(unittest.TestCase):

    def functional_test_helper(self, cl_args=[],
                               expected_stdout='', expected_stderr=''):
        with redirected_stream('stdout') as _stdout:
            with redirected_stream('stderr') as _stderr:
                main(args=cl_args)
        self.assertEqual(expected_stdout, _stdout.getvalue())
        self.assertEqual(expected_stderr, _stderr.getvalue())
