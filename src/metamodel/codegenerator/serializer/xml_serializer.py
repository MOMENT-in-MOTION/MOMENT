from xml.etree import ElementTree as ET
from xml.dom import minidom

from .serializer import Serializer
from ..mapper import Visitor, ClassDescriptor, FieldDescriptor, EnumDescriptor


class XmlSerializer(Visitor):
    """
    Serializes a full context (classes, enums) into a pretty-printed XML string.

    Builds an ElementTree incrementally as descriptors are visited, then renders
    the result via minidom for human-readable indentation.
    """

    def __init__(self):
        # Root element that holds all sections of the context
        self._root = ET.Element("context")
        self._classes_el = ET.SubElement(self._root, "classes")
        self._enums_el = ET.SubElement(self._root, "enums")

        # Tracks the <class> element currently being populated by visit_field
        self._current_class_el: ET.Element | None = None

    @property
    def file_extension(self) -> str:
        return "xml"

    def visit_class(self, class_descriptor: ClassDescriptor) -> None:
        """Open a new <class> element and record it so visit_field can append to it."""
        self._current_class_el = ET.SubElement(self._classes_el, "class")
        self._current_class_el.set("name", class_descriptor.class_name)

        for field in class_descriptor.fields:
            self.visit_field(field)

    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        """Append a <field> element with all descriptor attributes to the current class."""
        field_el = ET.SubElement(self._current_class_el, "field")
        field_el.set("name", field_descriptor.field_name)
        field_el.set("base_type", field_descriptor.base_type)
        field_el.set("multiplicity", field_descriptor.multiplicity.value)
        field_el.set("is_association", str(field_descriptor.is_association).lower())
        field_el.set("is_meta_enum", str(field_descriptor.is_meta_enum).lower())

        # Optional attributes are only written when present
        if field_descriptor.association_kind is not None:
            field_el.set("association_kind", field_descriptor.association_kind)
        if field_descriptor.default is not None:
            field_el.set("default", str(field_descriptor.default))

    def visit_enum(self, enum_descriptor: EnumDescriptor) -> None:
        """Serialize an enum and all its key/value options as <option> children."""
        enum_el = ET.SubElement(self._enums_el, "enum")
        enum_el.set("name", enum_descriptor.enum_name)

        for key, value in enum_descriptor.options.items():
            option_el = ET.SubElement(enum_el, "option")
            option_el.set("key", key)
            option_el.set("value", value)

    def append_api_config(self, api_config: dict) -> None:
        """Serialize the API config dictionary as <entry> elements under <api_config>."""
        config_el = ET.SubElement(self._root, "api_config")

        for key, value in api_config.items():
            entry_el = ET.SubElement(config_el, "entry")
            entry_el.set("key", key)
            entry_el.set("value", value)

    def render(self) -> str:
        """Render the accumulated XML tree as an indented, human-readable string."""
        raw = ET.tostring(self._root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="  ")
