import sys
import os

from argparse import ArgumentParser, RawTextHelpFormatter

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
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_source_control_url = "www.github.com/welchbj/tt"
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
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument("--kmap", 
                            action="store_true", 
                            help="generate kmap of specified boolean equation.")
        parser.add_argument("--intermediates", 
                            action="store_true", 
                            help="indicates that intermediate boolean expressions should be displayed with their own column in the truth table.\n"
                                  "Not valid with the --kmap option.")
        parser.add_argument("--version",
                            action="version",
                            version=program_version_message,
                            help="program version and latest build date")
        parser.add_argument(dest="equation", 
                            help="Boolean equation to be analyzed, surrounded with double quotes.\n"
                                 "Boolean operations are specified with:\n\n"
                                 "AND -> &\n"
                                 "OR -> |\n\n"
                                 "These are the operations currently supported\n"
                                 "The equation should be the last argument specified") 

        # Process arguments
        args = parser.parse_args()
        kmap = args.kmap
        intermediates = args.intermediates
        equation = args.equation
        
        if kmap and intermediates:
            parser.error("--intermediates option is not compatible with kmap generation")
        
        print("equation: {eq}".format(eq=equation))
            
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write("An unexpected error occurred.")
        sys.stderr.write("Please notify the project maintainer at {url}".formart(url=program_source_control_url))
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2