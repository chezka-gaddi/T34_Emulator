"""
.. moduleauthor:: Chezka Gaddi

"""

import argparse
import sys
import logging
from t34 import Emulator
from t34 import TestEmulator


def parse_args():
    """
        **Argument Parser**

        Parses the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Emulator")

    parser.add_argument("program_name",
                        nargs='?',
                        help="name of the object file for the program")

    parser.add_argument("--debug",
                        "-d",
                        action="store_true",
                        default=False,
                        help="Print debugging information")

    return parser.parse_args()


def main(args):
    """
        **Main**

        Entry point for the T34 emulator program.

        :param args: command line arguments.
    """
    if args.debug is True:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug(args)
    em = Emulator.Emulator(args.program_name)
    em.start_emulator()


if __name__ == "__main__":
    main(parse_args())
