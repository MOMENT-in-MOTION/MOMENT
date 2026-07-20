from typing import Callable

from .formatter import Formatter
from .case_conversion import to_camel_case
from ..mapper import FieldDescriptor


class CamelCaseFormatter(Formatter):
    """
    Formats descriptors to the camelCase convention:

    - class names  → PascalCase
    - field names  → camelCase
    - enum type    → PascalCase
    - enum members → UPPER_SNAKE_CASE
    """

    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        """Format a field name to camel case convention."""
        field_descriptor.field_name = to_camel_case(field_descriptor.field_name)
