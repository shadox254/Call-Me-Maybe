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
#  Updated: 2026/03/26 09:27:43 by rruiz                                      #
# *************************************************************************** #

from pydantic import BaseModel
from llm_sdk.llm_sdk import Small_LLM_Model
import json
from numpy import inf

class FunctionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

class PromptModel(BaseModel):
    prompt: str

class CallMeMaybe(Small_LLM_Model):
    def process(self, functions_list: list[FunctionModel], prompts_list: list[PromptModel]):
        function_txt = "Available functions:\n"
        for function in functions_list:
            params_str = json.dumps(function.parameters)
            function_txt += f'- {{"name": "{function.name}", "description": "{function.description}", "parameters": {params_str}}}\n'

        logits = set()
        for function in functions_list:
            for i in range(1, len(function.name) + 1):
                logits.add(function.name[:i])

        for prompt in prompts_list:
            to_write = function_txt + f'\nTask:\n{{\n  "prompt": "{prompt.prompt}",\n  "name": "'

            # print(to_write)
            encode_prompt = self.encode(to_write)
