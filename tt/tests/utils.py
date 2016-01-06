"""Utility methods/classes used in the testing pipeline.
"""

import sys
import unittest

from contextlib import contextmanager

from tt.core import main


class StreamReader():

    def __init__(self):
        self.content = ""

    def write(self, txt):
        self.content += str(txt)


@contextmanager
def redirected_stdout(new_target):
    old_stdout, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_stdout


@contextmanager
def redirected_stderr(new_target):
    old_stderr, sys.stderr = sys.stderr, new_target
    try:
        yield new_target
    finally:
        sys.stderr = old_stderr


class FunctionalTestCase(unittest.TestCase):

    def functional_test_helper(self,
                               cl_args=[],
                               expected_stdout='',
                               expected_stderr=''):
        stdout_reader = StreamReader()
        stderr_reader = StreamReader()

        with redirected_stdout(stdout_reader):
            with redirected_stderr(stderr_reader):
                main(cl_args)
                self.assertEqual(expected_stdout, stdout_reader.content)
                self.assertEqual(expected_stderr, stderr_reader.content)
