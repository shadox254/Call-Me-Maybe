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
#  File: prompts.py                                                           #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/25 10:17:49 by rruiz                                      #
#  Updated: 2026/03/31 10:27:35 by rruiz                                      #
# *************************************************************************** #

from json import load
from ..model import PromptModel


def load_prompts(path: str) -> list[PromptModel]:
    try:
        with open(path, "r") as f:
            data = load(f)
            prompts_list = [PromptModel(**arg) for arg in data]
        return prompts_list
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
