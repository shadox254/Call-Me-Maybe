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
#  Updated: 2026/04/01 10:07:19 by rruiz                                      #
# *************************************************************************** #

from json import load
from ..model import PromptModel


def load_prompts(path: str) -> list[PromptModel]:
    """Loads the list of prompts to evaluate from a JSON file.

    Args:
        path (str): The path to the prompts JSON file.

    Returns:
        list[PromptModel]: A list of objects modeling each prompt.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    try:
        with open(path, "r") as f:
            data = load(f)
            prompts_list = [PromptModel(**arg) for arg in data]
        return prompts_list
    except FileNotFoundError:
        raise FileNotFoundError(f"file not found: {path}")
