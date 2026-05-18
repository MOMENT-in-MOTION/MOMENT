"""Core data structures for the meta-model."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

# ---------------------------------------------------------------------------
# Enumerations to be used in the MetaModel
# ---------------------------------------------------------------------------

class MultiplicityOptions(str, Enum):
    """Multiplicity options for model elements."""
    
    ONE = "ONE"
    AT_LEAST_ONE = "AT_LEAST_ONE"
    ANY = "ANY"
    ZERO_OR_ONE = "ZERO_OR_ONE"  # Redundant with OPTIONAL, but may be useful for readability
    OPTIONAL = "OPTIONAL"

class AssociationOptions(str, Enum):
    """Association type options."""
    
    COMPOSITION = "COMPOSITION"
    REFERENCE = "REFERENCE"

class TypeOptions(str, Enum):
    """Type options for attributes."""
    
    INT = "int"
    BOOL = "bool"
    STRING = "str"

# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------


class MetaElement(ABC):
    """Base class for all meta-model elements."""

    @abstractmethod
    def validate(self):
        """Validate the element state."""


# ---------------------------------------------------------------------------
# METACLASS Enumeration
# ---------------------------------------------------------------------------


@dataclass(eq=True)
class MetaEnum(MetaElement):
    """Represents an enumeration in the meta-model.

    Attributes:
        name: Name of the enumeration.
        values: Enumeration literals.
    """

    name: str
    values: list[MetaEnumLiteral] = field(default_factory=list)

    def add_value(self, value_name: str, value: str) -> None:
        """Add a literal to the enumeration.

        Args:
            value_name: Name of the literal.
            value: Value of the literal.
        """
        self.values.append(MetaEnumLiteral(name=value_name, value=value))

    def validate(self) -> None:
        """Validate the enumeration.

        Raises:
            ValueError: If the name is empty.
            ValueError: If no literals are defined.
            ValueError: If duplicate literals exist.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaEnum must have a non-empty name.")

        if not self.values:
            raise ValueError(f"The MetaEnum '{self.name}' has no Literals.")

        if len(self.values) != len(set(self.values)):
            raise ValueError(f"The MetaEnum '{self.name}' has duplicate values.")

    def pretty(self, indent: int = 0) -> str:
        """Return a human-readable representation of the enumeration.

        Args:
            indent: Number of indentation spaces.

        Returns:
            Formatted string representation.
        """
        pad = " " * indent

        result = f"{pad}Enum: {self.name}\n"

        for value in self.values:
            result += value.pretty(indent + 2)

        return result


@dataclass(
    eq=True, frozen=True
)  # frozen=True bei MetaEnumLiteral allows hashing, which is necessary for the set() comparison in validate().
class MetaEnumLiteral(MetaElement):
    """Represents a literal of an enumeration.

    Attributes:
        name: Name of the literal.
        value: Literal value.
    """

    name: str
    value: str

    def validate(self) -> None:
        """Validate the enum literal.

        Raises:
            ValueError: If the name is empty.
            ValueError: If the value is empty.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaEnumLiteral must have a non-empty name.")
        if not self.value or self.value.strip() == "":
            raise ValueError("The MetaEnumLiteral must have a non-empty value.")

    def pretty(self, indent: int = 0):
        """Return a human-readable representation of the enum literal.

        Args:
            indent: Number of indentation spaces.

        Returns:
            Formatted string representation.
        """
        pad = " " * indent

        return f"{pad}Name: '{self.name}' and Value: '{self.value}'\n"


# ---------------------------------------------------------------------------
# METACLASS Core Elements
# ---------------------------------------------------------------------------


@dataclass(eq=True)
class Attribute(MetaElement):
    """Represents an attribute definition.

    Attributes:
        name: Name of the attribute.
        multiplicity: Attribute multiplicity.
        attribute_type: Attribute type.
        default_value: Optional default value.
    """

    name: str
    multiplicity: MetaEnumLiteral
    attribute_type: MetaEnumLiteral
    default_value: Any | None

    def validate(self) -> None:
        """Validate the attribute.

        Raises:
            ValueError: If the name is empty.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The Attribute must have a non-empty name.")


@dataclass(eq=True)
class Association(MetaElement):
    """Represents an association between meta-model elements.

    Attributes:
        name: Name of the association.
        multiplicity: Association multiplicity.
        association_type: Association type.
        association_target: Target element of the association.
    """

    name: str
    multiplicity: MultiplicityOptions
    association_type: AssociationOptions
    association_target: MetaClass | MetaEnum

    def validate(self) -> None:
        """Validate the association.

        Raises:
            ValueError: If the name is empty.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The Association must have a non-empty name.")


@dataclass(eq=True)
class OpenAssociation(MetaElement):
    """Represents an unresolved association.

    Attributes:
        name: Name of the association.
        multiplicity: Association multiplicity.
        association_type: Association type.
        association_target_name: Name of the unresolved target.
    """

    # association_origin: MetaClass | None #TODO besprechen. Vielleicht für zweiseitige Referenzen?
    name: str
    multiplicity: MultiplicityOptions
    association_type: AssociationOptions
    association_target_name: str

    def validate(self) -> None:
        """Validate the open association.

        Raises:
            ValueError: If the name is empty.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The Open-Association must have a non-empty name.")

    def to_association(self, final_target: MetaClass | MetaEnum) -> Association:
        """Create a resolved association.

        Args:
            final_target: Resolved association target.

        Returns:
            Resolved association instance.
        """
        return Association(
            name=self.name,
            multiplicity=self.multiplicity,
            association_type=self.association_type,
            association_target=final_target,
        )


# ---------------------------------------------------------------------------
# METACLASS Class
# ---------------------------------------------------------------------------


@dataclass(eq=True)
class MetaClass(MetaElement):
    """Represents a class definition in the meta-model.

    Attributes:
        name: Name of the class.
        attributes: Attributes of the class.
        associations: Associations of the class.
    """

    name: str
    attributes: list[Attribute] = field(default_factory=list)
    associations: list[Association | OpenAssociation] = field(default_factory=list)

    def validate(self) -> None:
        """Validate the class and its contained elements.

        Raises:
            ValueError: If the name is empty.
        """
        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaClass must have a non-empty name.")
        for attribute in self.attributes:
            attribute.validate()
        for association in self.associations:
            association.validate()

    def add_attribute(self, attribute: Attribute) -> None:
        """Add an attribute to the class.

        Args:
            attribute: Attribute to add.

        Raises:
            ValueError: If an attribute with the same name already exists.
        """
        if any(a.name == attribute.name for a in self.attributes):
            raise ValueError(
                f"A attribute with the name {attribute.name} "
                + f"already exists in the MetaClass {self.name}"
            )
        self.attributes.append(attribute)

    def add_association(self, association: Association) -> None:
        """Add an association to the class.

        Args:
            association: Association to add.

        Raises:
            ValueError: If an association with the same name already exists.
        """
        if any(a.name == association.name for a in self.associations):
            raise ValueError(
                f"The association with the name {association.name}"
                + f"already exists in the MetaClass {self.name}"
            )
        self.associations.append(association)

    def pretty(self, indent: int = 0) -> str:
        """Return a human-readable representation of the class.

        Args:
            indent: Number of indentation spaces.

        Returns:
            Formatted string representation.
        """
        pad = " " * indent

        result = f"{pad}Class: {self.name}\n"

        if self.attributes:
            result += f"{pad}  Attributes:\n"
            for attr in self.attributes:
                default = ""
                if attr.default_value:
                    default = attr.default_value
                result += (
                    f"{pad}    - {attr.name}: \t\t"
                    f"{attr.attribute_type.name} "
                    f"[{attr.multiplicity.name}] "
                    f"{default}\n"
                )

        if self.associations:
            result += f"{pad}  Associations:\n"
            for assoc in self.associations:
                if isinstance(assoc, OpenAssociation):
                    result += (
                        f"{pad}    -> Open Association {assoc.name} "
                        f"({assoc.association_type.name}) "
                        f"\t-> {assoc.association_target} "
                        f"[{assoc.multiplicity.name}]\n"
                    )
                else:
                    result += (
                        f"{pad}    -> {assoc.name} "
                        f"({assoc.association_type.name}) "
                        f"\t-> {assoc.association_target.name} "
                        f"[{assoc.multiplicity.name}]\n"
                    )

        return result


# ---------------------------------------------------------------------------
# MetaModel
# ---------------------------------------------------------------------------


@dataclass(eq=True)
class MetaModel(MetaElement):
    """Represents the root container of the meta-model.

    Attributes:
        name: Name of the meta-model.
        classes: Contained meta-classes.
        enums: Contained enumerations.
    """

    name: str = field(default="root")
    classes: list[MetaClass] = field(default_factory=list)
    enums: list[MetaEnum] = field(default_factory=list)

    def validate(self) -> None:
        """Validate the meta-model and its contained elements.

        Raises:
            ValueError: If the name is empty.
        """
        for cls in self.classes:
            cls.validate()

        for enum in self.enums:
            enum.validate()

        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaModel must have a non-empty name.")

    def pretty(self, indent: int = 0) -> str:
        """Return a human-readable representation of the meta-model.

        Args:
            indent: Number of indentation spaces.

        Returns:
            Formatted string representation.
        """
        pad = " " * indent

        result = f"{pad} MetaModel: {self.name}\n"

        if self.enums:
            result += f"{pad}   Enums:\n"
            for enum in self.enums:
                result += enum.pretty(indent + 4)

        if self.classes:
            result += f"{pad}   Classes:\n"
            for cls in self.classes:
                result += cls.pretty(indent + 4)

        return result

    def add_class(self, cls: MetaClass):
        """Add a class to the meta-model.

        Args:
            cls: Class to add.

        Raises:
            ValueError: If a class with the same name already exists.
        """
        if any(c.name == cls.name for c in self.classes):
            raise ValueError(
                f"A metaclass with the name {cls.name}"
                + f"already exists in the MetaModel {self.name}"
            )
        self.classes.append(cls)

    def add_enum(self, enum: MetaEnum) -> None:
        """Add an enumeration to the meta-model.

        Args:
            enum: Enumeration to add.

        Raises:
            ValueError: If an enumeration with the same name already exists.
        """
        if any(e.name == enum.name for e in self.enums):
            raise ValueError(
                f"The Enum with the name {enum.name}"
                + f"already exists in the MetaModel {self.name}"
            )
        self.enums.append(enum)
