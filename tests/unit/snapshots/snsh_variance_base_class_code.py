# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

class RootEntity():
    """
    Generated dataclass for RootEntity 
    Attributes:
        _name: str = "root" 
        _count: int = 3 
        _enabled: bool | None = True 
    """
    _name: str = "root"
    _count: int = 3
    _enabled: bool | None = True

    def __init__(self, name: str = "root", count: int = 3, enabled: bool | None = True) -> None:
        """Generated constructor for RootEntity"""
        self._name = name
        self._count = count
        self._enabled = enabled

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
            raise TypeError(f"Expected type str for field '_name', got {type(value)}")
        self._name = value

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
            raise TypeError(f"Expected type int for field '_count', got {type(value)}")
        self._count = value

    def get_enabled(self) -> bool | None:
        """Generated getter for _enabled"""
        if self._enabled is None:
            raise ValueError("Field '_enabled' has not been initialized.")
        return self._enabled

    def set_enabled(self, value: bool | None) -> None:
        """
        Generated setter for _enabled

        Args:
            value: The new value to assign to the "_enabled" attribute
        """
        if value is not None:
            if not isinstance(value, bool):
                raise TypeError(f"Expected type bool or None for field '_enabled', got {type(value)}")
        self._enabled = value

class SingleChild():
    """
    Generated dataclass for SingleChild 
    Attributes:
        _label: str 
    """
    _label: str

    def __init__(self, label: str) -> None:
        """Generated constructor for SingleChild"""
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
            raise TypeError(f"Expected type str for field '_label', got {type(value)}")
        self._label = value

class ManyChildren():
    """
    Generated dataclass for ManyChildren 
    Attributes:
        _index: int = 1 
    """
    _index: int = 1

    def __init__(self, index: int = 1) -> None:
        """Generated constructor for ManyChildren"""
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
            raise TypeError(f"Expected type int for field '_index', got {type(value)}")
        self._index = value

class OptionalReference():
    """
    Generated dataclass for OptionalReference 
    Attributes:
        _key: str 
    """
    _key: str

    def __init__(self, key: str) -> None:
        """Generated constructor for OptionalReference"""
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
            raise TypeError(f"Expected type str for field '_key', got {type(value)}")
        self._key = value

class AnyReference():
    """
    Generated dataclass for AnyReference 
    Attributes:
        _meta: str 
    """
    _meta: str

    def __init__(self, meta: str) -> None:
        """Generated constructor for AnyReference"""
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
            raise TypeError(f"Expected type str for field '_meta', got {type(value)}")
        self._meta = value

