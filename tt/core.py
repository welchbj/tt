"""
A module containing the gateway between the command line interface and tt's
underlying functionality.
"""

import logging as log

from argparse import ArgumentParser, RawTextHelpFormatter

from eqtools import BooleanEquationWrapper, GrammarError
from fmttools import TruthTablePrinter

__all__ = ["main"]
__version__ = 0.1
__date__ = "2015-11-24"
__updated__ = "2015-12-21"


def main():
    """
    The main entry point to the command line application. Sets up the arg
    parser and chooses which control flow to follow according to user's command
    line options.

    Returns:
        The error level:
            0: Program ran fine.
            1: Recognized error occurred.
            2: Unrecognized error occurred.
    """
    logging_format = "%(levelname)s: %(message)s"

    # program information
    program_source_control_url = "www.github.com/welchbj/tt"
    program_version = "v{0}".format(str(__version__))
    program_build_date = str(__updated__)
    program_version_message = "{version}, {build}".format(
        version=program_version, build=program_build_date)
    program_license = "MIT"
    program_author = "Brian Welch"
    program_desc = """\
    tt is a command line utility for printing truth tables and Karnaugh Maps.
    Here is some pertinent information about the release you are using:
    Version: {version}
    Author: {author}
    License: {license}
    URL: {url}""".format(
        version=program_version,
        author=program_author,
        license=program_license,
        url=program_source_control_url)

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_desc,
            formatter_class=RawTextHelpFormatter)
        parser.add_argument(
            "--version",
            action="version",
            version=program_version_message,
            help="Program version and latest build date")
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Specify verbose output, useful for debugging.")
        parser.add_argument(
            "--kmap",
            action="store_true",
            help="Generate kmap of specified boolean equation.\n"
                 "Currently unsupported.")
        parser.add_argument(
            "--intermediates",
            action="store_true",
            help="Indicates that intermediate Boolean expressions should be\n"
                 "displayed with their own column in the truth table.\n"
                 "Not valid with the --kmap option.\n"
                 "Currently unsupported.")
        parser.add_argument(
            dest="equation",
            help="Boolean equation to be analyzed, enclosed with quotes.\n"
                 "Boolean operations can be specified using plain English or "
                 "their common symbolic equivalents.\n"
                 "For example, the two equations:\n"
                 "\t(1) \"out = operand_1 and operand_2 or operand_3\"\n"
                 "\t(2) \"out = operand_1 && operand_2 || operand_3\"\n"
                 "Would evaluate identically.\n"
                 "\n"
                 "Supported Boolean operations are:\n"
                 "\tnot\n"
                 "\txor\n"
                 "\txnor\n"
                 "\tand\n"
                 "\tnand\n"
                 "\tor\n"
                 "\tnor\n")

        # Process arguments
        args = parser.parse_args()
        verbose = args.verbose
        kmap = args.kmap
        intermediates = args.intermediates
        equation = args.equation

        if verbose:
            log.basicConfig(format=logging_format, level=log.DEBUG)
            log.info("Starting verbose output.")
        else:
            log.basicConfig(format=logging_format)

        if kmap and intermediates:
            parser.error(
                "--intermediates option is not compatible with kmap generation"
            )
            raise NotImplementedError("--kmap and --intermediates")
        elif kmap:
            raise NotImplementedError("--kmap")
        elif intermediates:
            raise NotImplementedError("--intermediates")
        else:  # default to truth table generation
            bool_eq = BooleanEquationWrapper(equation)
            eval_result = bool_eq.get_evaluation_result()
            tt_printer = TruthTablePrinter(eval_result)
            tt_printer.print_tt()

    except KeyboardInterrupt:
        return 0
    except GrammarError as e:
        e.log()
        return 1
    except NotImplementedError as e:
        log.error("Tried to use a feature that is not yet implemented: " +
                  str(e))
        return 1
    except Exception as e:
        log.critical("An unknown error occurred. "
                     "Cannot continue program execution.\n" +
                     str(e))
        return 2
