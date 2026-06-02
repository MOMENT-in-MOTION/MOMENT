from typing import Callable

from .i_formatter import Formatter
from .helpers import to_snake_case


class SnakeCaseFormatter(Formatter):
    """Formats descriptors to the snake_case convention:
        - class names  → PascalCase
        - field names  → snake_case
        - enum type    → PascalCase
        - enum members → UPPER_SNAKE_CASE
    """

    @property
    def field_name_formatter(self) -> Callable[[str], str]:
        return to_snake_case
