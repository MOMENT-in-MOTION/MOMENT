# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

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

