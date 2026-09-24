# disable error: Too many positional arguments
# pylint: disable=R0917

from src.metameta.m_m_m_classes import Multiplicity
from src.metamodel.codegenerator.mapper import (
    ClassDescriptor,
    FieldDescriptor,
    EnumDescriptor,
)

DEFAULT_CONFIG = {
    "GenerateGetters": "true",
    "GenerateSetters": "true",
    "GenerateConstructors": "true",
    "GenerateHasFunctions": "true",
    "StrictPrivacy": "true",
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
    "AllowUnreachableClasses": "false",
    "RelativeImports": "true",
    "Inheritance": "native",
    "ImportMode": "merge",
}


def make_grouped_import_model() -> dict:
    """Return a model with multiple imported symbols from one module."""
    return {
        "name": "DemoModel",
        "enums": [],
        "classes": [
            {
                "name": "DemoModel",
                "attributes": [],
                "associations": [
                    {
                        "name": "owner",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Person",
                        "import_link": "models.person",
                    },
                    {
                        "name": "driver",
                        "multiplicity": "[1]",
                        "association_type": "REFERENCE",
                        "target": "Driver",
                        "import_link": "models.person",
                    },
                ],
                "inherits": [],
            }
        ],
    }


def make_field(
    name: str = "my_field",
    base_type: str = "MyType",
    multiplicity: Multiplicity = Multiplicity(1, 1),
    is_association: bool = False,
    is_meta_enum: bool = False,
    association_kind: str | None = None,
    default=None,
) -> FieldDescriptor:
    return FieldDescriptor(
        field_name=name,
        base_type=base_type,
        multiplicity=multiplicity,
        is_association=is_association,
        is_meta_enum=is_meta_enum,
        association_kind=association_kind,
        default=default,
    )


def make_class(
    name: str = "my_class", fields: list[FieldDescriptor] | None = None
) -> ClassDescriptor:
    return ClassDescriptor(
        class_name=name,
        fields=fields or [],
    )


def make_enum(name: str = "my_enum", options: dict | None = None) -> EnumDescriptor:
    return EnumDescriptor(
        enum_name=name,
        options=options or {"option_one": "value_one", "option_two": "value_two"},
    )
