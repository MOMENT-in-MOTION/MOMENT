# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

class ImportedThing():
    """
    Generated dataclass for ImportedThing 
    Attributes:
        _id: int = 7 
    """
    _id: int = 7

    def __init__(self, id: int = 7) -> None:
        """Generated constructor for ImportedThing"""
        self._id = id

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
            raise TypeError(f"Expected type int for field '_id', got {type(value)}")
        self._id = value

class ImportedChild():
    """
    Generated dataclass for ImportedChild 
    Attributes:
        _value: str 
    """
    _value: str

    def __init__(self, value: str) -> None:
        """Generated constructor for ImportedChild"""
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
            raise TypeError(f"Expected type str for field '_value', got {type(value)}")
        self._value = value

