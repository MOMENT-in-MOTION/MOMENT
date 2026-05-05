from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------

class MetaElement(ABC):
    """Base class for all elements of the Meta-Meta-Model."""
    @abstractmethod
    def validate(self):
        """Method to validate the MetaClass instance. Must be implemented by all subclasses."""

# ---------------------------------------------------------------------------
# METACLASS Enumeration
# ---------------------------------------------------------------------------

@dataclass(eq=True)
class MetaEnum(MetaElement):
    """Represents an enumeration in the Meta-Meta-Model."""
    name: str
    values: list[str]   = field(default_factory=list)

    def validate(self) -> None:
        if not self.values:
            raise ValueError(f"The MetaEnum '{self.name}' has no values.")

        if len(self.values) != len(set(self.values)):
            raise ValueError(f"The MetaEnum '{self.name}' has duplicate values.")

# ---------------------------------------------------------------------------
# METACLASS Core Elements
# ---------------------------------------------------------------------------

@dataclass(eq=True)
class Attribute(MetaElement):
    """Represents an attribute belonging to a MetaClass in the Meta-Meta-Model."""
    name                : str
    multiplicity        : MetaEnum
    type                : MetaEnum

    def validate(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("The Attribute must have a non-empty name.")

@dataclass(eq=True)
class Association(MetaElement):
    """Represents a directed association between two MetaClass instances."""
    name                : str
    multiplicity        : MetaEnum
    association         : MetaEnum
    association_target   : MetaClass

    def validate(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("The Association must have a non-empty name.")

@dataclass(eq=True)
class OpenReference(MetaElement):
    """Represents an unresolved reference within the Meta-Meta-Model."""
    association_origin  : MetaClass
    name                : str
    multiplicity        : MetaEnum
    association         : MetaEnum
    association_target   : MetaClass | str

    def validate(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("The Association must have a non-empty name.")

# ---------------------------------------------------------------------------
# METACLASS Class
# ---------------------------------------------------------------------------

@dataclass(eq=True)
class MetaClass(MetaElement):
    """Represents a class definition in the Meta-Meta-Model."""
    name            : str
    attributes      : list[Attribute]   = field(default_factory=list)
    associations    : list[Association] = field(default_factory=list)

    def validate(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaClass must have a non-empty name.")
        for attribute in self.attributes:
            attribute.validate()
        for association in self.associations:
            association.validate()

    def add_attribute(self, attribute: Attribute) -> None:
        if any(a.name == attribute.name for a in self.attributes):
            raise ValueError(f"The attribute with the name {attribute.name} " +
                f"already exists in the MetaClass {self.name}")
        self.attributes.append(attribute)

    def add_association(self, association: Association) -> None:
        if any (a.name == association.name for a in self.associations):
            raise ValueError(f"The association with the name {association.name}" +
                f"already exists in the MetaClass {self.name}")
        self.associations.append(association)

# ---------------------------------------------------------------------------
# MetaModel
# ---------------------------------------------------------------------------


@dataclass(eq=True)
class MetaModel(MetaElement):
    """Represents the top-level container that holds all Meta-Meta-Model elements."""
    name    : str                = field(default="root", init=False)
    classes : list[MetaClass]    = field(default_factory=list)
    enums   : list[MetaEnum]    = field(default_factory=list)

    def validate(self) -> None:
        for cls in self.classes:
            cls.validate()

        for enum in self.enums:
            enum.validate()

        if not self.name or self.name.strip() == "":
            raise ValueError("The MetaMetaModel must have a non-empty name.")

    def add_class(self, cls: MetaClass):
        if any(c.name == cls.name for c in self.classes):
            raise ValueError(f"A metaclass with the name {cls.name}" +
                f"already exists in the MetaMetaModel {self.name}")
        self.classes.append(cls)

    def add_enum(self, enum: MetaEnum) -> None:
        if any (e.name == enum.name for e in self.enums):
            raise ValueError(f"The Enum with the name {enum.name}" +
                f"already exists in the MetaClass {self.name}")
        self.enums.append(enum)
