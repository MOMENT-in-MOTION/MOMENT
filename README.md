# MOMENT

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Currently the programm is executable via the commandline. To run it enter:

```bash
python .\src\main.py <path-to-meta-model>
```

The meta-model has to be a .json file.

## API Configuration

The generated API can be customized by modifying the configuration file located at `src/api_config.json`. 

### Default Configuration

```json
{
    "GenerateGetters": "true",
    "GenerateSetters": "true",
    "GenerateConstructors": "true",
    "StrictPrivacy": "true",
    "NamingConvention": "snake_case"
}
```

Enable or disable the automatic creation of class methods using ```GenerateGetters```, ```GenerateSetters```, and ```GenerateConstructors```. 
Each accepts a string value of either "true" or "false".

Control the casing style of the generated code by changing the ```NamingConvention```. 
This option supports the following formatting styles: "snake_case" and "camelCase".
