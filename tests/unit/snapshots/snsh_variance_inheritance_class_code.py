# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations

class BaseNode():
    """
    Generated dataclass for BaseNode 
    Attributes:
        _name: str 
    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for BaseNode"""
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

class ChildNode(BaseNode):
    """
    Generated dataclass for ChildNode 
    Attributes:
        _rank: int = 1 
    """
    _rank: int = 1

    def __init__(self, rank: int = 1) -> None:
        """Generated constructor for ChildNode"""
        self._rank = rank

    def get_rank(self) -> int:
        """Generated getter for _rank"""
        if self._rank is None:
            raise ValueError("Field '_rank' has not been initialized.")
        return self._rank

    def set_rank(self, value: int) -> None:
        """
        Generated setter for _rank

        Args:
            value: The new value to assign to the "_rank" attribute
        """
        if not isinstance(value, int):
            raise TypeError(f"Expected type int for field '_rank', got {type(value)}")
        self._rank = value

class InterfaceNode():
    """
    Generated dataclass for InterfaceNode 
    Attributes:
        _visible: bool = False 
    """
    _visible: bool = False

    def __init__(self, visible: bool = False) -> None:
        """Generated constructor for InterfaceNode"""
        self._visible = visible

    def get_visible(self) -> bool:
        """Generated getter for _visible"""
        if self._visible is None:
            raise ValueError("Field '_visible' has not been initialized.")
        return self._visible

    def set_visible(self, value: bool) -> None:
        """
        Generated setter for _visible

        Args:
            value: The new value to assign to the "_visible" attribute
        """
        if not isinstance(value, bool):
            raise TypeError(f"Expected type bool for field '_visible', got {type(value)}")
        self._visible = value

class MultiInheritedNode(ChildNode, InterfaceNode):
    """
    Generated dataclass for MultiInheritedNode 
    Attributes:
        _weight: int | None = None 
    """
    _weight: int | None = None

    def __init__(self, weight: int | None = None) -> None:
        """Generated constructor for MultiInheritedNode"""
        self._weight = weight

    def get_weight(self) -> int | None:
        """Generated getter for _weight"""
        if self._weight is None:
            raise ValueError("Field '_weight' has not been initialized.")
        return self._weight

    def set_weight(self, value: int | None) -> None:
        """
        Generated setter for _weight

        Args:
            value: The new value to assign to the "_weight" attribute
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError(f"Expected type int or None for field '_weight', got {type(value)}")
        self._weight = value

