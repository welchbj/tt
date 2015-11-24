import sys
import os

from argparse import ArgumentParser, ArgumentError
from argparse import RawDescriptionHelpFormatter
from argparse import REMAINDER

__all__ = ['main']
__version__ = 0.1
__date__ = "2015-11-24"
__updated__ = "2015-11-24"

def help_provider():
    pass

def main(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v{version}".format(version=str(__version__))
    program_build_date = str(__updated__)
    program_version_message = \
        "{version}, {build}".format(version=program_version, 
                                    build=program_build_date)
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

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_desc, 
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--kmap", 
                            action="store_true", 
                            help="generate kmap of specified boolean equation")
        parser.add_argument("--intermediates", 
                            action="store_true", 
                            help="""indicates that intermediate boolean expressions should be displayed with their own column in the truth table. 
                                    Not valid with the --kmap option.""")
        parser.add_argument(dest="equation", 
                            help="Boolean equation to be analyzed. This should be the last argument provided") 

        # Process arguments
        args = parser.parse_args()
        kmap = args.kmap
        intermediates = args.intermediates
        equation = args.intermediates
        
        
        if kmap and intermediates:
            raise ArgumentError("--intermediates option is not compatible with kmap generation")
        
        print("equation: {eq}".format(eq=equation))
            
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2