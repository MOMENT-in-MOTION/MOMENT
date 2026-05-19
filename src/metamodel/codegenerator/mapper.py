from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from shared.load_json_as_dict import load_json_as_dict

# pylint: disable=W0614, W0401
from metameta.m_m_m_classes import *

class Descriptor(ABC):
    """
    Abstract base for all template descriptors.
    """


@dataclass(eq=True)
class FieldDescriptor(Descriptor):
    """
    Describes a single field (attribute or association) on a generated class.
    Attributes:
        field_name:         The Python identifier used as the field name.
        type_hint:          The fully resolved type annotation string,
                            e.g. 'str', 'list[str]', 'str | None'.
        default:            The default value expression as a string if explicitly
                            set, None if no default was provided, "None" if the
                            field is optional (e.g. 'ZERO_OR_ONE').
        is_association:     True when this field was derived from an Association.
        association_kind:   The association kind ('composition', 'reference'), or None for
                            plain attributes.
    """
    field_name: str
    type_hint: str
    is_association: bool
    is_meta_enum: bool
    association_kind: str | None
    default: str | None

    @property
    def has_default(self) -> bool:
        """True if this field has an explicit default (including "None" when optional)."""
        return self.default is not None

    @property
    def rendered_default(self) -> str | None:
        """Returns the default value formatted for use in generated code."""
        if self.default == "None":
            return None
        if "list" in self.type_hint:
            return build_list_default(self.default, self.type_hint, self.is_meta_enum)
        return build_default(self.default, self.type_hint, self.is_meta_enum)

def build_default(default_value: str, type_hint: str, is_meta_enum: bool) -> str:
    if is_meta_enum:
        return f'{type_hint}.{default_value}'
    if type_hint in ("str", "str | None"):
        return f'"{default_value}"'
    if type_hint in ("bool", "bool | None"):
        return f'{default_value}'
    if type_hint in ("int", "int | None"):
        return f'{default_value}'
    return f'{default_value}'

def build_list_default(default_values: list[str] | str, type_hint: str, is_meta_enum: bool) -> str:

    list_default = "["
    for val in default_values:
        default_value = build_default(val, type_hint[5:-1], is_meta_enum)
        list_default += f"{default_value}, "
    return list_default[:-2] + "]"


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


def resolve_primitive_type_or_meta_enum(type_option: TypeOptions) -> str:
    if isinstance(type_option, MetaEnum):
        return type_option.name, True
    if type_option in TypeOptions:
        return type_option.value, False
    raise TypeError(f"Expected TypeOptions enum or MetaEnum, got {type_option}")

def resolve_multiplicity_and_default(
    multiplicity: str,
    type_option: str,
    default: str | None = None
) -> tuple[str, str | None]:
    """
    Resolves the type hint and default value for a field based on its multiplicity.

    Args:
        multiplicity:   How many instances of the type are allowed:
                            - "ONE"         → exactly one, required (e.g. `str`)
                            - "AT_LEAST_ONE"→ one or more, required (e.g. `list[str]`)
                            - "ANY"         → zero or more, optional (e.g. `list[str] | None`)
                            - "ZERO_OR_ONE" → zero or one, optional (e.g. `str | None`)
                            - "OPTIONAL"    → same as ZERO_OR_ONE
                            - None          → defaults to ANY behaviour
        type_option:    The base Python type name to wrap, e.g. `"str"`, `"int"`, `"MyClass"`.
        default:        The default value as a string, e.g. `"42"`, `"MyClass"`.
                        If None and the field is optional, defaults to `"None"`.
                        If None and the field is required (ONE, AT_LEAST_ONE), no default is set.

    Returns:
        A tuple of (type_hint, default_value) where:
            - type_hint     is the fully resolved type annotation string
            - default_value is the default expression string, or None if no default applies
    """
    optional_default = "None" if default is None else default

    match multiplicity:
        case "ONE":
            return f"{type_option}", default
        case "AT_LEAST_ONE":
            return f"list[{type_option}]", default
        case "ANY":
            return f"list[{type_option}] | None", optional_default
        case "ZERO_OR_ONE":
            return f"{type_option} | None", optional_default
        case "OPTIONAL":
            return f"{type_option} | None", optional_default
        case None:
            return f"list[{type_option}] | None", optional_default
        case _:
            raise TypeError(
                f"Unknown multiplicity: {multiplicity} is not a valid multiplicity!"
            )


def field_view_from_attribute(attribute: Attribute) -> FieldDescriptor:
    """
    Build a FieldDescriptor for a class attribute (non-association).

    Resolves the attribute's multiplicity and primitive type to produce the
    appropriate type hint and default value, then wraps everything in a
    FieldDescriptor.

    Args:
        attribute: The Attribute instance from the meta-model.
    """
    print(f"Creating Field-View with the title: {attribute.name}")
    type_hint, is_meta_enum = resolve_primitive_type_or_meta_enum(attribute.attribute_type)
    type_hint, default = resolve_multiplicity_and_default(
        attribute.multiplicity,
        type_hint,
        attribute.default_value
    )

    return FieldDescriptor(
        field_name=attribute.name,
        type_hint=type_hint,
        default=default,
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


def field_view_from_association(association: Association) -> FieldDescriptor:
    """
    Build a FieldDescriptor for a class association (reference to another class).

    Resolves the association's multiplicity against the target class name to
    produce the appropriate type hint and default value, then wraps everything
    in a FieldDescriptor.

    Args:
        association: The Association instance from the meta-model.
    """
    print(f"Creating Field-View with the title: {association.name}")
    type_hint, default = resolve_multiplicity_and_default(
        association.multiplicity,
        association.association_target.name
    )

    return FieldDescriptor(
        field_name=association.name,
        type_hint=type_hint,
        default=default,
        is_association=True,
        association_kind=resolve_association(association.association_type),
        is_meta_enum=False
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
        class_view.fields.append(field_view_from_attribute(attribute))

    for association in cls.associations:
        class_view.fields.append(field_view_from_association(association))

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


def create_descriptors(meta_model: MetaModel) -> dict[str, list[Descriptor]]:
    """
    Convert an entire MetaModel into a dictionary of class and enum descriptors.

    Iterates over all classes and enumerations in the meta-model, building a
    ClassDescriptor for each class and an EnumDescriptor for each enum.

    Args:
        meta_model: The MetaModel instance containing all classes and enums.
    """
    class_views: list[ClassDescriptor] = []
    enum_views: list[EnumDescriptor] = []

    ApiConfig = load_json_as_dict(path=Path("src/ApiConfig.json"))

    for cls in meta_model.classes:
        class_views.append(create_class_descriptor(cls))

    for enum in meta_model.enums:
        enum_views.append(create_enum_descriptor(enum))

    return {"classes": class_views, "enums": enum_views, "ApiConfig": ApiConfig}
