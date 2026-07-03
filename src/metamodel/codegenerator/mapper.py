from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from ...shared.load_json_as_dict import load_json_as_dict

from ...metameta.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    Association,
    TypeOptions,
    Attribute,
    MetaModel,
    MultiplicityOptions
)

class Descriptor(ABC):
    """
    Abstract base for all template descriptors.
    """


@dataclass(eq=True)
class FieldDescriptor(Descriptor):
    """
    Describes a single field on a generated class.

    Stores the raw building blocks separately so that renaming a class
    (base_type) never corrupts the multiplicity wrapping, and so that
    default formatting can inspect each part independently.

    Attributes:
        field_name:       Python identifier for the field.
        base_type:        The unwrapped type name, e.g. 'str', 'MyClass'.
        multiplicity:     Cardinality of the field.
        default:          Raw default value string from the metamodel, or None.
        is_association:   True when derived from an Association.
        is_meta_enum:     True when base_type refers to a MetaEnum.
        association_kind: 'composition', 'reference', or None.
    """
    field_name: str
    base_type: str
    multiplicity: MultiplicityOptions
    is_association: bool
    is_meta_enum: bool
    association_kind: str | None
    default: str | None


    @property
    def type_hint(self) -> str:
        """Fully resolved type annotation, e.g. 'list[MyClass] | None'."""
        t = self.base_type
        if self.multiplicity.is_list:
            t = f"list[{t}]"
        if self.multiplicity.is_optional:
            t = f"{t} | None"
        return t

    @property
    def has_default(self) -> bool:
        return self.multiplicity.is_optional or self.default is not None

    @property
    def rendered_default(self) -> str | None:
        """Default expression ready for code generation, or None if omitted."""
        if self.multiplicity.is_optional and self.default is None:
            return "None"
        if self.default is None:
            return None
        if self.multiplicity.is_list:
            return self._render_list_default(self.default)
        return self._render_scalar_default(self.default)

    def _render_scalar_default(self, value: str) -> str:
        if self.is_meta_enum:
            return f"{self.base_type}.{value}"
        if self.base_type in ("str",):
            return f'"{value}"'
        # int, bool is emited as-is
        return value

    def _render_list_default(self, values: list[str] | str) -> str:
        items = ", ".join(self._render_scalar_default(v) for v in values)
        return f"[{items}]"


@dataclass(eq=True)
class ClassDescriptor(Descriptor):
    """
    Describes a generated dataclass.
    Attributes:
        class_name:     The Python class name.
        fields:         Ordered list of field descriptors.
        sorted_fields:  Fields ordered so required fields precede optional ones
                        (a dataclass constraint).
    """
    class_name: str
    fields: list[FieldDescriptor]

    @property
    def sorted_fields(self) -> list[FieldDescriptor]:
        """Required fields first, then fields with defaults."""
        return sorted(self.fields, key=lambda f: f.has_default)


@dataclass(eq=True)
class EnumDescriptor(Descriptor):
    """
    Describes a generated Enum class.

    Attributes:
        enum_name: The Python class name.
        options:   The enum member names and values.
                   In a dictionary where each key is the member name
                   and each value the member value.
    """
    enum_name: str
    options: dict[str,str]


@dataclass
class TemplateContext:
    """
    The top-level object passed into every Jinja2 template.

    Bundles all descriptors that a template may need, keeping the template
    environment free of metamodel types.

    Attributes:
        classes: All class descriptors, in the order they appear in the
                 metamodel (dependency ordering is the caller's responsibility).
        enums:   All enum descriptors, in declaration order.
    """
    classes: list[ClassDescriptor]
    enums: list[EnumDescriptor]


def resolve_primitive_type_or_meta_enum(type_option: TypeOptions) -> tuple[str, bool]:
    if isinstance(type_option, MetaEnum):
        return type_option.name, True
    if type_option in TypeOptions:
        return type_option.value, False
    raise TypeError(f"Expected TypeOptions enum or MetaEnum, got {type_option}")


def field_descriptor_from_attribute(attribute: Attribute) -> FieldDescriptor:
    print(f"Creating Field with the title: {attribute.name}")
    base_type, is_meta_enum = resolve_primitive_type_or_meta_enum(attribute.attribute_type)
    multiplicity = MultiplicityOptions(attribute.multiplicity or "ANY")

    return FieldDescriptor(
        field_name=attribute.name,
        base_type=base_type,
        multiplicity=multiplicity,
        default=attribute.default_value,
        is_meta_enum=is_meta_enum,
        is_association=False,
        association_kind=None,
    )


def resolve_association(association: str) -> str:
    """
    Normalize an association kind string to a canonical lower-case form.

    Args:
        association: The raw association kind string.
    """
    return association.lower()


def field_descriptor_from_association(association: Association | OpenAssociation) -> FieldDescriptor:
    """
    Build a FieldDescriptor for a class association (reference to another class).

    Resolves the association's multiplicity against the target class name to
    produce the appropriate type hint and default value, then wraps everything
    in a FieldDescriptor.

    Args:
        association: The Association instance from the meta-model.
    """
    print(f"Creating Field with the title: {association.name}")
    multiplicity = MultiplicityOptions(association.multiplicity or "ANY")

    return FieldDescriptor(
        field_name=association.name,
        base_type=association.association_target.name,
        multiplicity=multiplicity,
        default=None,
        is_meta_enum=False,
        is_association=True,
        association_kind=resolve_association(association.association_type),
    )


def create_class_descriptor(cls: MetaClass) -> ClassDescriptor:
    """
    Build a ClassDescriptor for a meta-model class.

    Iterates over all attributes and associations of the given MetaClass,
    converting each to a FieldDescriptor and collecting them into a single
    ClassDescriptor.

    Args:
        cls: The MetaClass instance to convert.
    """
    print(f"Creating Class-View with the title: {cls.name}")
    class_view = ClassDescriptor(class_name=cls.name, fields=[])

    for attribute in cls.attributes:
        class_view.fields.append(field_descriptor_from_attribute(attribute))

    for association in cls.associations:
        class_view.fields.append(field_descriptor_from_association(association))

    return class_view


def create_enum_descriptor(enum: MetaEnum):
    """
    Build an EnumDescriptor for a meta-model enumeration.

    Args:
        enum: The MetaEnum instance to convert.
    """
    print(f"Creating Enum-View with the title: {enum.name}")
    enum_values: dict[str, str] = {}
    for meta_enum_literal in enum.values:
        enum_values[meta_enum_literal.name] = meta_enum_literal.value
    return EnumDescriptor(enum_name=enum.name, options=enum_values)


def create_descriptors(meta_model: MetaModel) -> dict[str, list[ClassDescriptor]|list[EnumDescriptor]]:
    """
    Convert an entire MetaModel into a dictionary of class and enum descriptors.

    Iterates over all classes and enumerations in the meta-model, building a
    ClassDescriptor for each class and an EnumDescriptor for each enum.

    Args:
        meta_model: The MetaModel instance containing all classes and enums.
    """
    class_views: list[ClassDescriptor] = []
    enum_views: list[EnumDescriptor] = []

    for cls in meta_model.classes:
        class_views.append(create_class_descriptor(cls))

    for enum in meta_model.enums:
        enum_views.append(create_enum_descriptor(enum))

    return {"classes": class_views, "enums": enum_views}
