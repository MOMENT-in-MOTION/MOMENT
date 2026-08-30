# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations
from .enum_code import *

class MetaModelDummy:
    """
    Generated dataclass for MetaModelDummy 
    Attributes:
        _class_imported_1: ImportedMetaClassDummy1 
        _class_meta_class_dummy_1: MetaClassDummy1 
        _class_meta_class_dummy_2: MetaClassDummy2 
        _class_meta_reference_dummy_1: MetaReferenceDummy1 
        _class_meta_reference_dummy_3: list[MetaReferenceDummy3] 
        _enum_example_enum_1: ExampleEnum1 
        _name: str = "root" 
        _class_meta_reference_dummy_2: MetaReferenceDummy2 | None = None 
        _class_meta_reference_dummy_4: list[MetaReferenceDummy4] | None = None 
    """
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
        self._class_imported_1 = class_imported_1
        self._class_meta_class_dummy_1 = class_meta_class_dummy_1
        self._class_meta_class_dummy_2 = class_meta_class_dummy_2
        self._class_meta_reference_dummy_1 = class_meta_reference_dummy_1
        self._class_meta_reference_dummy_3 = class_meta_reference_dummy_3
        self._enum_example_enum_1 = enum_example_enum_1
        self._name = name
        self._class_meta_reference_dummy_2 = class_meta_reference_dummy_2
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
            raise TypeError(f"Expected type ImportedMetaClassDummy1 for field '_class_imported_1', got {type(value)}")
        self._class_imported_1 = value

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
            raise TypeError(f"Expected type MetaClassDummy1 for field '_class_meta_class_dummy_1', got {type(value)}")
        self._class_meta_class_dummy_1 = value

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
            raise TypeError(f"Expected type MetaClassDummy2 for field '_class_meta_class_dummy_2', got {type(value)}")
        self._class_meta_class_dummy_2 = value

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
            raise TypeError(f"Expected type MetaReferenceDummy1 for field '_class_meta_reference_dummy_1', got {type(value)}")
        self._class_meta_reference_dummy_1 = value

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
            raise TypeError(f"Expected type list[MetaReferenceDummy3] for field '_class_meta_reference_dummy_3', got {type(value)}")
        self._class_meta_reference_dummy_3 = value

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
            raise TypeError(f"Expected type ExampleEnum1 for field '_enum_example_enum_1', got {type(value)}")
        self._enum_example_enum_1 = value

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

    def get_class_meta_reference_dummy_2(self) -> MetaReferenceDummy2 | None:
        """Generated getter for _class_meta_reference_dummy_2"""
        if self._class_meta_reference_dummy_2 is None:
            raise ValueError("Field '_class_meta_reference_dummy_2' has not been initialized.")
        return self._class_meta_reference_dummy_2

    def set_class_meta_reference_dummy_2(self, value: MetaReferenceDummy2 | None) -> None:
        """
        Generated setter for _class_meta_reference_dummy_2

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_2" attribute
        """
        if value is not None:
            if not isinstance(value, MetaReferenceDummy2):
                raise TypeError(f"Expected type MetaReferenceDummy2 or None for field '_class_meta_reference_dummy_2', got {type(value)}")
        self._class_meta_reference_dummy_2 = value

    def get_class_meta_reference_dummy_4(self) -> list[MetaReferenceDummy4] | None:
        """Generated getter for _class_meta_reference_dummy_4"""
        if self._class_meta_reference_dummy_4 is None:
            raise ValueError("Field '_class_meta_reference_dummy_4' has not been initialized.")
        return self._class_meta_reference_dummy_4

    def set_class_meta_reference_dummy_4(self, value: list[MetaReferenceDummy4] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummy_4

        Args:
            value: The new value to assign to the "_class_meta_reference_dummy_4" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy4) for i in value):
                raise TypeError(f"Expected type list[MetaReferenceDummy4] or None for field '_class_meta_reference_dummy_4', got {type(value)}")
        self._class_meta_reference_dummy_4 = value

class MetaClassDummy1:
    """
    Generated dataclass for MetaClassDummy1 
    Attributes:
        _name: str 
        _test_str: str 
        _class_meta_composition_dummy_1: MetaCompositionDummy1 
        _tst_nr: int = 1 
        _test_bool: bool = False 
        _test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1 
    """
    _name: str
    _test_str: str
    _class_meta_composition_dummy_1: MetaCompositionDummy1
    _tst_nr: int = 1
    _test_bool: bool = False
    _test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1

    def __init__(self, name: str, test_str: str, class_meta_composition_dummy_1: MetaCompositionDummy1, tst_nr: int = 1, test_bool: bool = False, test_enum: ExampleEnum2 = ExampleEnum2.VALUE_1) -> None:
        """Generated constructor for MetaClassDummy1"""
        self._name = name
        self._test_str = test_str
        self._class_meta_composition_dummy_1 = class_meta_composition_dummy_1
        self._tst_nr = tst_nr
        self._test_bool = test_bool
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
            raise TypeError(f"Expected type str for field '_name', got {type(value)}")
        self._name = value

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
            raise TypeError(f"Expected type str for field '_test_str', got {type(value)}")
        self._test_str = value

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
            raise TypeError(f"Expected type MetaCompositionDummy1 for field '_class_meta_composition_dummy_1', got {type(value)}")
        self._class_meta_composition_dummy_1 = value

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
            raise TypeError(f"Expected type int for field '_tst_nr', got {type(value)}")
        self._tst_nr = value

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
            raise TypeError(f"Expected type bool for field '_test_bool', got {type(value)}")
        self._test_bool = value

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
            raise TypeError(f"Expected type ExampleEnum2 for field '_test_enum', got {type(value)}")
        self._test_enum = value

class MetaClassDummy2:
    """
    Generated dataclass for MetaClassDummy2 
    Attributes:
        _name: str 
        _tst_nr: int = 125 
        _test_str: str | None = None 
        _test_bool: list[bool] = [True, False] 
        _class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None 
        _class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None 
        _class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None 
        _class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None 
        _class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None 
        _test_enum: list[ExampleEnum1] = [ExampleEnum1.VALUE_1, ExampleEnum1.VALUE_2] 
    """
    _name: str
    _tst_nr: int = 125
    _test_str: str | None = None
    _test_bool: list[bool] = [True, False]
    _class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None
    _class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None
    _class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None
    _class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None
    _class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None
    _test_enum: list[ExampleEnum1] = [ExampleEnum1.VALUE_1, ExampleEnum1.VALUE_2]

    def __init__(self, name: str, tst_nr: int = 125, test_str: str | None = None, test_bool: list[bool] = [True, False], class_meta_composition_dummies_1: list[MetaCompositionDummy1] | None = None, class_meta_reference_dummies_1: list[MetaReferenceDummy1] | None = None, class_meta_reference_dummies_2: list[MetaReferenceDummy2] | None = None, class_meta_reference_dummies_3: list[MetaReferenceDummy3] | None = None, class_meta_reference_dummies_4: list[MetaReferenceDummy4] | None = None, test_enum: list[ExampleEnum1] = [ExampleEnum1.VALUE_1, ExampleEnum1.VALUE_2]) -> None:
        """Generated constructor for MetaClassDummy2"""
        self._name = name
        self._tst_nr = tst_nr
        self._test_str = test_str
        self._test_bool = test_bool
        self._class_meta_composition_dummies_1 = class_meta_composition_dummies_1
        self._class_meta_reference_dummies_1 = class_meta_reference_dummies_1
        self._class_meta_reference_dummies_2 = class_meta_reference_dummies_2
        self._class_meta_reference_dummies_3 = class_meta_reference_dummies_3
        self._class_meta_reference_dummies_4 = class_meta_reference_dummies_4
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
            raise TypeError(f"Expected type str for field '_name', got {type(value)}")
        self._name = value

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
            raise TypeError(f"Expected type int for field '_tst_nr', got {type(value)}")
        self._tst_nr = value

    def get_test_str(self) -> str | None:
        """Generated getter for _test_str"""
        if self._test_str is None:
            raise ValueError("Field '_test_str' has not been initialized.")
        return self._test_str

    def set_test_str(self, value: str | None) -> None:
        """
        Generated setter for _test_str

        Args:
            value: The new value to assign to the "_test_str" attribute
        """
        if value is not None:
            if not isinstance(value, str):
                raise TypeError(f"Expected type str or None for field '_test_str', got {type(value)}")
        self._test_str = value

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
            raise TypeError(f"Expected type list[bool] for field '_test_bool', got {type(value)}")
        self._test_bool = value

    def get_class_meta_composition_dummies_1(self) -> list[MetaCompositionDummy1] | None:
        """Generated getter for _class_meta_composition_dummies_1"""
        if self._class_meta_composition_dummies_1 is None:
            raise ValueError("Field '_class_meta_composition_dummies_1' has not been initialized.")
        return self._class_meta_composition_dummies_1

    def set_class_meta_composition_dummies_1(self, value: list[MetaCompositionDummy1] | None) -> None:
        """
        Generated setter for _class_meta_composition_dummies_1

        Args:
            value: The new value to assign to the "_class_meta_composition_dummies_1" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaCompositionDummy1) for i in value):
                raise TypeError(f"Expected type list[MetaCompositionDummy1] or None for field '_class_meta_composition_dummies_1', got {type(value)}")
        self._class_meta_composition_dummies_1 = value

    def get_class_meta_reference_dummies_1(self) -> list[MetaReferenceDummy1] | None:
        """Generated getter for _class_meta_reference_dummies_1"""
        if self._class_meta_reference_dummies_1 is None:
            raise ValueError("Field '_class_meta_reference_dummies_1' has not been initialized.")
        return self._class_meta_reference_dummies_1

    def set_class_meta_reference_dummies_1(self, value: list[MetaReferenceDummy1] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_1

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_1" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy1) for i in value):
                raise TypeError(f"Expected type list[MetaReferenceDummy1] or None for field '_class_meta_reference_dummies_1', got {type(value)}")
        self._class_meta_reference_dummies_1 = value

    def get_class_meta_reference_dummies_2(self) -> list[MetaReferenceDummy2] | None:
        """Generated getter for _class_meta_reference_dummies_2"""
        if self._class_meta_reference_dummies_2 is None:
            raise ValueError("Field '_class_meta_reference_dummies_2' has not been initialized.")
        return self._class_meta_reference_dummies_2

    def set_class_meta_reference_dummies_2(self, value: list[MetaReferenceDummy2] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_2

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_2" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy2) for i in value):
                raise TypeError(f"Expected type list[MetaReferenceDummy2] or None for field '_class_meta_reference_dummies_2', got {type(value)}")
        self._class_meta_reference_dummies_2 = value

    def get_class_meta_reference_dummies_3(self) -> list[MetaReferenceDummy3] | None:
        """Generated getter for _class_meta_reference_dummies_3"""
        if self._class_meta_reference_dummies_3 is None:
            raise ValueError("Field '_class_meta_reference_dummies_3' has not been initialized.")
        return self._class_meta_reference_dummies_3

    def set_class_meta_reference_dummies_3(self, value: list[MetaReferenceDummy3] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_3

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_3" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy3) for i in value):
                raise TypeError(f"Expected type list[MetaReferenceDummy3] or None for field '_class_meta_reference_dummies_3', got {type(value)}")
        self._class_meta_reference_dummies_3 = value

    def get_class_meta_reference_dummies_4(self) -> list[MetaReferenceDummy4] | None:
        """Generated getter for _class_meta_reference_dummies_4"""
        if self._class_meta_reference_dummies_4 is None:
            raise ValueError("Field '_class_meta_reference_dummies_4' has not been initialized.")
        return self._class_meta_reference_dummies_4

    def set_class_meta_reference_dummies_4(self, value: list[MetaReferenceDummy4] | None) -> None:
        """
        Generated setter for _class_meta_reference_dummies_4

        Args:
            value: The new value to assign to the "_class_meta_reference_dummies_4" attribute
        """
        if value is not None:
            if not isinstance(value, list) or not all(isinstance(i, MetaReferenceDummy4) for i in value):
                raise TypeError(f"Expected type list[MetaReferenceDummy4] or None for field '_class_meta_reference_dummies_4', got {type(value)}")
        self._class_meta_reference_dummies_4 = value

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
            raise TypeError(f"Expected type list[ExampleEnum1] for field '_test_enum', got {type(value)}")
        self._test_enum = value

class MetaCompositionDummy1:
    """
    Generated dataclass for MetaCompositionDummy1 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaCompositionDummy1"""
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

class MetaReferenceDummy1:
    """
    Generated dataclass for MetaReferenceDummy1 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy1"""
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

class MetaReferenceDummy2:
    """
    Generated dataclass for MetaReferenceDummy2 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy2"""
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

class MetaReferenceDummy3:
    """
    Generated dataclass for MetaReferenceDummy3 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy3"""
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

class MetaReferenceDummy4:
    """
    Generated dataclass for MetaReferenceDummy4 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for MetaReferenceDummy4"""
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

class ImportedRoot:
    """
    Generated dataclass for ImportedRoot 
    Attributes:
        _imported_meta_class_dummy_1: ImportedMetaClassDummy1 
        _name: str = "root" 
    """
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

class ImportedMetaClassDummy1:
    """
    Generated dataclass for ImportedMetaClassDummy1 
    Attributes:
        _name: str 
    """
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

