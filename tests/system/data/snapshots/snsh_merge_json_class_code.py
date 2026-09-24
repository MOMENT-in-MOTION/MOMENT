# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

class MetaModelDummy():
    """
    Generated dataclass for MetaModelDummy
    Attributes:
        _class_imported_1: ImportedMetaClassDummy1        _class_meta_class_dummy_1: MetaClassDummy1        _class_meta_class_dummy_2: MetaClassDummy2        _class_meta_reference_dummy_1: MetaReferenceDummy1        _class_meta_reference_dummy_3: list[MetaReferenceDummy3]        _enum_example_enum_1: ExampleEnum1        _name: str = "root"        _class_meta_reference_dummy_2: MetaReferenceDummy2 | None = None        _class_meta_reference_dummy_4: list[MetaReferenceDummy4] | None = None    """
    _class_imported_1: ImportedMetaClassDummy1
    _class_meta_class_dummy_1: MetaClassDummy1
    _class_meta_class_dummy_2: MetaClassDummy2
    _class_meta_reference_dummy_1: MetaReferenceDummy1
    _class_meta_reference_dummy_3: list[MetaReferenceDummy3]
    _enum_example_enum_1: ExampleEnum1
    _name: str = "root"
    _class_meta_reference_dummy_2: MetaReferenceDummy2 | None = None
    _class_meta_reference_dummy_4: list[MetaReferenceDummy4] | None = None

    def __init__(self, class_imported_1: ImportedMetaClassDummy1, class_meta_class_dummy_1: MetaClassDummy1, class_meta_class_dummy_2: MetaClassDummy2, class_meta_reference_dummy_1: MetaReferenceDummy1, class_meta_reference_dummy_3: list[MetaReferenceDummy3], enum_example_enum_1: ExampleEnum1, name: str = "root", class_meta_reference_dummy_2: MetaReferenceDummy2 | None = None, class_meta_reference_dummy_4: list[MetaReferenceDummy4] | None = None) -> None:
        """Generated constructor for MetaModelDummy"""
        if not isinstance(class_imported_1, ImportedMetaClassDummy1):
            raise TypeError(
                f"Expected 'ImportedMetaClassDummy1' for '_class_imported_1', got {type(class_imported_1).__name__!r}"
            )

        self._class_imported_1 = class_imported_1
        if not isinstance(class_meta_class_dummy_1, MetaClassDummy1):
            raise TypeError(
                f"Expected 'MetaClassDummy1' for '_class_meta_class_dummy_1', got {type(class_meta_class_dummy_1).__name__!r}"
            )

        self._class_meta_class_dummy_1 = class_meta_class_dummy_1
        if not isinstance(class_meta_class_dummy_2, MetaClassDummy2):
            raise TypeError(
                f"Expected 'MetaClassDummy2' for '_class_meta_class_dummy_2', got {type(class_meta_class_dummy_2).__name__!r}"
            )

        self._class_meta_class_dummy_2 = class_meta_class_dummy_2
        if not isinstance(class_meta_reference_dummy_1, MetaReferenceDummy1):
            raise TypeError(
                f"Expected 'MetaReferenceDummy1' for '_class_meta_reference_dummy_1', got {type(class_meta_reference_dummy_1).__name__!r}"
            )

        self._class_meta_reference_dummy_1 = class_meta_reference_dummy_1
        if not isinstance(class_meta_reference_dummy_3, list) or not all(isinstance(i, MetaReferenceDummy3) for i in class_meta_reference_dummy_3):
            raise TypeError(
                f"Expected 'list[MetaReferenceDummy3]' for '_class_meta_reference_dummy_3', got {type(class_meta_reference_dummy_3).__name__!r}"
            )
        if len(class_meta_reference_dummy_3) < 1:
            raise ValueError(
                f"Field '_class_meta_reference_dummy_3' must have at least 1 element(s), got {len(class_meta_reference_dummy_3)}"
            )

        self._class_meta_reference_dummy_3 = class_meta_reference_dummy_3
        if not isinstance(enum_example_enum_1, ExampleEnum1):
            raise TypeError(
                f"Expected 'ExampleEnum1' for '_enum_example_enum_1', got {type(enum_example_enum_1).__name__!r}"
            )

        self._enum_example_enum_1 = enum_example_enum_1
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

        self._name = name
        if class_meta_reference_dummy_2 is not None:
            if not isinstance(class_meta_reference_dummy_2, MetaReferenceDummy2):
                raise TypeError(
                    f"Expected 'MetaReferenceDummy2' or None for '_class_meta_reference_dummy_2', got {type(class_meta_reference_dummy_2).__name__!r}"
                )

        self._class_meta_reference_dummy_2 = class_meta_reference_dummy_2
        if class_meta_reference_dummy_4 is not None:
            if not isinstance(class_meta_reference_dummy_4, list) or not all(isinstance(i, MetaReferenceDummy4) for i in class_meta_reference_dummy_4):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy4]' or None for '_class_meta_reference_dummy_4', got {type(class_meta_reference_dummy_4).__name__!r}"
                )

        self._class_meta_reference_dummy_4 = class_meta_reference_dummy_4

    def get_class_imported_1(self) -> ImportedMetaClassDummy1:
        """Generated getter for _class_imported_1"""
        if self._class_imported_1 is None:
            raise ValueError("Field '_class_imported_1' has not been initialized.")
        return self._class_imported_1

    def set_class_imported_1(self, value: ImportedMetaClassDummy1) -> None:
        """
        Generated setter for _class_imported_1

        Args:
            value: The new value to assign to the "_class_imported_1" attribute
        """
        if not isinstance(value, ImportedMetaClassDummy1):
            raise TypeError(
                f"Expected 'ImportedMetaClassDummy1' for '_class_imported_1', got {type(value).__name__!r}"
            )

        self._class_imported_1 = value

    def has_class_imported_1(self) -> bool:
        """Generated has function for _class_imported_1"""
        if self._class_imported_1 is None:
            return False
        return True
    def get_class_meta_class_dummy_1(self) -> MetaClassDummy1:
        """Generated getter for _class_meta_class_dummy_1"""
        if self._class_meta_class_dummy_1 is None:
            raise ValueError("Field '_class_meta_class_dummy_1' has not been initialized.")
        return self._class_meta_class_dummy_1

    def set_class_meta_class_dummy_1(self, value: MetaClassDummy1) -> None:
        """
        Generated setter for _class_meta_class_dummy_1

        Args:
            value: The new value to assign to the "_class_meta_class_dummy_1" attribute
        """
        if not isinstance(value, MetaClassDummy1):
            raise TypeError(
                f"Expected 'MetaClassDummy1' for '_class_meta_class_dummy_1', got {type(value).__name__!r}"
            )

        self._class_meta_class_dummy_1 = value

    def has_class_meta_class_dummy_1(self) -> bool:
        """Generated has function for _class_meta_class_dummy_1"""
        if self._class_meta_class_dummy_1 is None:
            return False
        return True
    def get_class_meta_class_dummy_2(self) -> MetaClassDummy2:
        """Generated getter for _class_meta_class_dummy_2"""
        if self._class_meta_class_dummy_2 is None:
            raise ValueError("Field '_class_meta_class_dummy_2' has not been initialized.")
        return self._class_meta_class_dummy_2

    def set_class_meta_class_dummy_2(self, value: MetaClassDummy2) -> None:
        """
        Generated setter for _class_meta_class_dummy_2

        Args:
            value: The new value to assign to the "_class_meta_class_dummy_2" attribute
        """
        if not isinstance(value, MetaClassDummy2):
            raise TypeError(
                f"Expected 'MetaClassDummy2' for '_class_meta_class_dummy_2', got {type(value).__name__!r}"
            )

        self._class_meta_class_dummy_2 = value

    def has_class_meta_class_dummy_2(self) -> bool:
        """Generated has function for _class_meta_class_dummy_2"""
        if self._class_meta_class_dummy_2 is None:
            return False
        return True
    def get_class_meta_reference_dummy_1(self) -> MetaReferenceDummy1:
        """Generated getter for _class_meta_reference_dummy_1"""
        if self._class_meta_reference_dummy_1 is None:
            raise ValueError("Field '_class_meta_reference_dummy_1' has not been initialized.")
        return self._class_meta_reference_dummy_1

    def set_class_meta_reference_dummy_1(self, value: MetaReferenceDummy1) -> None:
        """
        Generated setter for _class_meta_reference_dummy_1

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_1" attribute
        """
        if not isinstance(value, MetaReferenceDummy1):
            raise TypeError(
                f"Expected 'MetaReferenceDummy1' for '_class_meta_reference_dummy_1', got {type(value).__name__!r}"
            )

        self._class_meta_reference_dummy_1 = value

    def has_class_meta_reference_dummy_1(self) -> bool:
        """Generated has function for _class_meta_reference_dummy_1"""
        if self._class_meta_reference_dummy_1 is None:
            return False
        return True
    def get_class_meta_reference_dummy_3(self) -> list[MetaReferenceDummy3]:
        """Generated getter for _class_meta_reference_dummy_3"""
        if self._class_meta_reference_dummy_3 is None:
            raise ValueError("Field '_class_meta_reference_dummy_3' has not been initialized.")
        return self._class_meta_reference_dummy_3

    def set_class_meta_reference_dummy_3(self, value: list[MetaReferenceDummy3]) -> None:
        """
        Generated setter for _class_meta_reference_dummy_3

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_3" attribute
        """
        if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy3) for i in value):
            raise TypeError(
                f"Expected 'list[MetaReferenceDummy3]' for '_class_meta_reference_dummy_3', got {type(value).__name__!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"Field '_class_meta_reference_dummy_3' must have at least 1 element(s), got {len(value)}"
            )

        self._class_meta_reference_dummy_3 = value

    def has_class_meta_reference_dummy_3(self) -> bool:
        """Generated has function for _class_meta_reference_dummy_3"""
        if self._class_meta_reference_dummy_3 is None:
            return False
        return True
    def get_enum_example_enum_1(self) -> ExampleEnum1:
        """Generated getter for _enum_example_enum_1"""
        if self._enum_example_enum_1 is None:
            raise ValueError("Field '_enum_example_enum_1' has not been initialized.")
        return self._enum_example_enum_1

    def set_enum_example_enum_1(self, value: ExampleEnum1) -> None:
        """
        Generated setter for _enum_example_enum_1

        Args:
            value: The new value to assign to the "_enum_example_enum_1" attribute
        """
        if not isinstance(value, ExampleEnum1):
            raise TypeError(
                f"Expected 'ExampleEnum1' for '_enum_example_enum_1', got {type(value).__name__!r}"
            )

        self._enum_example_enum_1 = value

    def has_enum_example_enum_1(self) -> bool:
        """Generated has function for _enum_example_enum_1"""
        if self._enum_example_enum_1 is None:
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
    def get_class_meta_reference_dummy_2(self) -> MetaReferenceDummy2 | None:
        """Generated getter for _class_meta_reference_dummy_2"""
        return self._class_meta_reference_dummy_2

    def set_class_meta_reference_dummy_2(self, value: MetaReferenceDummy2 | None) -> None:
        """
        Generated setter for _class_meta_reference_dummy_2

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_2" attribute
        """
        if value is not None:
            if not isinstance(value, MetaReferenceDummy2):
                raise TypeError(
                    f"Expected 'MetaReferenceDummy2' or None for '_class_meta_reference_dummy_2', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummy_2 = value

    def has_class_meta_reference_dummy_2(self) -> bool:
        """Generated has function for _class_meta_reference_dummy_2"""
        if self._class_meta_reference_dummy_2 is None:
            return False
        return True
    def get_class_meta_reference_dummy_4(self) -> list[MetaReferenceDummy4] | None:
        """Generated getter for _class_meta_reference_dummy_4"""
        return self._class_meta_reference_dummy_4

    def set_class_meta_reference_dummy_4(self, value: list[MetaReferenceDummy4] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummy_4

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_4" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy4) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy4]' or None for '_class_meta_reference_dummy_4', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummy_4 = value

    def has_class_meta_reference_dummy_4(self) -> bool:
        """Generated has function for _class_meta_reference_dummy_4"""
        if self._class_meta_reference_dummy_4 is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaModelDummy"""
        result = {}
        result["class_imported_1"] = (
            self._class_imported_1.to_dict() if hasattr(self._class_imported_1, "to_dict")
            else (self._class_imported_1.value if hasattr(self._class_imported_1, "value") else self._class_imported_1)
        )
        result["class_meta_class_dummy_1"] = (
            self._class_meta_class_dummy_1.to_dict() if hasattr(self._class_meta_class_dummy_1, "to_dict")
            else (self._class_meta_class_dummy_1.value if hasattr(self._class_meta_class_dummy_1, "value") else self._class_meta_class_dummy_1)
        )
        result["class_meta_class_dummy_2"] = (
            self._class_meta_class_dummy_2.to_dict() if hasattr(self._class_meta_class_dummy_2, "to_dict")
            else (self._class_meta_class_dummy_2.value if hasattr(self._class_meta_class_dummy_2, "value") else self._class_meta_class_dummy_2)
        )
        result["class_meta_reference_dummy_1"] = (
            self._class_meta_reference_dummy_1.to_dict() if hasattr(self._class_meta_reference_dummy_1, "to_dict")
            else (self._class_meta_reference_dummy_1.value if hasattr(self._class_meta_reference_dummy_1, "value") else self._class_meta_reference_dummy_1)
        )
        result["class_meta_reference_dummy_3"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummy_3]
        )
        result["enum_example_enum_1"] = (
            self._enum_example_enum_1.to_dict() if hasattr(self._enum_example_enum_1, "to_dict")
            else (self._enum_example_enum_1.value if hasattr(self._enum_example_enum_1, "value") else self._enum_example_enum_1)
        )
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        result["class_meta_reference_dummy_2"] = (
            self._class_meta_reference_dummy_2.to_dict() if hasattr(self._class_meta_reference_dummy_2, "to_dict")
            else (self._class_meta_reference_dummy_2.value if hasattr(self._class_meta_reference_dummy_2, "value") else self._class_meta_reference_dummy_2)
            if self._class_meta_reference_dummy_2 is not None else None
        )
        result["class_meta_reference_dummy_4"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummy_4]
            if self._class_meta_reference_dummy_4 is not None else None
        )
        return result

class MetaClassDummy1():
    """
    Generated dataclass for MetaClassDummy1
    Attributes:
        _name: str        _test_str: str        _class_meta_composition_dummy_1: MetaCompositionDummy1        _tst_nr: int = 1        _test_bool: bool = False        _test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1    """
    _name: str
    _test_str: str
    _class_meta_composition_dummy_1: MetaCompositionDummy1
    _tst_nr: int = 1
    _test_bool: bool = False
    _test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1

    def __init__(self, name: str, test_str: str, class_meta_composition_dummy_1: MetaCompositionDummy1, tst_nr: int = 1, test_bool: bool = False, test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1) -> None:
        """Generated constructor for MetaClassDummy1"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

        self._name = name
        if not isinstance(test_str, str):
            raise TypeError(
                f"Expected 'str' for '_test_str', got {type(test_str).__name__!r}"
            )

        self._test_str = test_str
        if not isinstance(class_meta_composition_dummy_1, MetaCompositionDummy1):
            raise TypeError(
                f"Expected 'MetaCompositionDummy1' for '_class_meta_composition_dummy_1', got {type(class_meta_composition_dummy_1).__name__!r}"
            )

        self._class_meta_composition_dummy_1 = class_meta_composition_dummy_1
        if not isinstance(tst_nr, int):
            raise TypeError(
                f"Expected 'int' for '_tst_nr', got {type(tst_nr).__name__!r}"
            )

        self._tst_nr = tst_nr
        if not isinstance(test_bool, bool):
            raise TypeError(
                f"Expected 'bool' for '_test_bool', got {type(test_bool).__name__!r}"
            )

        self._test_bool = test_bool
        if not isinstance(test_enum, ExampleEnum2):
            raise TypeError(
                f"Expected 'ExampleEnum2' for '_test_enum', got {type(test_enum).__name__!r}"
            )

        self._test_enum = test_enum

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
    def get_test_str(self) -> str:
        """Generated getter for _test_str"""
        if self._test_str is None:
            raise ValueError("Field '_test_str' has not been initialized.")
        return self._test_str

    def set_test_str(self, value: str) -> None:
        """
        Generated setter for _test_str

        Args:
            value: The new value to assign to the "_test_str" attribute
        """
        if not isinstance(value, str):
            raise TypeError(
                f"Expected 'str' for '_test_str', got {type(value).__name__!r}"
            )

        self._test_str = value

    def has_test_str(self) -> bool:
        """Generated has function for _test_str"""
        if self._test_str is None:
            return False
        return True
    def get_class_meta_composition_dummy_1(self) -> MetaCompositionDummy1:
        """Generated getter for _class_meta_composition_dummy_1"""
        if self._class_meta_composition_dummy_1 is None:
            raise ValueError("Field '_class_meta_composition_dummy_1' has not been initialized.")
        return self._class_meta_composition_dummy_1

    def set_class_meta_composition_dummy_1(self, value: MetaCompositionDummy1) -> None:
        """
        Generated setter for _class_meta_composition_dummy_1

        Args:
            value: The new value to assign to the "_class_meta_composition_dummy_1" attribute
        """
        if not isinstance(value, MetaCompositionDummy1):
            raise TypeError(
                f"Expected 'MetaCompositionDummy1' for '_class_meta_composition_dummy_1', got {type(value).__name__!r}"
            )

        self._class_meta_composition_dummy_1 = value

    def has_class_meta_composition_dummy_1(self) -> bool:
        """Generated has function for _class_meta_composition_dummy_1"""
        if self._class_meta_composition_dummy_1 is None:
            return False
        return True
    def get_tst_nr(self) -> int:
        """Generated getter for _tst_nr"""
        if self._tst_nr is None:
            raise ValueError("Field '_tst_nr' has not been initialized.")
        return self._tst_nr

    def set_tst_nr(self, value: int) -> None:
        """
        Generated setter for _tst_nr

        Args:
            value: The new value to assign to the "_tst_nr" attribute
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Expected 'int' for '_tst_nr', got {type(value).__name__!r}"
            )

        self._tst_nr = value

    def has_tst_nr(self) -> bool:
        """Generated has function for _tst_nr"""
        if self._tst_nr is None:
            return False
        return True
    def get_test_bool(self) -> bool:
        """Generated getter for _test_bool"""
        if self._test_bool is None:
            raise ValueError("Field '_test_bool' has not been initialized.")
        return self._test_bool

    def set_test_bool(self, value: bool) -> None:
        """
        Generated setter for _test_bool

        Args:
            value: The new value to assign to the "_test_bool" attribute
        """
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected 'bool' for '_test_bool', got {type(value).__name__!r}"
            )

        self._test_bool = value

    def has_test_bool(self) -> bool:
        """Generated has function for _test_bool"""
        if self._test_bool is None:
            return False
        return True
    def get_test_enum(self) -> ExampleEnum2:
        """Generated getter for _test_enum"""
        if self._test_enum is None:
            raise ValueError("Field '_test_enum' has not been initialized.")
        return self._test_enum

    def set_test_enum(self, value: ExampleEnum2) -> None:
        """
        Generated setter for _test_enum

        Args:
            value: The new value to assign to the "_test_enum" attribute
        """
        if not isinstance(value, ExampleEnum2):
            raise TypeError(
                f"Expected 'ExampleEnum2' for '_test_enum', got {type(value).__name__!r}"
            )

        self._test_enum = value

    def has_test_enum(self) -> bool:
        """Generated has function for _test_enum"""
        if self._test_enum is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaClassDummy1"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        result["test_str"] = (
            self._test_str.to_dict() if hasattr(self._test_str, "to_dict")
            else (self._test_str.value if hasattr(self._test_str, "value") else self._test_str)
        )
        result["class_meta_composition_dummy_1"] = (
            self._class_meta_composition_dummy_1.to_dict() if hasattr(self._class_meta_composition_dummy_1, "to_dict")
            else (self._class_meta_composition_dummy_1.value if hasattr(self._class_meta_composition_dummy_1, "value") else self._class_meta_composition_dummy_1)
        )
        result["tst_nr"] = (
            self._tst_nr.to_dict() if hasattr(self._tst_nr, "to_dict")
            else (self._tst_nr.value if hasattr(self._tst_nr, "value") else self._tst_nr)
        )
        result["test_bool"] = (
            self._test_bool.to_dict() if hasattr(self._test_bool, "to_dict")
            else (self._test_bool.value if hasattr(self._test_bool, "value") else self._test_bool)
        )
        result["test_enum"] = (
            self._test_enum.to_dict() if hasattr(self._test_enum, "to_dict")
            else (self._test_enum.value if hasattr(self._test_enum, "value") else self._test_enum)
        )
        return result

class MetaClassDummy2():
    """
    Generated dataclass for MetaClassDummy2
    Attributes:
        _name: str        _tst_nr: int = 125        _test_str: str | None = None        _test_bool: list[bool] = ['True', 'False']        _class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None        _class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None        _class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None        _class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None        _class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None        _test_enum: list[ExampleEnum1] = ['VALUE_1', 'VALUE_2']    """
    _name: str
    _tst_nr: int = 125
    _test_str: str | None = None
    _test_bool: list[bool] = ['True', 'False']
    _class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None
    _class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None
    _class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None
    _class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None
    _class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None
    _test_enum: list[ExampleEnum1] = ['VALUE_1', 'VALUE_2']

    def __init__(self, name: str, tst_nr: int = 125, test_str: str | None = None, test_bool: list[bool] = ['True', 'False'], class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None, class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None, class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None, class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None, class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None, test_enum: list[ExampleEnum1] = ['VALUE_1', 'VALUE_2']) -> None:
        """Generated constructor for MetaClassDummy2"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

        self._name = name
        if not isinstance(tst_nr, int):
            raise TypeError(
                f"Expected 'int' for '_tst_nr', got {type(tst_nr).__name__!r}"
            )

        self._tst_nr = tst_nr
        if test_str is not None:
            if not isinstance(test_str, str):
                raise TypeError(
                    f"Expected 'str' or None for '_test_str', got {type(test_str).__name__!r}"
                )

        self._test_str = test_str
        if not isinstance(test_bool, list) or not all(isinstance(i, bool) for i in test_bool):
            raise TypeError(
                f"Expected 'list[bool]' for '_test_bool', got {type(test_bool).__name__!r}"
            )
        if len(test_bool) < 1:
            raise ValueError(
                f"Field '_test_bool' must have at least 1 element(s), got {len(test_bool)}"
            )

        self._test_bool = test_bool
        if class_meta_composition_dummies_1 is not None:
            if not isinstance(class_meta_composition_dummies_1, list) or not all(isinstance(i, MetaCompositionDummy1) for i in class_meta_composition_dummies_1):
                raise TypeError(
                    f"Expected 'list[MetaCompositionDummy1]' or None for '_class_meta_composition_dummies_1', got {type(class_meta_composition_dummies_1).__name__!r}"
                )

        self._class_meta_composition_dummies_1 = class_meta_composition_dummies_1
        if class_meta_reference_dummies_1 is not None:
            if not isinstance(class_meta_reference_dummies_1, list) or not all(isinstance(i, MetaReferenceDummy1) for i in class_meta_reference_dummies_1):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy1]' or None for '_class_meta_reference_dummies_1', got {type(class_meta_reference_dummies_1).__name__!r}"
                )

        self._class_meta_reference_dummies_1 = class_meta_reference_dummies_1
        if class_meta_reference_dummies_2 is not None:
            if not isinstance(class_meta_reference_dummies_2, list) or not all(isinstance(i, MetaReferenceDummy2) for i in class_meta_reference_dummies_2):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy2]' or None for '_class_meta_reference_dummies_2', got {type(class_meta_reference_dummies_2).__name__!r}"
                )

        self._class_meta_reference_dummies_2 = class_meta_reference_dummies_2
        if class_meta_reference_dummies_3 is not None:
            if not isinstance(class_meta_reference_dummies_3, list) or not all(isinstance(i, MetaReferenceDummy3) for i in class_meta_reference_dummies_3):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy3]' or None for '_class_meta_reference_dummies_3', got {type(class_meta_reference_dummies_3).__name__!r}"
                )

        self._class_meta_reference_dummies_3 = class_meta_reference_dummies_3
        if class_meta_reference_dummies_4 is not None:
            if not isinstance(class_meta_reference_dummies_4, list) or not all(isinstance(i, MetaReferenceDummy4) for i in class_meta_reference_dummies_4):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy4]' or None for '_class_meta_reference_dummies_4', got {type(class_meta_reference_dummies_4).__name__!r}"
                )

        self._class_meta_reference_dummies_4 = class_meta_reference_dummies_4
        if not isinstance(test_enum, list) or not all(isinstance(i, ExampleEnum1) for i in test_enum):
            raise TypeError(
                f"Expected 'list[ExampleEnum1]' for '_test_enum', got {type(test_enum).__name__!r}"
            )
        if len(test_enum) < 1:
            raise ValueError(
                f"Field '_test_enum' must have at least 1 element(s), got {len(test_enum)}"
            )

        self._test_enum = test_enum

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
    def get_tst_nr(self) -> int:
        """Generated getter for _tst_nr"""
        if self._tst_nr is None:
            raise ValueError("Field '_tst_nr' has not been initialized.")
        return self._tst_nr

    def set_tst_nr(self, value: int) -> None:
        """
        Generated setter for _tst_nr

        Args:
            value: The new value to assign to the "_tst_nr" attribute
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Expected 'int' for '_tst_nr', got {type(value).__name__!r}"
            )

        self._tst_nr = value

    def has_tst_nr(self) -> bool:
        """Generated has function for _tst_nr"""
        if self._tst_nr is None:
            return False
        return True
    def get_test_str(self) -> str | None:
        """Generated getter for _test_str"""
        return self._test_str

    def set_test_str(self, value: str | None) -> None:
        """
        Generated setter for _test_str

        Args:
            value: The new value to assign to the "_test_str" attribute
        """
        if value is not None:
            if not isinstance(value, str):
                raise TypeError(
                    f"Expected 'str' or None for '_test_str', got {type(value).__name__!r}"
                )

        self._test_str = value

    def has_test_str(self) -> bool:
        """Generated has function for _test_str"""
        if self._test_str is None:
            return False
        return True
    def get_test_bool(self) -> list[bool]:
        """Generated getter for _test_bool"""
        if self._test_bool is None:
            raise ValueError("Field '_test_bool' has not been initialized.")
        return self._test_bool

    def set_test_bool(self, value: list[bool]) -> None:
        """
        Generated setter for _test_bool

        Args:
            value: The new value to assign to the "_test_bool" attribute
        """
        if not isinstance(value, list) or not all(isinstance(i, bool) for i in value):
            raise TypeError(
                f"Expected 'list[bool]' for '_test_bool', got {type(value).__name__!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"Field '_test_bool' must have at least 1 element(s), got {len(value)}"
            )

        self._test_bool = value

    def has_test_bool(self) -> bool:
        """Generated has function for _test_bool"""
        if self._test_bool is None:
            return False
        return True
    def get_class_meta_composition_dummies_1(self) -> list[MetaCompositionDummy1] | None:
        """Generated getter for _class_meta_composition_dummies_1"""
        return self._class_meta_composition_dummies_1

    def set_class_meta_composition_dummies_1(self, value: list[MetaCompositionDummy1] | None) -> None:
        """
        Generated setter for _class_meta_composition_dummies_1

        Args:
            value: The new value to assign to the "_class_meta_composition_dummies_1" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaCompositionDummy1) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaCompositionDummy1]' or None for '_class_meta_composition_dummies_1', got {type(value).__name__!r}"
                )

        self._class_meta_composition_dummies_1 = value

    def has_class_meta_composition_dummies_1(self) -> bool:
        """Generated has function for _class_meta_composition_dummies_1"""
        if self._class_meta_composition_dummies_1 is None:
            return False
        return True
    def get_class_meta_reference_dummies_1(self) -> list[MetaReferenceDummy1] | None:
        """Generated getter for _class_meta_reference_dummies_1"""
        return self._class_meta_reference_dummies_1

    def set_class_meta_reference_dummies_1(self, value: list[MetaReferenceDummy1] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_1

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_1" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy1) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy1]' or None for '_class_meta_reference_dummies_1', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummies_1 = value

    def has_class_meta_reference_dummies_1(self) -> bool:
        """Generated has function for _class_meta_reference_dummies_1"""
        if self._class_meta_reference_dummies_1 is None:
            return False
        return True
    def get_class_meta_reference_dummies_2(self) -> list[MetaReferenceDummy2] | None:
        """Generated getter for _class_meta_reference_dummies_2"""
        return self._class_meta_reference_dummies_2

    def set_class_meta_reference_dummies_2(self, value: list[MetaReferenceDummy2] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_2

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_2" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy2) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy2]' or None for '_class_meta_reference_dummies_2', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummies_2 = value

    def has_class_meta_reference_dummies_2(self) -> bool:
        """Generated has function for _class_meta_reference_dummies_2"""
        if self._class_meta_reference_dummies_2 is None:
            return False
        return True
    def get_class_meta_reference_dummies_3(self) -> list[MetaReferenceDummy3] | None:
        """Generated getter for _class_meta_reference_dummies_3"""
        return self._class_meta_reference_dummies_3

    def set_class_meta_reference_dummies_3(self, value: list[MetaReferenceDummy3] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_3

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_3" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy3) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy3]' or None for '_class_meta_reference_dummies_3', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummies_3 = value

    def has_class_meta_reference_dummies_3(self) -> bool:
        """Generated has function for _class_meta_reference_dummies_3"""
        if self._class_meta_reference_dummies_3 is None:
            return False
        return True
    def get_class_meta_reference_dummies_4(self) -> list[MetaReferenceDummy4] | None:
        """Generated getter for _class_meta_reference_dummies_4"""
        return self._class_meta_reference_dummies_4

    def set_class_meta_reference_dummies_4(self, value: list[MetaReferenceDummy4] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_4

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_4" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy4) for i in value):
                raise TypeError(
                    f"Expected 'list[MetaReferenceDummy4]' or None for '_class_meta_reference_dummies_4', got {type(value).__name__!r}"
                )

        self._class_meta_reference_dummies_4 = value

    def has_class_meta_reference_dummies_4(self) -> bool:
        """Generated has function for _class_meta_reference_dummies_4"""
        if self._class_meta_reference_dummies_4 is None:
            return False
        return True
    def get_test_enum(self) -> list[ExampleEnum1]:
        """Generated getter for _test_enum"""
        if self._test_enum is None:
            raise ValueError("Field '_test_enum' has not been initialized.")
        return self._test_enum

    def set_test_enum(self, value: list[ExampleEnum1]) -> None:
        """
        Generated setter for _test_enum

        Args:
            value: The new value to assign to the "_test_enum" attribute
        """
        if not isinstance(value, list) or not all(isinstance(i, ExampleEnum1) for i in value):
            raise TypeError(
                f"Expected 'list[ExampleEnum1]' for '_test_enum', got {type(value).__name__!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"Field '_test_enum' must have at least 1 element(s), got {len(value)}"
            )

        self._test_enum = value

    def has_test_enum(self) -> bool:
        """Generated has function for _test_enum"""
        if self._test_enum is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaClassDummy2"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        result["tst_nr"] = (
            self._tst_nr.to_dict() if hasattr(self._tst_nr, "to_dict")
            else (self._tst_nr.value if hasattr(self._tst_nr, "value") else self._tst_nr)
        )
        result["test_str"] = (
            self._test_str.to_dict() if hasattr(self._test_str, "to_dict")
            else (self._test_str.value if hasattr(self._test_str, "value") else self._test_str)
            if self._test_str is not None else None
        )
        result["test_bool"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._test_bool]
        )
        result["class_meta_composition_dummies_1"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_composition_dummies_1]
            if self._class_meta_composition_dummies_1 is not None else None
        )
        result["class_meta_reference_dummies_1"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummies_1]
            if self._class_meta_reference_dummies_1 is not None else None
        )
        result["class_meta_reference_dummies_2"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummies_2]
            if self._class_meta_reference_dummies_2 is not None else None
        )
        result["class_meta_reference_dummies_3"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummies_3]
            if self._class_meta_reference_dummies_3 is not None else None
        )
        result["class_meta_reference_dummies_4"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._class_meta_reference_dummies_4]
            if self._class_meta_reference_dummies_4 is not None else None
        )
        result["test_enum"] = (
            [v.to_dict() if hasattr(v, "to_dict") else (v.value if hasattr(v, "value") else v) for v in self._test_enum]
        )
        return result

class MetaCompositionDummy1():
    """
    Generated dataclass for MetaCompositionDummy1
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaCompositionDummy1"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaCompositionDummy1"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class MetaReferenceDummy1():
    """
    Generated dataclass for MetaReferenceDummy1
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy1"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaReferenceDummy1"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class MetaReferenceDummy2():
    """
    Generated dataclass for MetaReferenceDummy2
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy2"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaReferenceDummy2"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class MetaReferenceDummy3():
    """
    Generated dataclass for MetaReferenceDummy3
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy3"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaReferenceDummy3"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class MetaReferenceDummy4():
    """
    Generated dataclass for MetaReferenceDummy4
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy4"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MetaReferenceDummy4"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class ImportedRoot():
    """
    Generated dataclass for ImportedRoot
    Attributes:
        _imported_meta_class_dummy_1: ImportedMetaClassDummy1        _name: str = "root"    """
    _imported_meta_class_dummy_1: ImportedMetaClassDummy1
    _name: str = "root"

    def __init__(self, imported_meta_class_dummy_1: ImportedMetaClassDummy1, name: str = "root") -> None:
        """Generated constructor for ImportedRoot"""
        if not isinstance(imported_meta_class_dummy_1, ImportedMetaClassDummy1):
            raise TypeError(
                f"Expected 'ImportedMetaClassDummy1' for '_imported_meta_class_dummy_1', got {type(imported_meta_class_dummy_1).__name__!r}"
            )

        self._imported_meta_class_dummy_1 = imported_meta_class_dummy_1
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'ImportedMetaClassDummy1' for '_imported_meta_class_dummy_1', got {type(value).__name__!r}"
            )

        self._imported_meta_class_dummy_1 = value

    def has_imported_meta_class_dummy_1(self) -> bool:
        """Generated has function for _imported_meta_class_dummy_1"""
        if self._imported_meta_class_dummy_1 is None:
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

    def to_dict(self) -> dict:
        """Generated serialization method for ImportedRoot"""
        result = {}
        result["imported_meta_class_dummy_1"] = (
            self._imported_meta_class_dummy_1.to_dict() if hasattr(self._imported_meta_class_dummy_1, "to_dict")
            else (self._imported_meta_class_dummy_1.value if hasattr(self._imported_meta_class_dummy_1, "value") else self._imported_meta_class_dummy_1)
        )
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class ImportedMetaClassDummy1():
    """
    Generated dataclass for ImportedMetaClassDummy1
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for ImportedMetaClassDummy1"""
        if not isinstance(name, str):
            raise TypeError(
                f"Expected 'str' for '_name', got {type(name).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'str' for '_name', got {type(value).__name__!r}"
            )

        self._name = value

    def has_name(self) -> bool:
        """Generated has function for _name"""
        if self._name is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for ImportedMetaClassDummy1"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

