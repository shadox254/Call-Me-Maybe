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
#  File: __main__.py                                                          #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/23 16:52:43 by rruiz                                      #
#  Updated: 2026/03/27 12:00:48 by rruiz                                      #
# *************************************************************************** #

import sys
from src import parse_arguments
from src import load_functions
from src import load_prompts
from src import CallMeMaybe

def main():
    try:
        try:
            args = parse_arguments()

            functions_list = load_functions(args.functions_definition)
            if not functions_list:
                print(f"Error, no function was loaded from {args.functions_definition}")
                sys.exit(2)

            prompts_list = load_prompts(args.input)
            if not prompts_list:
                print(f"Error, no prompt was loaded from {args.input}")
                sys.exit(2)

            test = CallMeMaybe()
            test.process(functions_list, prompts_list, args)

            # with open(args.output, "w") as f:
            #     for prompt in prompts_list:
            #         to_dump = {"prompt": prompt.prompt, "name": None, "parameters": None}
            #         Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            #         dump(to_dump, f)

        except (FileNotFoundError) as e:
            print(e)
            sys.exit()
    except Exception as e:
        print(f"Unexpected error: {e}")





if __name__ == "__main__":
    sys.exit(main())
    # test = Small_LLM_Model()
    # print("to vocab", test.get_path_to_vocab_file())
    # print("to_tokenizer", test.get_path_to_tokenizer_file())
    # print("to merge", test.get_path_to_merges_file())
    # test2 = test.encode("sum add ajout somme")
    # test3 = []
    # for t in test2:
    #     for e in t:
    #         # print(f"{e}: {test.decode(e)}")
    #         test3.append(e)
    # test5 = "\n".join(str(t) for t in sorted(test.get_logits_from_input_ids(test3), reverse=True))
    # with open("test.txt", "w") as f:
    #     f.write(f"{test5}\n")
    # print(f"test2: {test2}\n\ntest: {test.decode(test2)}")
