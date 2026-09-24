# --- GENERATED CODE - DO NOT EDIT ---
from __future__ import annotations

class BaseNode():
    """
    Generated dataclass for BaseNode
    Attributes:
        _name: str    """
    _name: str

    def __init__(self, name: str) -> None:
        """Generated constructor for BaseNode"""
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
        """Generated serialization method for BaseNode"""
        result = {}
        result["name"] = (
            self._name.to_dict() if hasattr(self._name, "to_dict")
            else (self._name.value if hasattr(self._name, "value") else self._name)
        )
        return result

class ChildNode(BaseNode):
    """
    Generated dataclass for ChildNode
    Attributes:
        _parent: BaseNode        _rank: int = 1    """
    _parent: BaseNode
    _rank: int = 1

    def __init__(self, parent: BaseNode, rank: int = 1) -> None:
        """Generated constructor for ChildNode"""
        if not isinstance(parent, BaseNode):
            raise TypeError(
                f"Expected 'BaseNode' for '_parent', got {type(parent).__name__!r}"
            )

        self._parent = parent
        if not isinstance(rank, int):
            raise TypeError(
                f"Expected 'int' for '_rank', got {type(rank).__name__!r}"
            )

        self._rank = rank

    def get_parent(self) -> BaseNode:
        """Generated getter for _parent"""
        if self._parent is None:
            raise ValueError("Field '_parent' has not been initialized.")
        return self._parent

    def set_parent(self, value: BaseNode) -> None:
        """
        Generated setter for _parent

        Args:
            value: The new value to assign to the "_parent" attribute
        """
        if not isinstance(value, BaseNode):
            raise TypeError(
                f"Expected 'BaseNode' for '_parent', got {type(value).__name__!r}"
            )

        self._parent = value

    def has_parent(self) -> bool:
        """Generated has function for _parent"""
        if self._parent is None:
            return False
        return True
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
            raise TypeError(
                f"Expected 'int' for '_rank', got {type(value).__name__!r}"
            )

        self._rank = value

    def has_rank(self) -> bool:
        """Generated has function for _rank"""
        if self._rank is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for ChildNode"""
        result = {}
        result["parent"] = (
            self._parent.to_dict() if hasattr(self._parent, "to_dict")
            else (self._parent.value if hasattr(self._parent, "value") else self._parent)
        )
        result["rank"] = (
            self._rank.to_dict() if hasattr(self._rank, "to_dict")
            else (self._rank.value if hasattr(self._rank, "value") else self._rank)
        )
        return result

class InterfaceNode():
    """
    Generated dataclass for InterfaceNode
    Attributes:
        _visible: bool = False    """
    _visible: bool = False

    def __init__(self, visible: bool = False) -> None:
        """Generated constructor for InterfaceNode"""
        if not isinstance(visible, bool):
            raise TypeError(
                f"Expected 'bool' for '_visible', got {type(visible).__name__!r}"
            )

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
            raise TypeError(
                f"Expected 'bool' for '_visible', got {type(value).__name__!r}"
            )

        self._visible = value

    def has_visible(self) -> bool:
        """Generated has function for _visible"""
        if self._visible is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for InterfaceNode"""
        result = {}
        result["visible"] = (
            self._visible.to_dict() if hasattr(self._visible, "to_dict")
            else (self._visible.value if hasattr(self._visible, "value") else self._visible)
        )
        return result

class MultiInheritedNode(ChildNode, InterfaceNode):
    """
    Generated dataclass for MultiInheritedNode
    Attributes:
        _weight: int | None = None    """
    _weight: int | None = None

    def __init__(self, weight: int | None = None) -> None:
        """Generated constructor for MultiInheritedNode"""
        if weight is not None:
            if not isinstance(weight, int):
                raise TypeError(
                    f"Expected 'int' or None for '_weight', got {type(weight).__name__!r}"
                )

        self._weight = weight

    def get_weight(self) -> int | None:
        """Generated getter for _weight"""
        return self._weight

    def set_weight(self, value: int | None) -> None:
        """
        Generated setter for _weight

        Args:
            value: The new value to assign to the "_weight" attribute
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError(
                    f"Expected 'int' or None for '_weight', got {type(value).__name__!r}"
                )

        self._weight = value

    def has_weight(self) -> bool:
        """Generated has function for _weight"""
        if self._weight is None:
            return False
        return True

    def to_dict(self) -> dict:
        """Generated serialization method for MultiInheritedNode"""
        result = {}
        result["weight"] = (
            self._weight.to_dict() if hasattr(self._weight, "to_dict")
            else (self._weight.value if hasattr(self._weight, "value") else self._weight)
            if self._weight is not None else None
        )
        return result

