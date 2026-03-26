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
#  File: Makefile                                                             #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/23 08:55:56 by rruiz                                      #
#  Updated: 2026/03/25 09:41:30 by rruiz                                      #
# *************************************************************************** #

MYPY_FLAGS= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install:
	@echo "Beautiful message"
	uv sync

run:
	uv run python -m src

debug:
	@echo "debug not available"

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	@-flake8 ${SRC}
	@-mypy ${SRC} $(MYPY_FLAGS)

lint-strict:
	@-flake8 ${SRC}
	@-mypy ${SRC} $(MYPY_FLAGS) --strict

sync:
	uv sync
