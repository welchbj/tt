"""Core command-line interface for tt."""

import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from ..expressions import BooleanExpression
from .utils import print_err, print_info


__version__ = 0.4


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
        prog='tt',
        description=(
            'tt is a library and command-line utility written in Python for\n'
            'interacting with Boolean Algebra expressions. tt is open source\n'
            'software and released under the MIT License. Please use\n'
            '`tt --help` for more information.'),
        formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--version',
        action='version',
        version='v'+str(__version__),
        help='program version')

    parser.add_argument(
        '--tokens',
        action='store_true',
        dest='tokens',
        help='print the parsed tokens of the expression')

    parser.add_argument(
        '--postfix-tokens',
        action='store_true',
        dest='postfix_tokens',
        help='print the tokens of this expression in postfix form')

    parser.add_argument(
        'expression',
        nargs='*',
        help=(
            'Boolean expression to process; surround it in quotes to\n'
            'avoid escaping control characters in your terminal'))

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def main(args=None):
    """The main routine to run the tt command-line interface.

    Args:
        args (List[str], optional): The ``args`` argument to be passed to the
            ``get_parsed_args`` function.

    Returns:
        int: The exit code of the program.

    """
    try:
        if args is None:
            args = sys.argv[1:]

        opts = get_parsed_args(args)

        tokens = opts.tokens
        postfix_tokens = opts.postfix_tokens
        expression = ' '.join(opts.expression)

        b = BooleanExpression(expression)

        if tokens:
            print_info('\n'.join(b.tokens))

        if postfix_tokens:
            print_info('\n'.join(b.postfix_tokens))

        return 0
    except Exception as e:
        print_err('Received unexpected error; re-raising it!')
        raise e
