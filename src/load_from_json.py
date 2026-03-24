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
#  File: load_from_json.py                                                    #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/23 16:41:34 by rruiz                                      #
#  Updated: 2026/03/24 09:20:41 by rruiz                                      #
# *************************************************************************** #

import json
from .model import FunctionModel, PromptModel

def load_functions(path: str) -> list:
    try:
        with open(path, "r") as f:
            data = json.load(f)
            # for arg in data:
            funcs_list = [FunctionModel(**arg) for arg in data]
        return funcs_list
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")


def load_prompts(path: str) -> list:
    try:
        with open(path, "r") as f:
            data = json.load(f)
            prompts_list = [PromptModel(**arg) for arg in data]
        return prompts_list
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
