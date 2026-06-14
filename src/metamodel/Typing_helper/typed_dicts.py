from __future__ import annotations
from typing import TypedDict
from typing_extensions import NotRequired


class ImportableDict(TypedDict):
    """A base class for dictionaries that can contain an import key."""
    import_: NotRequired[str]


class MetaModelInfoDict(TypedDict):
    """A dictionary containing the prefix, model dictionary, and merge status of a Meta-Model."""
    prefix: str
    model_dict: MetaModelDict
    merged: bool


class MetaModelDict(TypedDict):
    """A dictionary containing the name, enums, and classes of a Meta-Model."""
    name: str
    enums: list[MetaEnumDict]
    classes: list[MetaClassDict]


class MetaClassDict(TypedDict):
    """A dictionary containing the name, attributes, and associations of a Meta-Class."""
    name: str
    attributes: list[MetaAttributesDict]
    associations: list[MetaAssociationsDict]


class MetaAttributesDict(ImportableDict):
    """A dictionary containing the name, type, multiplicity, and default value of a Meta-Class attribute."""
    name: str
    attribute_type: str
    multiplicity: str
    default_value: NotRequired[str | int]


class MetaAssociationsDict(ImportableDict):
    """A dictionary containing the name, multiplicity, type, and target of a Meta-Class association."""
    name: str
    multiplicity: str
    association_type: str
    target: str


class MetaEnumLiteralDict(TypedDict):
    """A dictionary containing the name and value of a Meta-Enum literal."""
    name: str
    value: str


class MetaEnumDict(TypedDict):
    """A dictionary containing the name and values of a Meta-Enum."""
    name: str
    values: list[str | MetaEnumLiteralDict]
