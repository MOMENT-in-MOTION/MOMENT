# MOMENT

## Installation

Install the required dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

For production only (no dev dependencies):

```bash
uv sync --no-dev
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

## API Configuration

The generated API can be customized by modifying the configuration file located at `src/api_config.json`.

### Default Configuration

```json
{
    "GenerateGetters": "true",
    "GenerateSetters": "true",
    "GenerateConstructors": "true",
    "GenerateHasFunctions": "true",
    "StrictPrivacy": "true",
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
    "AllowUnreachableClasses": "true",
    "RelativeImports": "true",
    "Inheritance": "native",
    "ImportMode": "merge",
    "SerializationFormat": [
        "json",
        "xml"
    ]
}
```

### Configuration Options

#### Code Generation

Enable or disable the automatic creation of class methods using:
- `GenerateGetters` - generates getter methods for all fields
- `GenerateSetters` - generates setter methods for all fields
- `GenerateConstructors` - generates constructor methods for all fields
- `GenerateHasFunctions` - generates Has-Functions for all fields

Each accepts a string value of either "true" or "false".

##### Getters  
Getters will be generated following a template like so:
```python
def  get_test(self) -> Test:
"""Generated getter for _test"""
if  self._test  is  None:
raise  ValueError("Field '_test' has not been initialized.")
return  self._test
```
##### Setters
Setters will be generated following a template like so:
```python
def  set_test(self, value: Test) -> None:
"""
Generated setter for _test

Args:
value: The new value to assign to the "_test" attribute
"""
if  not  isinstance(value, Test):
raise  TypeError(
f"Expected 'Test' for '_test', got {type(value).__name__!r}"
)
self._test  =  value
```
##### Constructors
Constructors will be generated following a template like so:
```python
    def __init__(self, test: Test, name: str = "root") -> None:
        """Generated constructor for Tester"""
        if not isinstance(test, Test):
            raise TypeError(
                f"Expected 'Test' for '_test', got {type(test).__name__!r}"
            )

        self._test = test
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

        self._name = name
```
##### Has-Functions
Has-Functions will be generated following a template like so:
```python
    def has_test(self) -> bool:
        """Generated has function for _test"""
        if self._test is None:
            return False
        return True
```
##### StrictPrivacy

adds leading underscores to fields. Can be configured to use double underscore with `UseDoubleUnderscore`

#### Naming Convention

Control the casing style of the generated code using `NamingConvention`.
Supported values: `"snake_case"` and `"camelCase"`

#### Import Mode

The `ImportMode` setting controls how the metamodel resolver handles imports and references.

**`"merge"` mode (default):**
- Used for file-based metamodel composition
- Imports are specified as file paths (e.g., `"path/to/submodel.json"`)
- Merges referenced submodels into the main metamodel
- All class/enum references must be resolvable within the merged model
- **Example import_link:** `"models/customer.json"` or `"C:/models/order.json"`

**`"import"` mode:**
- Used for module-based external references
- Imports are specified as Python module names (e.g., `"customer_service.models"`)
- Does NOT merge external submodels (assumes they're provided as installed Python packages)
- Local classes/enums within the model are still resolved
- External module imports remain unresolved by design (will be imported at runtime)
- **Example import_link:** `"customer_service.models"` or `"models.customer"`

**Error Handling:** If you see error messages about mismatched import modes, verify that your metamodel's `import_link` values match your configured `ImportMode`:
- File paths (e.g., `".json"`) require `ImportMode: "merge"`
- Module names (e.g., `"package.module"`) require `ImportMode: "import"`

#### Other Options

- `AllowUnreachableClasses` - permits classes not reachable from root class ("true" or "false")
- `RelativeImports` - generates relative imports in output code ("true" or "false")
- `Inheritance` - inheritance strategy: `"native"` or `"manual"`
- `ExplicitTypeSafety` - enforces strict type hints ("true" or "false")
- `UseDoubleUnderscore` - uses double underscore for private attributes ("true" or "false")

## Metamodel Structure

### Import Links Configuration

When authoring your JSON metamodel, use the `import_link` field to reference external content:

**For merge mode (file-based submodels):**
```json
{
  "name": "Order",
  "associations": [
    {
      "name": "customer",
      "target": "Customer",
      "import_link": "models/customer.json"
    }
  ]
}
```

**For import mode (Python module references):**
```json
{
  "name": "Order",
  "associations": [
    {
      "name": "customer",
      "target": "Customer",
      "import_link": "customer_service.models"
    }
  ]
}
```

### Local vs. External References

In `import` mode, you can reference both local and external targets:

```json
{
  "name": "Order",
  "associations": [
    {
      "name": "items",
      "target": "OrderItem",
      "association_type": "COMPOSITION"
      // No import_link: OrderItem is defined locally in this model
    },
    {
      "name": "customer",
      "target": "Customer",
      "import_link": "customer_service.models"
      // With import_link: Customer comes from external module
    }
  ]
}
```

Local references (without `import_link`) are automatically resolved within the model.
External module references remain unresolved and will be imported at runtime.


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

## Licensing

This project uses the BSD 3-Clause License.
