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
#  Updated: 2026/03/30 03:08:50 by rruiz                                      #
# *************************************************************************** #

from pydantic import BaseModel
from llm_sdk.llm_sdk import Small_LLM_Model
import json
from enum import Enum
from argparse import Namespace
from pathlib import Path

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
    PARAMETERS_VALUE = "parameters value"
    END = "end"

class CallMeMaybe(Small_LLM_Model):
    def process(self, functions_list: list[FunctionModel], prompts_list: list[PromptModel], args: Namespace):
        state = States.START
        results = []
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
            for a in self.encode(to_write):
                for b in a:
                    input_ids.append(b)

            function_name = ""
            state = States.NAME
            saved_params = {}
            while (state != States.END):
                logits = self.get_logits_from_input_ids(input_ids)
                if state == States.NAME:
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

                    best_token_id = logits.index(max(logits))
                    best_token = rev_vocab[best_token_id]

                    function_name += best_token
                    input_ids.append(best_token_id)

                    for function in functions_list:
                        if function_name == function.name:
                            state = States.END_NAME
                            break

                elif state == States.END_NAME:
                    between_name_params = '", "parameters": {'
                    for a in self.encode(between_name_params):
                        for b in a:
                            input_ids.append(b)
                    params_to_process = list(function.parameters.items())
                    state = States.PARAMETERS

                elif state == States.PARAMETERS:
                    if len(params_to_process) == 0:
                        last_bracket = self.encode("}")
                        for a in last_bracket:
                            for b in a:
                                input_ids.append(b)
                        state = States.END
                    else:
                        key, value = params_to_process.pop(0)
                        for a in self.encode(f'"{key}": '):
                            for b in a:
                                input_ids.append(b)
                        param_tokens = []
                        state = States.PARAMETERS_VALUE

                elif state == States.PARAMETERS_VALUE:
                    match value["type"]:
                        case "number": # float
                            generate_number = ""
                            has_a_point_decimal = False
                            end_tokens = [",", "}"]

                            while True:
                                logits = self.get_logits_from_input_ids(input_ids)
                                for token, id in vocab.items():
                                    if token in end_tokens:
                                        if len(generate_number) == 0:
                                            logits[id] = float('-inf')
                                        continue

                                    elif not all(c in "-0123456789." for c in token):
                                        logits[id] = float('-inf')

                                    elif "-" in token and len(generate_number) > 0:
                                        logits[id] = float('-inf')

                                    elif "." in token:
                                        if has_a_point_decimal is True or len(generate_number) == 0:
                                            logits[id] = float('-inf')

                                best_id = logits.index(max(logits))
                                best_token = rev_vocab[best_id]

                                if best_token == "," or best_token == "}":
                                    saved_params[key] = float(generate_number)
                                    input_ids.append(best_id)

                                    if best_token == ",":
                                        for a in self.encode(" "):
                                            for b in a:
                                                input_ids.append(b)
                                        state = States.PARAMETERS
                                    else:
                                        state = States.END
                                    break
                                input_ids.append(best_id)
                                generate_number += best_token
                                if "." in best_token:
                                    has_a_point_decimal = True

                        case "string":
                            if len(param_tokens) == 0:
                                for a in self.encode('"'):
                                    for b in a:
                                        input_ids.append(b)

                            logits = self.get_logits_from_input_ids(input_ids)
                            best_id = logits.index(max(logits))
                            best_token = rev_vocab[best_id]

                            param_tokens.append(best_token)
                            current_str = "".join(param_tokens)

                            end_index = -1
                            escaped = False
                            
                            for i, char in enumerate(current_str):
                                if char == '\\' and not escaped:
                                    escaped = True
                                elif char == '"' and not escaped:
                                    end_index = i
                                    break
                                else:
                                    escaped = False

                            if end_index != -1:
                                final_value = current_str[:end_index]
                                saved_params[key] = final_value
                                
                                valid_part = current_str[len(current_str) - len(best_token):end_index + 1]
                                for a in self.encode(valid_part):
                                    for b in a:
                                        input_ids.append(b)
                                
                                param_tokens.clear()
                                
                                if len(params_to_process) > 0:
                                    for a in self.encode(', '):
                                        for b in a:
                                            input_ids.append(b)
                                    state = States.PARAMETERS
                                else:
                                    for a in self.encode('}'):
                                        for b in a:
                                            input_ids.append(b)
                                    state = States.END
                            else:
                                input_ids.append(best_id)


                        case "integer": # int
                            state = States.PARAMETERS


                        case _:
                            raise TypeError("Error, unknow type")


            current_result = {
                "prompt": prompt.prompt,
                "name": function_name,
                "parameters": saved_params
            }
            results.append(current_result)

            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

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