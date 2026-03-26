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
#  File: model.py                                                             #
#  By: rruiz <rruiz@student.42.fr>                                            #
#  Created: 2026/03/23 16:57:41 by rruiz                                      #
#  Updated: 2026/03/26 18:12:18 by rruiz                                      #
# *************************************************************************** #

from pydantic import BaseModel
from llm_sdk.llm_sdk import Small_LLM_Model
import json
from enum import Enum

class FunctionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

class PromptModel(BaseModel):
    prompt: str

class States(Enum):
    START = "start"
    NAME = "name"
    END_NAME = "end_name"
    PARAMETERS = "parameters"
    END = "end"

class CallMeMaybe(Small_LLM_Model):
    def process(self, functions_list: list[FunctionModel], prompts_list: list[PromptModel]):
        state = States.START
        function_txt = "Available functions:\n"
        for function in functions_list:
            params_str = json.dumps(function.parameters)
            function_txt += f'- {{"name": "{function.name}", "description": "{function.description}", "parameters": {params_str}}}\n'

        prefixes = set()
        for function in functions_list:
            for i in range(1, len(function.name) + 1):
                prefixes.add(function.name[:i])

        vocab_path = self.get_path_to_vocab_file()
        vocab = self.load_vocab(vocab_path)
        rev_vocab = self.reverse_vocab(vocab)

        for prompt in prompts_list:
            to_write = function_txt + f'\nTask:\n{{\n  "prompt": "{prompt.prompt}",\n  "name": "'
            input_ids = []
            function_name = ""
            while (state != States.END):
                input_ids = []
                for a in self.encode(to_write):
                        input_ids.append(b for b in a)
                logits = self.get_logits_from_input_ids(input_ids)
                for token, id in vocab.items():
                    is_valid = False
                    if ((function_name + token) in prefixes):
                        is_valid = True
                    else:
                        if ((function_name + token) == (function.name for function in functions_list)):
                            is_valid = True
                            break
                    if is_valid is False:
                        logits[id] = float('-inf')
                best_id = logits.index(max(logits))
                best_token = rev_vocab[best_id]

                function_name += best_token
                input_ids.append(best_id)

                for function in functions_list:
                    if function_name == function.name:
                        state = States.END_NAME
                        break

            elif state == States.END_NAME:
                break

    def load_vocab(self, path: str):
        try:
            with open(path, "r") as f:
                vocab = json.load(f)
            return vocab
        except FileNotFoundError:
            raise FileNotFoundError("Error, vocab file not found")

    def reverse_vocab(self, vocab: dict):
        rev_vocab = {}
        for key, value in vocab.items():
            rev_vocab[value] = key
        return rev_vocab