# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations

class ImportedRoot():
    """
    Generated dataclass for ImportedRoot
    Attributes:
        _imported_meta_class_dummy_1: ImportedMetaClassDummy1        _name: str = "root"    """
    _imported_meta_class_dummy_1: ImportedMetaClassDummy1
    _name: str = "root"

    def __init__(self, imported_meta_class_dummy_1: ImportedMetaClassDummy1, name: str = "root") -> None:
        """Generated constructor for ImportedRoot"""
        self._imported_meta_class_dummy_1 = imported_meta_class_dummy_1
        self._name = name

    def get_imported_meta_class_dummy_1(self) -> ImportedMetaClassDummy1:
        """Generated getter for _imported_meta_class_dummy_1"""
        if self._imported_meta_class_dummy_1 is None:
            raise ValueError("Field '_imported_meta_class_dummy_1' has not been initialized.")
        return self._imported_meta_class_dummy_1

    def set_imported_meta_class_dummy_1(self, value: ImportedMetaClassDummy1) -> None:
        """
        Generated setter for _imported_meta_class_dummy_1

        Args:
            value: The new value to assign to the "_imported_meta_class_dummy_1" attribute
        """
        if not isinstance(value, ImportedMetaClassDummy1):
            raise TypeError(f"Expected type ImportedMetaClassDummy1 for field '_imported_meta_class_dummy_1', got {type(value)}")
        self._imported_meta_class_dummy_1 = value

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

class ImportedMetaClassDummy1():
    """
    Generated dataclass for ImportedMetaClassDummy1
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for ImportedMetaClassDummy1"""
        self._name = name

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

