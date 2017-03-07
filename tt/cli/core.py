"""Core command-line interface for tt."""

import argparse
import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from ..errors import GrammarError
from ..expressions import BooleanExpression
from ..tables import TruthTable
from ..version import __version__
from .utils import print_err, print_info

from typing import List


def _add_expression_arg(parser: ArgumentParser) -> None:
    """Add the expression argument to a parser."""
    parser.add_argument(
        'expression',
        nargs='*',
        help='Boolean expression to process; surround it in quotes to\n'
             'avoid escaping control characters in your terminal')


def _tokens(opts: argparse.Namespace) -> None:
    """Run the `tokens` command."""
    b = BooleanExpression(opts.expression)
    print_info('\n'.join(b.tokens))


def _postfix_tokens(opts: argparse.Namespace) -> None:
    """Run the `postfix-tokens` command."""
    b = BooleanExpression(opts.expression)
    print_info('\n'.join(b.postfix_tokens))


def _tree(opts: argparse.Namespace) -> None:
    """Run the `tree` command."""
    b = BooleanExpression(opts.expression)
    print_info(b.tree)


def _table(opts: argparse.Namespace) -> None:
    """Run the `table` command."""
    t = TruthTable(opts.expression)
    print_info(t)


def get_parsed_args(args: List[str]=None) -> argparse.Namespace:
    """Get the parsed command line arguments.

    Args:
        args: The command line args to parse; if ommitted, ``sys.argv``
            will be used.

    Returns:
        The ``Namespace`` object indicating the parsed arguments.

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

    sub_parsers = parser.add_subparsers(help='the tt command to run')

    # tokens sub-parser
    parser_tokens = sub_parsers.add_parser(
        'tokens',
        help='print the expression\'s tokens in order of appearance')
    _add_expression_arg(parser_tokens)
    parser_tokens.set_defaults(func=_tokens)

    # postfix-tokens sub-parser
    parser_postfix_tokens = sub_parsers.add_parser(
        'postfix-tokens',
        help='print the expression\'s tokens in postfix order')
    _add_expression_arg(parser_postfix_tokens)
    parser_postfix_tokens.set_defaults(func=_postfix_tokens)

    # tree sub-parser
    parser_tree = sub_parsers.add_parser(
        'tree',
        help='print the expression\'s tree representation')
    _add_expression_arg(parser_tree)
    parser_tree.set_defaults(func=_tree)

    # table sub-parser
    parser_table = sub_parsers.add_parser(
        'table',
        help='print the expression\'s truth table')
    _add_expression_arg(parser_table)
    parser_table.set_defaults(func=_table)

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def main(args: List[str]=None) -> int:
    """The main routine to run the tt command-line interface.

    Args:
        args: The command-line arguments.

    Returns:
        The exit code of the program.

    """
    try:
        if args is None:
            args = sys.argv[1:]

        opts = get_parsed_args(args)
        func = getattr(opts, 'func', None)
        if func is None:
            print_err('No command specified; use `tt --help` for options.')
            return 2

        expr = opts.expression
        setattr(opts, 'expression', ' '.join(expr))
        func(opts)

        return 0
    except GrammarError as e:
        print_err('Error! ', e.message, ':', sep='')
        print_err(e.expr_str)
        print_err(' ' * e.error_pos, '^', sep='')
        return 1
    except Exception as e:
        print_err('Received unexpected error; re-raising it!')
        raise e
