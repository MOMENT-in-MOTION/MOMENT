# MOMENT

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

MOMENT is executable via the command line:

```bash
python -m src.main <path-to-metamodel> [OPTIONS]
```

The metamodel must be a `.json` file.

### Arguments

| Argument            | Description                        |
|---------------------|------------------------------------|
| `path-to-metamodel` | Path to the metamodel JSON file    |

### Options

| Option                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `-o`, `--output <path>`       | Output directory for generated files (default: `project-root/output/`)      |
| `-v`, `--verbose`             | Enables debug-level logging; defaults to info level                         |

### Examples

Generate Python API code from a metamodel:

```bash
python -m src.main path/to/metamodel.json
```

## Testing

Run all tests using pytest:

```bash
python -m pytest
```

Run a specific test file:

```bash
python -m pytest tests/codegenerator/test_codegenerator.py -v
```

### Code Coverage

Run tests with coverage report:

```bash
python -m pytest --cov=src
```

Generate HTML coverage report:

```bash
python -m pytest --cov=src --cov-report=html
```

View the HTML report by opening `htmlcov/index.html` in your browser.

## Linting

This project uses pylint for code quality checks. Run pylint on the source and test files:

```bash
python -m pylint src/ tests/
```

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
