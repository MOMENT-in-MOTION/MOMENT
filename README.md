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
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
    "AllowUnreachableClasses": "false",
    "RelativeImports": "true",
    "Inheritance": "native",
    "ImportMode": "merge"
}
```

### Configuration Options

#### Code Generation

Enable or disable the automatic creation of class methods using:
- `GenerateGetters` - generates getter methods
- `GenerateSetters` - generates setter methods
- `GenerateConstructors` - generates constructor methods

Each accepts a string value of either "true" or "false".

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
