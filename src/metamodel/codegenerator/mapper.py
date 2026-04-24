from __future__ import annotations

from metameta.api.m_m_m_classes import *
from dataclasses import dataclass
from abc import ABC


class view(ABC):
    pass


@dataclass(eq=True)
class ClassView(view):
    class_name: str
    fields: list[FieldView]


@dataclass(eq=True)
class FieldView(view):
    field_name: str
    type_hint: str
    default: str | None
    is_association: bool
    association_kind: str | None


@dataclass(eq=True)
class EnumView(view):
    enum_name: str
    options: list[str]


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


def apply_multiplicity(multiplicity: str, type_option: str) -> str:
    is_list: bool
    is_optional: bool

    match multiplicity:
        case "ONE":
            is_list = False
            is_optional = False
        case "AT_LEAST_ONE":
            is_list = True
            is_optional = False
        case "ANY":
            is_list = True
            is_optional = False
        case "ZERO_OR_ONE":
            is_list = False
            is_optional = True
        case "OPTIONAL":
            is_list = False
            is_optional = True
        case None:
            is_list = True
            is_optional = False
        case _:
            raise TypeError(
                f"The multiplicity: {multiplicity} could not be matched to one of the MetaEnums "
                "'ONE', 'AT_LEAST_ONE', 'ANY', 'ZERO_OR_ONE' or 'OPTIONAL'"
            )

    if is_list:
        type_option = f"list[{type_option}]"

    if is_optional:
        type_option = f"{type_option} | None"

    return type_option


def field_view_from_attribute(attribute: Attribute) -> FieldView:
    print(f"Creating Field-View with the title: {attribute.name}")
    type_hint: str = apply_multiplicity(
        attribute.multiplicity, resolve_primitive_type(attribute.type)
    )

    return FieldView(
        field_name=attribute.name,
        type_hint=type_hint,
        default=None,
        is_association=False,
        association_kind=None,
    )


def resolve_association(association: str):
    return association.lower()


def field_view_from_association(association: Association) -> FieldView:
    print(f"Creating Field-View with the title: {association.name}")
    type_hint: str = apply_multiplicity(
        association.multiplicity, association.associationTarget.name
    )

    return FieldView(
        field_name=association.name,
        type_hint=type_hint,
        default=None,
        is_association=True,
        association_kind=resolve_association(association.association),
    )


def create_class_view(cls: MetaClass) -> ClassView:
    print(f"Creating Class-View with the title: {cls.name}")
    class_view = ClassView(class_name=cls.name, fields=[])
    for attribute in cls.attributes:
        class_view.fields.append(field_view_from_attribute(attribute))

    for association in cls.associations:
        class_view.fields.append(field_view_from_association(association))

    return class_view


# ---------------------------------------------------------------------------
# Build EnumViews
# ---------------------------------------------------------------------------


def create_enum_view(enum: MetaEnum):
    print(f"Creating Enum-View with the title: {enum.name}")
    return EnumView(enum_name=enum.name, options=enum.values)


# ---------------------------------------------------------------------------
# Collect Views
# ---------------------------------------------------------------------------


def create_view(meta_model: MetaModel) -> dict[str, list[view]]:
    class_views: list[ClassView] = []
    enum_views: list[EnumView] = []

    for cls in meta_model.classes:
        class_views.append(create_class_view(cls))

    for enum in meta_model.enums:
        enum_views.append(create_enum_view(enum))

    return {"classes": class_views, "enums": enum_views}
