from .camel_case_formatter import CamelCaseFormatter
from .snake_case_formatter import SnakeCaseFormatter
from .i_formatter import Formatter

def get_formatter(format_style: str) -> Formatter:
    formatters = {
        "snake_case": SnakeCaseFormatter(),
        "camelCase":  CamelCaseFormatter(),
    }
    formatter = formatters.get(format_style)

    if formatter is None:
        raise ValueError(f"Unknown format style: '{format_style}'")

    return formatter
