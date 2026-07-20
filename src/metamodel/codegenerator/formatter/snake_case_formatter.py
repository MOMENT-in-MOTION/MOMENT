from typing import Callable

from .formatter import Formatter
from .case_conversion import to_snake_case
from ..mapper import FieldDescriptor


class SnakeCaseFormatter(Formatter):
    """
    Formats descriptors to the snake_case convention:

    - class names  → PascalCase
    - field names  → snake_case
    - enum type    → PascalCase
    - enum members → UPPER_SNAKE_CASE
    """

    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        """Format a field name to snake case convention."""
        field_descriptor.field_name = to_snake_case(field_descriptor.field_name)
