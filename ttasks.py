"""Script for performing common tasks for the tt project."""

from __future__ import print_function

import doctest
import os
import subprocess
import sys
import tt
import unittest

from argparse import ArgumentParser, RawTextHelpFormatter
from contextlib import contextmanager
from livereload import Server


HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(HERE, 'docs')
TT_DIR = os.path.join(HERE, 'tt')
TESTS_DIR = os.path.join(TT_DIR, 'tests')


class SubprocessFailureError(Exception):
    """An exception type for a subprocess exiting with a non-zero exit code."""


class TestFailureError(Exception):
    """An exception type for failed tests."""


@contextmanager
def _cwd(new_cwd):
    """Context manager for temporarily changing the cwd."""
    old_cwd = os.getcwd()
    os.chdir(new_cwd)
    yield
    os.chdir(old_cwd)


def _print_py_version():
    """Print a formatted notice of the current Python version to stdout."""
    v_info = sys.version_info
    v_maj, v_min, v_mic = v_info.major, v_info.minor, v_info.micro
    py_version = '.'.join(str(i) for i in (v_maj, v_min, v_mic))

    info_str = '| Running tests with Python version ' + py_version + ' |'
    num_dashes = len(info_str) - 2
    box_top = '+' + '-' * num_dashes + '+'

    print()
    print(box_top)
    print(info_str)
    print(box_top)
    print()


def build_docs():
    """Build the documentation from source into HTML."""
    with _cwd(DOCS_DIR):
        exit_code = subprocess.call('make html', shell=True)

    if exit_code:
        print('Something went wrong building the docs', file=sys.stderr)
        raise SubprocessFailureError


def serve_docs():
    """Serve the documentation on a local livereload server."""
    server = Server()

    watch_patterns = ['docs/**/*.rst', 'tt/**/*.py']
    for pattern in watch_patterns:
        server.watch(pattern, build_docs)

    server.serve(root='docs/_build/html', host='127.0.0.1', port=5000)


def test():
    """Run tt tests."""
    _print_py_version()

    suite = unittest.defaultTestLoader.discover(
        TESTS_DIR,
        pattern='test_*.py',
        top_level_dir=HERE)

    doctest_modules = [
        tt.definitions.operators,
        tt.expressions.bexpr,
        tt.errors.evaluation,
        tt.errors.generic,
        tt.errors.grammar,
        tt.tables.truth_table,
        tt.trees.expr_tree,  # TODO: doctests for this module
        tt.trees.tree_node,  # TODO: doctests for this module
        tt.utils.assertions  # TODO: doctests for this module
    ]

    for module in doctest_modules:
        suite.addTests(doctest.DocTestSuite(module))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise TestFailureError


TASKS = {
    'build-docs': build_docs,
    'serve-docs': serve_docs,
    'test': test
}


def get_parsed_args(args=None):
    """Get the parsed command line arguments.

    :param args: The command-line args to parse; if omitted,
        :data:`sys.argv <python:sys.argv>` will be used.
    :type args: List[:class:`str <python:str>`], optional

    :return: The :class:`Namespace <python:argparse.Namespace>` object holding
        the parsed args.
    :rtype: :class:`argparse.Namespace <python:argparse.Namespace>`

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

    :param args: The command-line arguments.
    :type args: List[:class:`str <python:str>`], optional

    :returns: The exit code of the program.
    :rtype: :class:`int <python:int>`

    """
    try:
        opts = get_parsed_args()
        task = TASKS[opts.task]
        task()
        return 0
    except (SubprocessFailureError, TestFailureError):
        return 1
    except Exception as e:
        print('Received unexpected exception; re-raising it.', file=sys.stderr)
        raise e


if __name__ == '__main__':
    sys.exit(main())
