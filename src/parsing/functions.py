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
#  File: functions.py                                                         #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/25 10:16:31 by rruiz                                      #
#  Updated: 2026/04/01 10:07:17 by rruiz                                      #
# *************************************************************************** #

from json import load
from ..model import FunctionModel


def load_functions(path: str) -> list[FunctionModel]:
    """Loads the list of function definitions from a JSON file.

    Args:
        path (str): The path to the functions JSON file.

    Returns:
        list[FunctionModel]: A list of objects modeling each function.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    try:
        with open(path, "r") as f:
            data = load(f)
            funcs_list = [FunctionModel(**arg) for arg in data]
        return funcs_list
    except FileNotFoundError:
        raise FileNotFoundError(f"file not found: {path}")
