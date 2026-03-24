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
#  File: main.py                                                              #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/23 16:52:43 by rruiz                                      #
#  Updated: 2026/03/24 16:54:36 by rruiz                                      #
# *************************************************************************** #

import argparse
import sys
from src.load_from_json import load_functions, load_prompts
from llm_sdk.llm_sdk import Small_LLM_Model

def main():
    try:
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("--input", default="data/input/function_calling_tests.json", type=str)
            parser.add_argument( "--functions_definition", default="data/input/functions_definition.json", type=str)
            parser.add_argument("--output", default="data/output/function_calling_results.json", type=str)
            args = parser.parse_args()

            functions_list = load_functions(args.functions_definition)
            if not functions_list:
                print(f"Error, no function was loaded from {args.functions_definition}")
                sys.exit(2)

            prompts_list = load_prompts(args.input)
            if not prompts_list:
                print(f"Error, no prompt was loaded from {args.input}")
                sys.exit(2)

        except (FileNotFoundError) as e:
            print(e)
            sys.exit()
    except Exception as e:
        print(f"Unexpected error: {e}")





if __name__ == "__main__":
    # sys.exit(main())
    test = Small_LLM_Model()
    test2 = test.encode("Je suis une phrase de texte d'une longueur correcte")
    for t in test2:
        for e in t:
            print(f"{e}: {test.decode(e)}")
    # print(f"test2: {test2}\n\ntest: {test.decode(test2)}")
