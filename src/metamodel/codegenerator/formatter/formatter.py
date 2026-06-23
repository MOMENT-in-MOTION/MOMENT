from abc import ABC, abstractmethod
from typing import Callable

from ....metameta.m_m_m_classes import TypeOptions

from .case_conversion import to_pascal_case, to_upper_snake_case


class Formatter(ABC):
    """
    Base formatter implementing the Template Method and Strategy patterns.

    Provides a shared execution template for formatting descriptors, while
    delegating the specific naming conventions to concrete subclasses.
    """

    @property
    def ignored_types(self) -> set[str]:
        """Dynamically fetch all types defined in TypeOptions to ignore."""
        return {e.value for e in TypeOptions}

    @property
    @abstractmethod
    def field_name_formatter(self) -> Callable[[str], str]:
        """Subclasses must return the casing function (e.g., to_snake_case)."""

    def format_descriptors(self, context: dict) -> dict:
        """The shared template method."""
        for cls in context["classes"]:
            cls.class_name = to_pascal_case(cls.class_name)

            for field in cls.fields:
                # Dynamically use the subclass's chosen formatter
                field.field_name = self.field_name_formatter(field.field_name)

                if field.base_type not in self.ignored_types:
                    field.base_type = to_pascal_case(field.base_type)

        for en in context["enums"]:
            en.enum_name = to_pascal_case(en.enum_name)
            en.options = {
                to_upper_snake_case(key): to_upper_snake_case(value)
                for key, value in en.options.items()
            }

        return context
