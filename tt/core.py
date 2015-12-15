import sys
import os
import logging as log

from argparse import ArgumentParser, RawTextHelpFormatter

from eqtools import get_evaluation_result
from fmttools import TruthTablePrinter

__all__ = ['main']
__version__ = 0.1
__date__ = "2015-11-24"
__updated__ = "2015-11-24"

def main(argv=None):
    """The main entry point for the program. Arguments and arguments 
        descriptions are defined, and the correct functionality is chosen
        from the user input.    
    """
    if argv is None:
        argv = ["tt", '"F = A or B or C"']
    else:
        sys.argv.extend(argv)

    # program information
    program_source_control_url = "www.github.com/welchbj/tt"
    program_name = os.path.basename(sys.argv[0])
    program_version = "v{0}".format(str(__version__))
    program_build_date = str(__updated__)
    program_version_message = "{version}, {build}".format(version=program_version, build=program_build_date)
    program_license = "MIT"
    program_author = "Brian Welch"
    program_desc = """
    tt is a command line utility for printing truth tables and Karnaugh Maps.
    Here is some pertinent information about the release you are using:
    Version: {version}
    Author: {author}
    License: {license}""".format(version=program_version,
                                 author=program_author,
                                 license=program_license)
    LOGGING_FORMAT = "%(levelname)s: %(message)s"

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_desc,
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument("--version",
                            action="version",
                            version=program_version_message,
                            help="Program version and latest build date")
        parser.add_argument("--verbose", "-v",
                            action="store_true",
                            help="Specify verbose output, useful for debugging.")
        parser.add_argument("--kmap", 
                            action="store_true", 
                            help="Generate kmap of specified boolean equation.")
        parser.add_argument("--intermediates", 
                            action="store_true", 
                            help="Indicates that intermediate boolean expressions should be\n"
                                 "displayed with their own column in the truth table.\n"
                                 "Not valid with the --kmap option.")
        parser.add_argument(dest="equation", 
                            help="Boolean equation to be analyzed, surrounded with double quotes.\n"
                                 "Boolean operations are specified using plain Englsh in lowercase\n"
                                 "For example, you would enter:\n"
                                 "F=A+B as \"F = A or B\"\n"
                                 "F=AB as \"F = A and B\"\n"
                                 "Currently the only operations supported are:\n"
                                 "(1) and\n"
                                 "(2) or\n"
                                 "The equation should be the last argument specified") 

        # Process arguments
        args = parser.parse_args()
        verbose = args.verbose
        kmap = args.kmap
        intermediates = args.intermediates
        equation = args.equation
        
        if verbose:
            log.basicConfig(format=LOGGING_FORMAT, level=log.DEBUG)
            log.info("Starting verbose output.")
        else:
            log.basicConfig(format=LOGGING_FORMAT)
        
        if kmap and intermediates:
            parser.error("--intermediates option is not compatible with kmap generation")
        elif kmap:
            # TODO
            pass
        elif intermediates:
            # TODO
            pass
        else: # default to truth table generation
            eval_result = get_evaluation_result(equation)
            tt_printer = TruthTablePrinter(eval_result)
            tt_printer.print_tt()

    except KeyboardInterrupt:
        return 0
    except RuntimeError:
        return 1
    #except Exception as e:
    #    indent = len(program_name) * " "
    #    print("An unexpected error occurred.\n",
    #          "Please notify the project maintainer at" + program_source_control_url + "\n",
    #          "Error info:\n",
    #          program_name + ": " + repr(e) + "\n",
    #          "for help use --help", sep="")
    #    return 2