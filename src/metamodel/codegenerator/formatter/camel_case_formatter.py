from typing import Callable

from .formatter import Formatter
from .case_conversion import to_camel_case

class CamelCaseFormatter(Formatter):
    """Formats descriptors to the camelCase convention:
        - class names  → PascalCase
        - field names  → camelCase
        - enum type    → PascalCase
        - enum members → UPPER_SNAKE_CASE
    """

    @property
    def field_name_formatter(self) -> Callable[[str], str]:
        return to_camel_case
