*This project has been created as part of the 42 curriculum by rruiz*

## 📄 Description

Call Me Maybe is a project that lets us explore LLMs (Large Language Model) using function calling.\
The output must be a 100% valid JSON file. Since LLMs do not always generate valid JSON, we must use constrained decoding to ensure a correct output.

We have one file containing prompts and another containing function definitions (name, description, arguments, and return value):

```json
# JSON prompt file example :
[
	{
    	"prompt": "What is the sum of 2 and 3?"
	},
	{
		"prompt": "Reverse the string '.nuf ton si ebyaM eM llaC'"
  	},
	{
    	"prompt": "Greet Chewbacca"
	}
]
```


```json
# JSON function description file example :
[
	{
    	"prompt": "What is the sum of 2 and 3?"
	},
	{
		"prompt": "Reverse the string '.nuf ton si ebyaM eM llaC'"
  	},
	{
    	"prompt": "Greet Chewbacca"
	}
]
```

 ### Output example :
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string '.nuf ton si ebyaM eM llaC'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": ".nuf ton si ebyaM eM llaC"
    }
  {
    "prompt": "Greet Chewbacca",
    "name": "fn_greet",
    "parameters": {
		"name": "Chewbacca"
    }
  }
]
```

## Prerequisites
- Python (3.10+)
- uv
- +2G of storage to download the LLM

## Instructions
**Using the Makefile**
```bash
mask install  # install all dependencied using uv
make run  # Execute the main function
make debug  # Run the program using the built-in Python debugger pdb
make lint  # Performs static code analysis using Flake8 and Mypy to ensure the quality of the project
make lint-strict  # Performs a strict linting check, disabling non-typed code and requiring 100% compliance with standards
make clean  # Remove temporary file and caches

```
**Using uv**
```
uv run python -m src  # Run with default configuration
uv run python -m src
[--functions_definition <function_definition_file>]
[--input <input_file>]
[--output <output_file>]  # Run with custom arguments/paths
```

### Arguments
| Flag | Description |
| ---- | ----------- |
| --functions_definition | path to functions definition |
| --input | path to Json file with prompt |
| --output | path to output json file |

## Algorithm explanation
The algorithm relies on a constrained decoding technique driven by a state machine. Instead of letting the small language model generate text freely, the program strictly controls the output structure to ensure a valid JSON format.

The process works as follows:

- State Tracking: The program always knows exactly which step of the JSON construction it is currently in (e.g., searching for the function name, opening parameters, finding a specific parameter's value).

- Logit Masking: For each generated token, the code analyzes the model's vocabulary. The probabilities (logits) of all tokens that would break the JSON syntax or fail to match the expected data type are artificially set to -inf.

- Forced Prediction: The model then chooses the most probable token among the remaining allowed ones. For example, if it is in the state of generating a number, only digits, dots, and minus signs are permitted.

## Design decisions
Several major choices guided the project's architecture:

- Strict Generation via State Machine: Rather than asking the model to attempt JSON generation and hoping for the best, the writing of braces, quotes, and commas is strictly enforced by the script. This completely eliminates parsing errors caused by malformed JSON.

- Plain Text Pre-prompting: The descriptions of available tools are provided to the model as plain text (rather than JSON) to prevent visual mimicry. This ensures the model actually processes the user's question instead of just copying the tool definition's format.

- Few-Shot Prompting: Small models sometimes lack broad context or specific vocabulary. Injecting a concrete resolution example directly into the context (prompt) helps the model understand the expected extraction logic, even when dealing with unfamiliar subjects.

## Performance analysis
- Accuracy: Structural reliability is 100% due to logit masking. On the semantic side (finding the right function and arguments), the results are excellent for standard queries. For out-of-distribution data (complex or unknown vocabulary), accuracy heavily depends on the quality of the examples provided in the pre-prompt.

- Speed: The method introduces some computational overhead. Forcing the model to generate the entire JSON structure token by token is slower than having it extract only the relevant values. Furthermore, adding the full context (functions and examples) increases the input size for each loop iteration, which impacts the overall execution time across a large test suite.

- Reliability: The system is highly robust against format hallucinations. Its main drawback is its rigidity: tokenization handling (such as an unexpected space at the beginning of a token or complex escape characters) must be exhaustively accounted for in the state machine, otherwise the generation process will crash.

## Challenges faced
The most difficult challenges for me are understanding how to implement constrained decoding and finding arguments in the prompt. I solved the first one by creating a sentence using the function and the prompt before processing them. For the second one, I broke the problem down to find the most logical approach and I give to him a exemple of waht i want.

## Testing strategy
I tested every error I could think of and handled them.

## Example usage
In prompt file :
```json
[
	{
		"prompt": "What is the weakness of water type in pokemon ?"
	}
]
```

In functions definition file :
```json
[
	{
	"name": "fn_get_pokemon_type_weakness",
	"description": "Retrieve the weaknesses of a given Pokemon type.",
	"parameters": {
		"pokemon_type": {
		"type": "string"
		}
	},
	"returns": {
		"type": "string"
		}
	}
]
```

The model produces this result every time:
```json
[
  {
    "prompt": "What is the weakness of water type in pokemon ?",
    "name": "fn_get_pokemon_type_weakness",
    "parameters": {
      "pokemon_type": "water"
    	}
  }
]
```

## Ressources
docu:
	https://www.datacamp.com/fr/tutorial/python-argparse
	https://www.aidancooper.co.uk/constrained-decoding/#motivating-example
	https://www.datacamp.com/tutorial/python-uv
