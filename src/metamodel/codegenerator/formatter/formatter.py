from abc import ABC, abstractmethod
from typing import Callable

from ....metameta.m_m_m_classes import TypeOptions

from ..mapper import Visitor, ClassDescriptor, FieldDescriptor, EnumDescriptor

from .case_conversion import to_pascal_case, to_upper_snake_case


class Formatter(Visitor, ABC):
    """
    Abstract base visitor that applies naming-convention formatting to descriptors.

    Handles class and enum formatting directly; delegates field formatting to
    subclasses, which may differ in their target conventions (e.g.
    snake_case for Python, camelCase for Java).
    """

    @property
    def ignored_types(self) -> set[str]:
        """Types defined in TypeOptions that should be skipped during formatting."""
        return {e.value for e in TypeOptions}

    def visit_class(self, class_descriptor: ClassDescriptor) -> None:
        """Convert the class name to PascalCase and format all its fields."""
        class_descriptor.class_name = to_pascal_case(class_descriptor.class_name)
        
        for field in class_descriptor.fields:
            if field.base_type not in self.ignored_types:
                field.base_type = to_pascal_case(field.base_type)

            self.visit_field(field)

    @abstractmethod
    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        """Format a field name according to the target convention."""
        pass

    def visit_enum(self, enum_descriptor: EnumDescriptor) -> None:
        """Convert the enum name to PascalCase and all option keys/values to UPPER_SNAKE_CASE."""
        enum_descriptor.enum_name = to_pascal_case(enum_descriptor.enum_name)
        enum_descriptor.options = {
            to_upper_snake_case(key): to_upper_snake_case(value)
            for key, value in enum_descriptor.options.items()
        }
