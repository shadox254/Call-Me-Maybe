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
#  Updated: 2026/03/31 10:43:12 by rruiz                                      #
# *************************************************************************** #

MYPY_FLAGS	= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip
SRC			= src

install:
	@echo "Beautiful message"
	uv sync

run:
	uv run python -m src

debug:
	@clear
	@uv run -m pdb -m src
	@echo "debug not available"

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	@-uv run flake8 ${SRC}
	@-uv run mypy ${SRC} $(MYPY_FLAGS)

lint-strict:
	@-uv run flake8 ${SRC}
	@-uv run mypy ${SRC} $(MYPY_FLAGS) --strict

sync:
	uv sync
