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


## Design decisions


## Performance analysis


## Challenges faced
The most difficult challenges for me are understanding how to implement constrained decoding and finding arguments in the prompt. I solved the first one by creating a sentence using the function and the prompt before processing them. For the second one, I broke the problem down to find the most logical approach.

## Testing strategy
I tested every error I could think of and handled them.

## Example usage
In prompt file :
```json
[
	{
		"prompt": "What is the Water-type's weakness in the Pokemon games ?"
	}
]
```

In functions definition file :
```json
[
	{
    "name": "fn_get_weakness",
    "description": "Get weakness of Pokemon type.",
    "parameters": {
      "type": {
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
  {
    "prompt": "What is the Water-type's weakness in the Pokemon games?",
    "name": "fn_get_weakness",
    "parameters": {
      "type": "string"
    }
  }
```

## Ressources
docu:
	https://www.datacamp.com/fr/tutorial/python-argparse
	https://www.aidancooper.co.uk/constrained-decoding/#motivating-example
	https://www.datacamp.com/tutorial/python-uv
































