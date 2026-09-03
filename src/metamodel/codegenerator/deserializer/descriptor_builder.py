"""
Rebuilds template descriptors from the dictionary shape the deserializers produce.

Both formats reduce their document to that shape, so reconstruction lives here
once rather than per format. Kept out of mapper.py deliberately: the serialized
key names are the serializers' format contract, not part of mapping meta-model
objects onto descriptors.
"""

from typing import Any

from ....metameta.m_m_m_classes import MultiplicityOptions

from ..mapper import (
    ClassDescriptor,
    EnumDescriptor,
    FieldDescriptor,
    TemplateContext,
)

from .deserializer import DeserializationError


def build_context(data: dict) -> TemplateContext:
    """
    Rebuild a TemplateContext from a parsed serialized document.

    Args:
        data: The parsed document, holding "classes" and "enums".

    Raises:
        DeserializationError: If a required key is missing.
    """
    return TemplateContext(
        classes=[
            build_class(class_data)
            for class_data in _require(data, "classes", "document")
        ],
        enums=[
            build_enum(enum_data)
            for enum_data in _require(data, "enums", "document")
        ],
    )


def build_class(data: dict) -> ClassDescriptor:
    """
    Rebuild a ClassDescriptor and all of its fields from serialized form.

    Args:
        data: A single serialized class entry.

    Raises:
        DeserializationError: If a required key is missing.
    """
    class_name = _require(data, "class_name", "class")

    return ClassDescriptor(
        class_name=class_name,
        fields=[
            build_field(field_data)
            for field_data in _require(data, "fields", f"class '{class_name}'")
        ],
    )


def build_field(data: dict) -> FieldDescriptor:
    """
    Rebuild a FieldDescriptor from its serialized form.

    Inverse of the field entries written by the serializers. The optional keys
    (association_kind, default) may be absent, since the XML serializer omits
    them when they are None.

    Args:
        data: A single serialized field entry.

    Raises:
        DeserializationError: If a required key is missing or the multiplicity
            is not a known MultiplicityOptions member.
    """
    field_name = _require(data, "field_name", "field")
    where = f"field '{field_name}'"

    raw_multiplicity = _require(data, "multiplicity", where)
    try:
        multiplicity = MultiplicityOptions(raw_multiplicity)
    except ValueError as e:
        raise DeserializationError(
            f"Unknown multiplicity '{raw_multiplicity}' in {where}"
        ) from e

    return FieldDescriptor(
        field_name=field_name,
        base_type=_require(data, "base_type", where),
        multiplicity=multiplicity,
        is_association=_require(data, "is_association", where),
        is_meta_enum=_require(data, "is_meta_enum", where),
        association_kind=data.get("association_kind"),
        default=data.get("default"),
    )


def build_enum(data: dict) -> EnumDescriptor:
    """
    Rebuild an EnumDescriptor from its serialized key/value options.

    Args:
        data: A single serialized enum entry.

    Raises:
        DeserializationError: If a required key is missing.
    """
    enum_name = _require(data, "enum_name", "enum")

    return EnumDescriptor(
        enum_name=enum_name,
        options=dict(_require(data, "options", f"enum '{enum_name}'")),
    )


def _require(data: dict, key: str, where: str) -> Any:
    """
    Fetch a required key from a serialized entry.

    Args:
        data:  The serialized entry to read from.
        key:   The key that must be present.
        where: Human readable location, used in the error message.

    Raises:
        DeserializationError: If the key is absent.
    """
    if key not in data:
        raise DeserializationError(f"Missing required key '{key}' in {where}")
    return data[key]
