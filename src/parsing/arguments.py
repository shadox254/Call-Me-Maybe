# *************************************************************************** #
#                                                                             #
#     |\      _,,,---,,_                                                      #
#     /,`.-'`'    -.  ;-;;,_                                                  #
#    |,4-  ) )-,_. ,\ (  `'-'                                                 #
#   '---''(_/--'  `-'\_)         __..--''``---....___   _..._    __           #
#                            _.-'    .-/";  `        ``<._  ``.''_ `.         #
#                        _.-' _..--.'_    \                    `( ) )         #
#                       (_..-' // (< _     ;_..__               ; `'          #
#                                  `-._,_)' // / ``--...____..-'              #
#                                                                             #
# *************************************************************************** #
#  File: arguments.py                                                         #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/25 10:05:54 by rruiz                                      #
#  Updated: 2026/03/31 14:57:59 by rruiz                                      #
# *************************************************************************** #

from argparse import Namespace, ArgumentParser


def parse_arguments() -> Namespace:
    """Parses command-line arguments.

    Returns:
        Namespace: The parsed arguments containing paths for the input file,
        functions definition, and output file.
    """
    args = ArgumentParser()
    args.add_argument(
        "--input", "-i",
        help="Path to the file containing the prompts",
        default="data/input/function_calling_tests.json",
        type=str
        )
    args.add_argument(
        "--functions_definition", "-d",
        help="Path to the file in which functions are defined",
        default="data/input/functions_definition.json",
        type=str
        )
    args.add_argument(
        "--output", "-o",
        help="Path to the file where output are saved",
        default="data/output/function_calling_results.json",
        type=str
        )
    parsed_args = args.parse_args()
    return parsed_args
