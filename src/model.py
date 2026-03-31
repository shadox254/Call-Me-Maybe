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
#  Updated: 2026/03/31 17:41:33 by rruiz                                      #
# *************************************************************************** #

from pydantic import BaseModel
from llm_sdk import Small_LLM_Model
import json
from enum import Enum
from argparse import Namespace
from pathlib import Path
from typing import Any


class FunctionModel(BaseModel):  # type: ignore[misc, unused-ignore]
    """Represents a callable function's schema.

    Defines the expected structure of a function, including its name,
    description, and the parameters it accepts.

    Attributes:
        name (str): The identifier of the function.
        description (str): A brief explanation of what the function does.
        parameters (dict): The expected arguments and their types.
    """
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]


class PromptModel(BaseModel):  # type: ignore[misc, unused-ignore]
    """Represents an input prompt for the model.

    Contains the natural language query that needs to be parsed into
    a specific function call by the LLM.

    Attributes:
        prompt (str): The raw text input to be processed.
    """
    prompt: str


class States(Enum):
    """Represents the different states of the parsing state machine.

    Attributes:
        NAME: Extracting the function name.
        END_NAME: Transition state after the function name is fully generated.
        PARAMETERS: Determining the next parameter to extract.
        PARAMETERS_VALUE: Extracting the value for a specific parameter.
        END: The parsing process is complete.
    """
    START = "start"
    NAME = "name"
    END_NAME = "end_name"
    PARAMETERS = "parameters"
    PARAMETERS_VALUE = "parameters value"
    END = "end"


class CallMeMaybe(Small_LLM_Model):  # type: ignore[misc, unused-ignore]
    """Core model class for handling function calling tasks.

    Inherits from Small_LLM_Model to process natural language prompts
    and map them to specific function calls with extracted parameters
    using a state machine approach.

    Attributes:
        (List your specific instance attributes here if you initialize any \
            in __init__)
    """
    def process(self, functions_list: list[FunctionModel],
                prompts_list: list[PromptModel], args: Namespace) -> None:
        """Executes the model on a series of prompts to call functions.

            Processes each prompt by identifying the corresponding function and
            extracting the expected parameter values using a state machine.
            Saves the final results to a JSON file.

            Args:
                functions_list (list[FunctionModel]): The available function \
                    models.
                prompts_list (list[PromptModel]): The input prompts.
                args (Namespace): The arguments containing the output path.

            Raises:
                TypeError: If a parameter type to process is unknown.
        """
        state = States.START
        results = []
        function_txt = "Available functions:\n"
        for function in functions_list:
            function_txt += f"- {function.name}: {function.description} Parameters: "
            params_list = []
            for p_name, p_info in function.parameters.items():
                params_list.append(f"{p_name} ({p_info['type']})")
            function_txt += ", ".join(params_list) + "\n"

        prefixes = set()
        for function in functions_list:
            for i in range(1, len(function.name) + 1):
                prefixes.add(function.name[:i])

        vocab_path = self.get_path_to_vocab_file()
        vocab = self.load_vocab(vocab_path)
        rev_vocab = self.reverse_vocab(vocab)

        for prompt in prompts_list:
            to_write = function_txt + (f'\nTask:\n{{\n  "prompt":\
"{prompt.prompt}",\n  "name": "')
            input_ids = []
            for a in self.encode(to_write):
                for b in a:
                    input_ids.append(b)

            function_name = ""
            state = States.NAME
            saved_params: dict[str, float | str | int] = {}
            while (state != States.END):
                logits = self.get_logits_from_input_ids(input_ids)
                if state == States.NAME:
                    for token, id in vocab.items():
                        is_valid = False

                        if ((function_name + token) in prefixes):
                            is_valid = True

                        else:
                            if ((function_name
                                 + token) == (function.name
                                              for function in functions_list)):
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
                        param_tokens: list[str] = []
                        state = States.PARAMETERS_VALUE

                elif state == States.PARAMETERS_VALUE:
                    match value["type"]:
                        case "number":  # float
                            logits = self.get_logits_from_input_ids(input_ids)
                            curr_str = "".join(param_tokens)

                            for token, id in vocab.items():
                                clean_token = token.strip()

                                if clean_token in [",", "}"]:
                                    if (len(curr_str) == 0 or
                                            curr_str in ["-", "."]):
                                        logits[id] = float('-inf')
                                    continue
                                if (not all(c in "0123456789-."
                                            for c in clean_token)):
                                    if clean_token != "":
                                        logits[id] = float('-inf')
                                    continue

                                if "-" in clean_token and len(curr_str) != 0:
                                    logits[id] = float('-inf')

                                if "." in clean_token and "." in curr_str:
                                    logits[id] = float('-inf')

                            best_id = logits.index(max(logits))
                            best_token = rev_vocab[best_id]
                            clean_best = best_token.strip()

                            if clean_best in [",", "}"]:
                                saved_params[key] = float(curr_str)

                                for a in self.encode(best_token):
                                    for b in a:
                                        input_ids.append(b)

                                if clean_best == ",":
                                    state = States.PARAMETERS
                                else:
                                    state = States.END

                            else:
                                input_ids.append(best_id)
                                param_tokens.append(clean_best)

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
                                final_value = (current_str[:end_index]
                                               .replace('\u0120', ' '))
                                saved_params[key] = final_value

                                valid_part = (
                                    current_str[len(current_str)
                                                - len(best_token):
                                                end_index + 1])
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

                        case "integer":
                            logits = self.get_logits_from_input_ids(input_ids)
                            curr_str = "".join(param_tokens)

                            for token, id in vocab.items():
                                clean_token = token.strip()

                                if clean_token in [",", "}"]:
                                    if len(curr_str) == 0 or curr_str == "-":
                                        logits[id] = float('-inf')
                                    continue

                                if not all(c in "0123456789-"
                                           for c in clean_token):
                                    if clean_token != "":
                                        logits[id] = float('-inf')
                                    continue

                                if "-" in clean_token and len(curr_str) != 0:
                                    logits[id] = float('-inf')

                                if (curr_str in ["0", "-0"] and any
                                        (c in "0123456789"
                                         for c in clean_token)):
                                    logits[id] = float('-inf')

                            best_id = logits.index(max(logits))
                            best_token = rev_vocab[best_id]
                            clean_best = best_token.strip()

                            if clean_best in [",", "}"]:
                                saved_params[key] = int(curr_str)

                                for a in self.encode(best_token):
                                    for b in a:
                                        input_ids.append(b)

                                if clean_best == ",":
                                    state = States.PARAMETERS
                                else:
                                    state = States.END

                            else:
                                input_ids.append(best_id)
                                param_tokens.append(clean_best)

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

    def load_vocab(self, path: str) -> Any:
        """Loads a vocabulary dictionary from a file.

        Args:
            path (str): The path to the vocabulary file.

        Returns:
            Any: The loaded vocabulary as a dictionary.

        Raises:
            FileNotFoundError: If the vocabulary file is not found.
        """
        try:
            with open(path, "r") as f:
                vocab = json.load(f)
            return vocab
        except FileNotFoundError:
            raise FileNotFoundError("Error, vocab file not found")

    def reverse_vocab(self, vocab: dict[str, int]) -> dict[int, str]:
        """Reverses the keys and values of a vocabulary dictionary.

        Args:
            vocab (dict[str, int]): The original vocabulary (token to id).

        Returns:
            dict[int, str]: The reversed vocabulary (id to token).
        """
        rev_vocab = {}
        for key, value in vocab.items():
            rev_vocab[value] = key
        return rev_vocab
