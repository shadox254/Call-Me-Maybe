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
#  Updated: 2026/03/30 04:54:01 by rruiz                                      #
# *************************************************************************** #

import sys
from src import parse_arguments
from src import load_functions
from src import load_prompts
from src import CallMeMaybe
from json import JSONDecodeError


def main() -> None:
    try:
        args = parse_arguments()

        functions_list = load_functions(args.functions_definition)
        if not functions_list:
            print(f"Error, no function was loaded from \
{args.functions_definition}")
            sys.exit(2)

        prompts_list = load_prompts(args.input)
        if not prompts_list:
            print(f"Error, no prompt was loaded from {args.input}")
            sys.exit(2)

        test = CallMeMaybe()
        test.process(functions_list, prompts_list, args)

    except FileNotFoundError as e:
        print(f"Error: The file '{e.filename}' was not found.",
              file=sys.stderr)
        sys.exit(1)
    except JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax at line {e.lineno}.",
              file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Data schema mismatch.\n{e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("User interruption (Ctrl+C).", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
