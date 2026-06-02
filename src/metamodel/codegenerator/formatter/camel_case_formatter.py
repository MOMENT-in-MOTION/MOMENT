from .i_formatter import Formatter
from .helpers import to_pascal_case, to_camel_case, to_upper_snake_case

class CamelCaseFormatter(Formatter):
    """Formats descriptors to the camelCase convention:
        - class names  → PascalCase
        - field names  → camelCase
        - enum type    → PascalCase
        - enum members → UPPER_SNAKE_CASE
    """

    def format_descriptors(self,  context: dict) -> dict:
        """Returns formatted descriptors in camelCase format."""
        for cls in context["classes"]:
            cls.class_name = to_pascal_case(cls.class_name)
            for field in cls.fields:
                field.field_name = to_camel_case(field.field_name)
                field.type_hint = to_pascal_case(field.type_hint)

        for en in context["enums"]:
            en.enum_name = to_pascal_case(en.enum_name)
            en.options = {
                to_upper_snake_case(key): value
                for key, value in en.options.items()
            }

        return context
