# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

class RootEntity():
    """
    Generated dataclass for RootEntity
    Attributes:
        _single_child: SingleChild        _many_children: list[ManyChildren]        _imported_thing: ImportedThing        _name: str = "root"        _count: int = 3        _enabled: bool | None = True        _optional_reference: OptionalReference | None = None        _any_reference: list[AnyReference] | None = None        _zero_or_one_status: Status | None = Status.ACTIVE    """
    _single_child: SingleChild
    _many_children: list[ManyChildren]
    _imported_thing: ImportedThing
    _name: str = "root"
    _count: int = 3
    _enabled: bool | None = True
    _optional_reference: OptionalReference | None = None
    _any_reference: list[AnyReference] | None = None
    _zero_or_one_status: Status | None = Status.ACTIVE

    def __init__(self, single_child: SingleChild, many_children: list[ManyChildren], imported_thing: ImportedThing, name: str = "root", count: int = 3, enabled: bool | None = True, optional_reference: OptionalReference | None = None, any_reference: list[AnyReference] | None = None, zero_or_one_status: Status | None = Status.ACTIVE) -> None:
        """Generated constructor for RootEntity"""
        if not isinstance(single_child, SingleChild):
            raise TypeError(
                f"Expected 'SingleChild' for '_single_child', got {type(single_child).__name__!r}"
            )

        self._single_child = single_child
        if not isinstance(many_children, list) or not all(isinstance(i, ManyChildren) for i in many_children):
            raise TypeError(
                f"Expected 'list[ManyChildren]' for '_many_children', got {type(many_children).__name__!r}"
            )
        if len(many_children) < 1:
            raise ValueError(
                f"Field '_many_children' must have at least 1 element(s), got {len(many_children)}"
            )

        self._many_children = many_children
        if not isinstance(imported_thing, ImportedThing):
            raise TypeError(
                f"Expected 'ImportedThing' for '_imported_thing', got {type(imported_thing).__name__!r}"
            )

        self._imported_thing = imported_thing
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

        self._name = name
        if not isinstance(count, int):
            raise TypeError(
                f"Expected 'int' for '_count', got {type(count).__name__!r}"
            )

        self._count = count
        if enabled is not None:
            if not isinstance(enabled, bool):
                raise TypeError(
                    f"Expected 'bool' or None for '_enabled', got {type(enabled).__name__!r}"
                )

        self._enabled = enabled
        if optional_reference is not None:
            if not isinstance(optional_reference, OptionalReference):
                raise TypeError(
                    f"Expected 'OptionalReference' or None for '_optional_reference', got {type(optional_reference).__name__!r}"
                )

        self._optional_reference = optional_reference
        if any_reference is not None:
            if not isinstance(any_reference, list) or not all(isinstance(i, AnyReference) for i in any_reference):
                raise TypeError(
                    f"Expected 'list[AnyReference]' or None for '_any_reference', got {type(any_reference).__name__!r}"
                )

        self._any_reference = any_reference
        if zero_or_one_status is not None:
            if not isinstance(zero_or_one_status, Status):
                raise TypeError(
                    f"Expected 'Status' or None for '_zero_or_one_status', got {type(zero_or_one_status).__name__!r}"
                )

        self._zero_or_one_status = zero_or_one_status

    def get_single_child(self) -> SingleChild:
        """Generated getter for _single_child"""
        if self._single_child is None:
            raise ValueError("Field '_single_child' has not been initialized.")
        return self._single_child

    def set_single_child(self, value: SingleChild) -> None:
        """
        Generated setter for _single_child

        Args:
            value: The new value to assign to the "_single_child" attribute
        """
        if not isinstance(value, SingleChild):
            raise TypeError(
                f"Expected 'SingleChild' for '_single_child', got {type(value).__name__!r}"
            )

        self._single_child = value

    def has_single_child(self) -> bool:
        """Generated has function for _single_child"""
        if self._single_child is None:
            return False
        return True
    def get_many_children(self) -> list[ManyChildren]:
        """Generated getter for _many_children"""
        if self._many_children is None:
            raise ValueError("Field '_many_children' has not been initialized.")
        return self._many_children

    def set_many_children(self, value: list[ManyChildren]) -> None:
        """
        Generated setter for _many_children

        Args:
            value: The new value to assign to the "_many_children" attribute
        """
        if not isinstance(value, list) or not all(isinstance(i, ManyChildren) for i in value):
            raise TypeError(
                f"Expected 'list[ManyChildren]' for '_many_children', got {type(value).__name__!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"Field '_many_children' must have at least 1 element(s), got {len(value)}"
            )

        self._many_children = value

    def has_many_children(self) -> bool:
        """Generated has function for _many_children"""
        if self._many_children is None:
            return False
        return True
    def get_imported_thing(self) -> ImportedThing:
        """Generated getter for _imported_thing"""
        if self._imported_thing is None:
            raise ValueError("Field '_imported_thing' has not been initialized.")
        return self._imported_thing

    def set_imported_thing(self, value: ImportedThing) -> None:
        """
        Generated setter for _imported_thing

        Args:
            value: The new value to assign to the "_imported_thing" attribute
        """
        if not isinstance(value, ImportedThing):
            raise TypeError(
                f"Expected 'ImportedThing' for '_imported_thing', got {type(value).__name__!r}"
            )

        self._imported_thing = value

    def has_imported_thing(self) -> bool:
        """Generated has function for _imported_thing"""
        if self._imported_thing is None:
            return False
        return True
    def get_name(self) -> str:
        """Generated getter for _name"""
        if self._name is None:
            raise ValueError("Field '_name' has not been initialized.")
        return self._name

    def set_name(self, value: str) -> None:
        """
        Generated setter for _name

        Args:
            value: The new value to assign to the "_name" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True
    def get_count(self) -> int:
        """Generated getter for _count"""
        if self._count is None:
            raise ValueError("Field '_count' has not been initialized.")
        return self._count

    def set_count(self, value: int) -> None:
        """
        Generated setter for _count

        Args:
            value: The new value to assign to the "_count" attribute
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Expected 'int' for '_count', got {type(value).__name__!r}"
            )

        self._count = value

    def has_count(self) -> bool:
        """Generated has function for _count"""
        if self._count is None:
            return False
        return True
    def get_enabled(self) -> bool | None:
        """Generated getter for _enabled"""
        return self._enabled

    def set_enabled(self, value: bool | None) -> None:
        """
        Generated setter for _enabled

        Args:
            value: The new value to assign to the "_enabled" attribute
        """
        if value is not None:
            if not isinstance(value, bool):
                raise TypeError(
                    f"Expected 'bool' or None for '_enabled', got {type(value).__name__!r}"
                )

        self._enabled = value

    def has_enabled(self) -> bool:
        """Generated has function for _enabled"""
        if self._enabled is None:
            return False
        return True
    def get_optional_reference(self) -> OptionalReference | None:
        """Generated getter for _optional_reference"""
        return self._optional_reference

    def set_optional_reference(self, value: OptionalReference | None) -> None:
        """
        Generated setter for _optional_reference

        Args:
            value: The new value to assign to the "_optional_reference" attribute
        """
        if value is not None:
            if not isinstance(value, OptionalReference):
                raise TypeError(
                    f"Expected 'OptionalReference' or None for '_optional_reference', got {type(value).__name__!r}"
                )

        self._optional_reference = value

    def has_optional_reference(self) -> bool:
        """Generated has function for _optional_reference"""
        if self._optional_reference is None:
            return False
        return True
    def get_any_reference(self) -> list[AnyReference] | None:
        """Generated getter for _any_reference"""
        return self._any_reference

    def set_any_reference(self, value: list[AnyReference] | None) -> None:
        """
        Generated setter for _any_reference

        Args:
            value: The new value to assign to the "_any_reference" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, AnyReference) for i in value):
                raise TypeError(
                    f"Expected 'list[AnyReference]' or None for '_any_reference', got {type(value).__name__!r}"
                )

        self._any_reference = value

    def has_any_reference(self) -> bool:
        """Generated has function for _any_reference"""
        if self._any_reference is None:
            return False
        return True
    def get_zero_or_one_status(self) -> Status | None:
        """Generated getter for _zero_or_one_status"""
        return self._zero_or_one_status

    def set_zero_or_one_status(self, value: Status | None) -> None:
        """
        Generated setter for _zero_or_one_status

        Args:
            value: The new value to assign to the "_zero_or_one_status" attribute
        """
        if value is not None:
            if not isinstance(value, Status):
                raise TypeError(
                    f"Expected 'Status' or None for '_zero_or_one_status', got {type(value).__name__!r}"
                )

        self._zero_or_one_status = value

    def has_zero_or_one_status(self) -> bool:
        """Generated has function for _zero_or_one_status"""
        if self._zero_or_one_status is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for RootEntity"""
        result = {}
        result["single_child"] = (
            self._single_child.to_dict() if hasattr(self._single_child, "to_dict")
            else (self._single_child.value if hasattr(self._single_child, "value") else self._single_child)
        )
        result["many_children"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._many_children]
        )
        result["imported_thing"] = (
            self._imported_thing.to_dict() if hasattr(self._imported_thing, "to_dict")
            else (self._imported_thing.value if hasattr(self._imported_thing, "value") else self._imported_thing)
        )
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        result["count"] = (
            self._count.to_dict() if hasattr(self._count, "to_dict")
            else (self._count.value if hasattr(self._count, "value") else self._count)
        )
        result["enabled"] = (
            self._enabled.to_dict() if hasattr(self._enabled, "to_dict")
            else (self._enabled.value if hasattr(self._enabled, "value") else self._enabled)
            if self._enabled is not None else None
        )
        result["optional_reference"] = (
            self._optional_reference.to_dict() if hasattr(self._optional_reference, "to_dict")
            else (self._optional_reference.value if hasattr(self._optional_reference, "value") else self._optional_reference)
            if self._optional_reference is not None else None
        )
        result["any_reference"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._any_reference]
            if self._any_reference is not None else None
        )
        result["zero_or_one_status"] = (
            self._zero_or_one_status.to_dict() if hasattr(self._zero_or_one_status, "to_dict")
            else (self._zero_or_one_status.value if hasattr(self._zero_or_one_status, "value") else self._zero_or_one_status)
            if self._zero_or_one_status is not None else None
        )
        return result

class SingleChild():
    """
    Generated dataclass for SingleChild
    Attributes:
        _label: str    """
    _label: str

    def __init__(self, label: str) -> None:
        """Generated constructor for SingleChild"""
        if not isinstance(label, str):
            raise TypeError(
                f"Expected 'str' for '_label', got {type(label).__name__!r}"
            )

        self._label = label

    def get_label(self) -> str:
        """Generated getter for _label"""
        if self._label is None:
            raise ValueError("Field '_label' has not been initialized.")
        return self._label

    def set_label(self, value: str) -> None:
        """
        Generated setter for _label

        Args:
            value: The new value to assign to the "_label" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_label', got {type(value).__name__!r}"
            )

        self._label = value

    def has_label(self) -> bool:
        """Generated has function for _label"""
        if self._label is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for SingleChild"""
        result = {}
        result["label"] = (
            self._label.to_dict() if hasattr(self._label, "to_dict")
            else (self._label.value if hasattr(self._label, "value") else self._label)
        )
        return result

class ManyChildren():
    """
    Generated dataclass for ManyChildren
    Attributes:
        _index: int = 1    """
    _index: int = 1

    def __init__(self, index: int = 1) -> None:
        """Generated constructor for ManyChildren"""
        if not isinstance(index, int):
            raise TypeError(
                f"Expected 'int' for '_index', got {type(index).__name__!r}"
            )

        self._index = index

    def get_index(self) -> int:
        """Generated getter for _index"""
        if self._index is None:
            raise ValueError("Field '_index' has not been initialized.")
        return self._index

    def set_index(self, value: int) -> None:
        """
        Generated setter for _index

        Args:
            value: The new value to assign to the "_index" attribute
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Expected 'int' for '_index', got {type(value).__name__!r}"
            )

        self._index = value

    def has_index(self) -> bool:
        """Generated has function for _index"""
        if self._index is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for ManyChildren"""
        result = {}
        result["index"] = (
            self._index.to_dict() if hasattr(self._index, "to_dict")
            else (self._index.value if hasattr(self._index, "value") else self._index)
        )
        return result

class OptionalReference():
    """
    Generated dataclass for OptionalReference
    Attributes:
        _key: str    """
    _key: str

    def __init__(self, key: str) -> None:
        """Generated constructor for OptionalReference"""
        if not isinstance(key, str):
            raise TypeError(
                f"Expected 'str' for '_key', got {type(key).__name__!r}"
            )

        self._key = key

    def get_key(self) -> str:
        """Generated getter for _key"""
        if self._key is None:
            raise ValueError("Field '_key' has not been initialized.")
        return self._key

    def set_key(self, value: str) -> None:
        """
        Generated setter for _key

        Args:
            value: The new value to assign to the "_key" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_key', got {type(value).__name__!r}"
            )

        self._key = value

    def has_key(self) -> bool:
        """Generated has function for _key"""
        if self._key is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for OptionalReference"""
        result = {}
        result["key"] = (
            self._key.to_dict() if hasattr(self._key, "to_dict")
            else (self._key.value if hasattr(self._key, "value") else self._key)
        )
        return result

class AnyReference():
    """
    Generated dataclass for AnyReference
    Attributes:
        _meta: str    """
    _meta: str

    def __init__(self, meta: str) -> None:
        """Generated constructor for AnyReference"""
        if not isinstance(meta, str):
            raise TypeError(
                f"Expected 'str' for '_meta', got {type(meta).__name__!r}"
            )

        self._meta = meta

    def get_meta(self) -> str:
        """Generated getter for _meta"""
        if self._meta is None:
            raise ValueError("Field '_meta' has not been initialized.")
        return self._meta

    def set_meta(self, value: str) -> None:
        """
        Generated setter for _meta

        Args:
            value: The new value to assign to the "_meta" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_meta', got {type(value).__name__!r}"
            )

        self._meta = value

    def has_meta(self) -> bool:
        """Generated has function for _meta"""
        if self._meta is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for AnyReference"""
        result = {}
        result["meta"] = (
            self._meta.to_dict() if hasattr(self._meta, "to_dict")
            else (self._meta.value if hasattr(self._meta, "value") else self._meta)
        )
        return result

class ImportedThing():
    """
    Generated dataclass for ImportedThing
    Attributes:
        _imported_child: list[ImportedChild]        _id: int = 7        _imported_status_ref: ImportedStatus | None = None    """
    _imported_child: list[ImportedChild]
    _id: int = 7
    _imported_status_ref: ImportedStatus | None = None

    def __init__(self, imported_child: list[ImportedChild], id: int = 7, imported_status_ref: ImportedStatus | None = None) -> None:
        """Generated constructor for ImportedThing"""
        if not isinstance(imported_child, list) or not all(isinstance(i, ImportedChild) for i in imported_child):
            raise TypeError(
                f"Expected 'list[ImportedChild]' for '_imported_child', got {type(imported_child).__name__!r}"
            )
        if len(imported_child) < 1:
            raise ValueError(
                f"Field '_imported_child' must have at least 1 element(s), got {len(imported_child)}"
            )

        self._imported_child = imported_child
        if not isinstance(id, int):
            raise TypeError(
                f"Expected 'int' for '_id', got {type(id).__name__!r}"
            )

        self._id = id
        if imported_status_ref is not None:
            if not isinstance(imported_status_ref, ImportedStatus):
                raise TypeError(
                    f"Expected 'ImportedStatus' or None for '_imported_status_ref', got {type(imported_status_ref).__name__!r}"
                )

        self._imported_status_ref = imported_status_ref

    def get_imported_child(self) -> list[ImportedChild]:
        """Generated getter for _imported_child"""
        if self._imported_child is None:
            raise ValueError("Field '_imported_child' has not been initialized.")
        return self._imported_child

    def set_imported_child(self, value: list[ImportedChild]) -> None:
        """
        Generated setter for _imported_child

        Args:
            value: The new value to assign to the "_imported_child" attribute
        """
        if not isinstance(value, list) or not all(isinstance(i, ImportedChild) for i in value):
            raise TypeError(
                f"Expected 'list[ImportedChild]' for '_imported_child', got {type(value).__name__!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"Field '_imported_child' must have at least 1 element(s), got {len(value)}"
            )

        self._imported_child = value

    def has_imported_child(self) -> bool:
        """Generated has function for _imported_child"""
        if self._imported_child is None:
            return False
        return True
    def get_id(self) -> int:
        """Generated getter for _id"""
        if self._id is None:
            raise ValueError("Field '_id' has not been initialized.")
        return self._id

    def set_id(self, value: int) -> None:
        """
        Generated setter for _id

        Args:
            value: The new value to assign to the "_id" attribute
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Expected 'int' for '_id', got {type(value).__name__!r}"
            )

        self._id = value

    def has_id(self) -> bool:
        """Generated has function for _id"""
        if self._id is None:
            return False
        return True
    def get_imported_status_ref(self) -> ImportedStatus | None:
        """Generated getter for _imported_status_ref"""
        return self._imported_status_ref

    def set_imported_status_ref(self, value: ImportedStatus | None) -> None:
        """
        Generated setter for _imported_status_ref

        Args:
            value: The new value to assign to the "_imported_status_ref" attribute
        """
        if value is not None:
            if not isinstance(value, ImportedStatus):
                raise TypeError(
                    f"Expected 'ImportedStatus' or None for '_imported_status_ref', got {type(value).__name__!r}"
                )

        self._imported_status_ref = value

    def has_imported_status_ref(self) -> bool:
        """Generated has function for _imported_status_ref"""
        if self._imported_status_ref is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for ImportedThing"""
        result = {}
        result["imported_child"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._imported_child]
        )
        result["id"] = (
            self._id.to_dict() if hasattr(self._id, "to_dict")
            else (self._id.value if hasattr(self._id, "value") else self._id)
        )
        result["imported_status_ref"] = (
            self._imported_status_ref.to_dict() if hasattr(self._imported_status_ref, "to_dict")
            else (self._imported_status_ref.value if hasattr(self._imported_status_ref, "value") else self._imported_status_ref)
            if self._imported_status_ref is not None else None
        )
        return result

class ImportedChild():
    """
    Generated dataclass for ImportedChild
    Attributes:
        _value: str    """
    _value: str

    def __init__(self, value: str) -> None:
        """Generated constructor for ImportedChild"""
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_value', got {type(value).__name__!r}"
            )

        self._value = value

    def get_value(self) -> str:
        """Generated getter for _value"""
        if self._value is None:
            raise ValueError("Field '_value' has not been initialized.")
        return self._value

    def set_value(self, value: str) -> None:
        """
        Generated setter for _value

        Args:
            value: The new value to assign to the "_value" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_value', got {type(value).__name__!r}"
            )

        self._value = value

    def has_value(self) -> bool:
        """Generated has function for _value"""
        if self._value is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for ImportedChild"""
        result = {}
        result["value"] = (
            self._value.to_dict() if hasattr(self._value, "to_dict")
            else (self._value.value if hasattr(self._value, "value") else self._value)
        )
        return result

