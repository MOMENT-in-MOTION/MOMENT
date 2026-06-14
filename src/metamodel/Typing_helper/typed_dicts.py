from __future__ import annotations

from typing import TypedDict
from typing_extensions import NotRequired


class ImportableDict(TypedDict):
    import_: NotRequired[str]


class MetaModelInfoDict(TypedDict):
    prefix: str
    model_dict: MetaModelDict
    merged: bool


class MetaModelDict(TypedDict):
    name: str
    enums: list[MetaEnumDict]
    classes: list[MetaClassDict]


class MetaClassDict(TypedDict):
    name: str
    attributes: list[MetaAttributesDict]
    associations: list[MetaAssociationsDict]


class MetaAttributesDict(ImportableDict):
    name: str
    attribute_type: str
    multiplicity: str
    default_value: NotRequired[str | int]


class MetaAssociationsDict(ImportableDict):
    name: str
    multiplicity: str
    association_type: str
    target: str


class MetaEnumLiteralDict(TypedDict):
    name: str
    value: str


class MetaEnumDict(TypedDict):
    name: str
    values: list[str | MetaEnumLiteralDict]