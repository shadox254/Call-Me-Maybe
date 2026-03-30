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
#  Updated: 2026/03/30 07:06:34 by rruiz                                      #
# *************************************************************************** #

from json import load


def load_functions(path: str) -> list:
    from src import FunctionModel
    try:
        with open(path, "r") as f:
            data = load(f)
            # for arg in data:
            funcs_list = [FunctionModel(**arg) for arg in data]
        return funcs_list
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
