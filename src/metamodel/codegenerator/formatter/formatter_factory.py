from .camel_case_formatter import CamelCaseFormatter
from .snake_case_formatter import SnakeCaseFormatter
from .i_formatter import Formatter

def get_formatter(format_style: str) -> Formatter:
    """
    Retrieves a formatter instance based on the specified naming convention.

    Args:
        format_style: The casing style requested (e.g., "snake_case", "camelCase").

    Returns:
        An instance of a concrete Formatter strategy.

    Raises:
        ValueError: If `format_style` does not match any registered formatter.
    """
    formatters = {
        "snake_case": SnakeCaseFormatter(),
        "camelCase":  CamelCaseFormatter(),
    }
    formatter = formatters.get(format_style)

    if formatter is None:
        raise ValueError(f"Unknown format style: '{format_style}'")

    return formatter
