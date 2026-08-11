import json

from .serializer import Serializer
from ..mapper import Visitor, ClassDescriptor, FieldDescriptor, EnumDescriptor


class JsonSerializer(Serializer):
    """
    Serializes a full context (classes, enums) into a pretty-printed JSON string.

    Builds a nested dictionary incrementally as descriptors are visited, then
    renders the result via json.dumps.
    """

    def __init__(self):
        self._output = {
            "classes": [],
            "enums": [],
            "api_config": {},
        }
        # Tracks the class dict currently being populated by visit_field
        self._current_class: dict | None = None

    @property
    def file_extension(self) -> str:
        return "json"

    def visit_class(self, class_descriptor: ClassDescriptor) -> None:
        """Open a new class entry, append it to the output, then visit all its fields."""
        self._current_class = {
            "class_name": class_descriptor.class_name,
            "fields": [],
        }
        self._output["classes"].append(self._current_class)

        for field in class_descriptor.fields:
            self.visit_field(field)

    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        """Append a field entry with all descriptor attributes to the current class."""
        self._current_class["fields"].append({
            "field_name": field_descriptor.field_name,
            "base_type": field_descriptor.base_type,
            "multiplicity": field_descriptor.multiplicity.value,
            "is_association": field_descriptor.is_association,
            "is_meta_enum": field_descriptor.is_meta_enum,
            "association_kind": field_descriptor.association_kind,
            "default": field_descriptor.default,
        })

    def visit_enum(self, enum_descriptor: EnumDescriptor) -> None:
        """Append an enum entry with its key/value options to the output."""
        self._output["enums"].append({
            "enum_name": enum_descriptor.enum_name,
            "options": enum_descriptor.options,
        })

    def append_api_config(self, api_config: dict) -> None:
        """Store the API config dictionary directly in the output."""
        self._output["api_config"] = api_config

    def render(self) -> str:
        """Render the accumulated context as an indented JSON string."""
        return json.dumps(self._output, indent=2)
