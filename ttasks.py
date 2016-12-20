"""Script for performing common tasks for the tt project."""

from __future__ import print_function

import os
import sys
import unittest

from argparse import ArgumentParser, RawTextHelpFormatter


HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(HERE, 'docs')
TT_DIR = os.path.join(HERE, 'tt')
TESTS_DIR = os.path.join(TT_DIR, 'tests')


class TestFailureError(Exception):
    """An exception type for failed tests."""


def test():
    """Run tt tests."""
    suite = unittest.defaultTestLoader.discover(
        TESTS_DIR,
        pattern='test_*.py',
        top_level_dir=HERE)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise TestFailureError


TASKS = {
    'test': test
}


def get_parsed_args(args=None):
    """Get the parsed command line arguments.

    Args:
        args (List[str], optional): The list of command line args to parse;
            if left as None, sys.argv will be used.

    Returns:
        argparse.Namespace: The Namespace object returned by the
            ``ArgumentParser.parse_args`` function.

    """
    parser = ArgumentParser(
        prog='ttasks.py',
        description='Helper script for running tt project tasks (ttasks)',
        formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        'task',
        action='store',
        metavar='TASK',
        type=str,
        choices=sorted(TASKS.keys()),
        help='the ttask to run')

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def main(args=None):
    """Main routine for running this script.

    Args:
        args (List[str], optional): The ``args`` argument to be passed to the
            ``get_parsed_args`` function.

    Returns:
        int: The exit code of the program.

    """
    try:
        opts = get_parsed_args()
        task = TASKS[opts.task]
        task()
        return 0
    except TestFailureError:
        return 1
    except Exception as e:
        print('Received unexpected exception; re-raising it.', file=sys.stderr)
        raise e


if __name__ == '__main__':
    sys.exit(main())
