from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from shared.load_json_as_dict import load_json_as_dict

# pylint: disable=W0614, W0401
from metameta.api.m_m_m_classes import *

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
        if self.type_hint in ("str", "str | None"):
            return f'"{self.default}"'
        if self.type_hint in ("list[str]", "list[str] | None"):
            return f'["{self.default}"]'
        if "list" in self.type_hint:
            return f'[{self.default}]'
        return self.default


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
        options:   The enum member names.
                   Each becomes both the member name and its string value,
                   e.g. ``IN = "IN"``.
    """
    enum_name: str
    options: list[str]


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

# ---------------------------------------------------------------------------
# Build ClassViews
# ---------------------------------------------------------------------------


def resolve_primitive_type(type_option: str) -> str:
    match type_option:
        case "INT":
            return "int"
        case "BOOL":
            return "bool"
        case "STRING":
            return "str"
        case _:
            raise TypeError(
                f"Unknown primitive type: {type_option}. Expected 'INT', 'BOOL' or 'STRING'."
            )

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
    print(f"Creating Field-View with the title: {attribute.name}")
    type_hint, default = resolve_multiplicity_and_default(
        attribute.multiplicity,
        resolve_primitive_type(attribute.type),
        attribute.default_value
    )

    return FieldDescriptor(
        field_name=attribute.name,
        type_hint=type_hint,
        default=default,
        is_association=False,
        association_kind=None,
    )


def resolve_association(association: str):
    return association.lower()


def field_view_from_association(association: Association) -> FieldDescriptor:
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
        association_kind=resolve_association(association.association),
    )


def create_class_descriptor(cls: MetaClass) -> ClassDescriptor:
    print(f"Creating Class-View with the title: {cls.name}")
    class_view = ClassDescriptor(class_name=cls.name, fields=[])

    for attribute in cls.attributes:
        class_view.fields.append(field_view_from_attribute(attribute))

    for association in cls.associations:
        class_view.fields.append(field_view_from_association(association))

    return class_view


# ---------------------------------------------------------------------------
# Build EnumViews
# ---------------------------------------------------------------------------


def create_enum_descriptor(enum: MetaEnum):
    print(f"Creating Enum-View with the title: {enum.name}")
    return EnumDescriptor(enum_name=enum.name, options=enum.values)


# ---------------------------------------------------------------------------
# Collect Views
# ---------------------------------------------------------------------------


def create_descriptors(meta_model: MetaModel) -> dict[str, list[Descriptor]]:
    class_views: list[ClassDescriptor] = []
    enum_views: list[EnumDescriptor] = []

    api_config = load_json_as_dict(path=Path("src/api_config.json"))

    for cls in meta_model.classes:
        class_views.append(create_class_descriptor(cls))

    for enum in meta_model.enums:
        enum_views.append(create_enum_descriptor(enum))

    return {"classes": class_views, "enums": enum_views, "api_config": api_config}
