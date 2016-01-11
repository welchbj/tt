"""Utility methods/classes used in the testing pipeline.
"""

import sys
import unittest

from contextlib import contextmanager

from tt.core import main

if sys.version_info < (3, 0):
    from io import BytesIO as StringIO
else:
    from io import StringIO


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
class FunctionalTestAssertions(object):
    pass


class FunctionalTestCase(unittest.TestCase):

    def functional_test_helper(self, cl_args=[],
                               expected_stdout='', expected_stderr=''):
        with redirected_stream('stdout') as _stdout:
            with redirected_stream('stderr') as _stderr:
                main(args=cl_args)
        self.assertEqual(expected_stdout, _stdout.getvalue())
        self.assertEqual(expected_stderr, _stderr.getvalue())
