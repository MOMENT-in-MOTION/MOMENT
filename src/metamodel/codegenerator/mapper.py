from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from pathlib import Path

from ...metameta.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    Association,
    TypeOptions,
    Attribute,
    MetaModel,
    MultiplicityOptions,
    OpenAssociation
)

logger = logging.getLogger(__name__)

class Visitor(ABC):
    """
    Abstract visitor base for descriptor traversal.
    """

    @abstractmethod
    def visit_class(self, class_descriptor: ClassDescriptor) -> None: 
        pass

    @abstractmethod
    def visit_field(self, field_descriptor: FieldDescriptor) -> None:
        pass

    @abstractmethod
    def visit_enum(self, enum_descriptor: EnumDescriptor) -> None:
        pass

    def visit_context(self, context: Context) -> None:
        """Traverse all classes and enums in the context."""
        for cls in context.classes:
            self.visit_class(cls)

        for enum in context.enums:
            self.visit_enum(enum)


class Descriptor(ABC):
    """
    Abstract base for all template descriptors.
    """
    @abstractmethod
    def accpet(self, visitor: Visitor) -> None:
        pass


@dataclass(eq=True)
class FieldDescriptor(Descriptor):
    """
    Describes a single field on a generated class.

    Stores the raw building blocks separately so that renaming a class
    (base_type) never corrupts the multiplicity wrapping, and so that
    default formatting can inspect each part independently.

    Attributes:
        field_name:       Python identifier for the field.
        base_type:        The unwrapped type name, e.g. 'str', 'MyClass'.
        multiplicity:     Cardinality of the field.
        default:          Raw default value string from the metamodel, or None.
        is_association:   True when derived from an Association.
        is_meta_enum:     True when base_type refers to a MetaEnum.
        association_kind: 'composition', 'reference', or None.
    """
    field_name: str
    base_type: str
    multiplicity: MultiplicityOptions
    is_association: bool
    is_meta_enum: bool
    association_kind: str | None
    default: str | None

    @classmethod
    def from_association(cls, association: Association) -> FieldDescriptor:
        """
        Factory for building a FieldDescriptor form a association (reference to another class).

        Resolves the association's multiplicity against the target class name to
        produce the appropriate type hint and default value, then wraps everything
        in a FieldDescriptor.

        Args:
            association: The Association instance from the meta-model.
        """
        return cls(
            field_name=association.name,
            base_type=association.association_target.name,
            multiplicity=MultiplicityOptions(association.multiplicity or "ANY"),
            default=association.default_value,
            is_meta_enum=isinstance(association.association_target, MetaEnum),
            is_association=True,
            association_kind=cls._resolve_association(association.association_type),
        )

    @classmethod
    def from_attribute(cls, attribute: Attribute) -> FieldDescriptor:
        """
        Factory for building a FieldDescriptor form a attribute 

        Args:
            attribute: The Attribute instance from the meta-model.
        """
        primitive_type = cls._resolve_primitive_type(attribute.attribute_type)

        return cls(
            field_name=attribute.name,
            base_type=primitive_type,
            multiplicity=MultiplicityOptions(attribute.multiplicity or "ANY"),
            default=attribute.default_value,
            is_meta_enum=False,
            is_association=False,
            association_kind=None,
        )

    @property
    def type_hint(self) -> str:
        """Fully resolved type annotation, e.g. 'list[MyClass] | None'."""
        t = self.base_type
        if self.multiplicity.is_list:
            t = f"list[{t}]"
        if self.multiplicity.is_optional:
            t = f"{t} | None"
        return t

    @property
    def has_default(self) -> bool:
        return self.multiplicity.is_optional or self.default is not None

    @property
    def rendered_default(self) -> str | None:
        """Default expression ready for code generation, or None if omitted."""
        if self.multiplicity.is_optional and self.default is None:
            return "None"
        if self.default is None:
            return None
        if self.multiplicity.is_list:
            return self._render_list_default(self.default)
        return self._render_scalar_default(self.default)

    def accpet(self, visitor: Visitor) -> None:
        visitor.visit_field(self)

    def _render_scalar_default(self, value: str) -> str:
        if self.is_meta_enum:
            return f"{self.base_type}.{value}"
        if self.base_type in ("str",):
            return f'"{value}"'
        # int, bool is emited as-is
        return value

    def _render_list_default(self, values: list[str] | str) -> str:
        items = ", ".join(self._render_scalar_default(v) for v in values)
        return f"[{items}]"

    def _resolve_primitive_type(type_option: TypeOptions) -> str:
        """
        Maps a TypeOptions enum member to its Python type string.
        """
        if type_option in TypeOptions:
            return type_option.value
        raise TypeError(f"Expected TypeOptions enum, got {type_option}")

    def _resolve_association(association: str) -> str:
        """
        Normalize an association kind string to a canonical lower-case form.

        Args:
            association: The raw association kind string.
        """
        return association.lower()


@dataclass(eq=True)
class ClassDescriptor(Descriptor):
    """
    Describes a generated dataclass.
    Attributes:
        class_name:     The Python class name.
        fields:         Ordered list of field descriptors.
        sorted_fields:  Fields ordered so required fields precede optional ones
                        (a dataclass constraint).
    """
    class_name: str
    fields: list[FieldDescriptor]

    @classmethod
    def from_meta_class(cls, meta_class: MetaClass) -> ClassDescriptor:
        """
        Build a ClassDescriptor for a meta-model class.

        Iterates over all attributes and associations of the given MetaClass,
        converting each to a FieldDescriptor and collecting them into a single
        ClassDescriptor.

        Args:
            meta_class: The MetaClass instance to convert.
        """
        association_fields = []
        for assoc in meta_class.associations:
            if isinstance(assoc, OpenAssociation):
                logger.warning(
                    f"Association '{assoc.name}' in class '{meta_class.name}' is an OpenAssociation. "
                    f"It was not resolved and will be skipped in code generation."
                )
                continue
            association_fields.append(FieldDescriptor.from_association(assoc))

        return cls(
            class_name=meta_class.name,
            fields=[
                FieldDescriptor.from_attribute(attr)
                for attr in meta_class.attributes
            ] + association_fields,
        )

    @property
    def sorted_fields(self) -> list[FieldDescriptor]:
        """Required fields first, then fields with defaults."""
        return sorted(self.fields, key=lambda f: f.has_default)
    
    def accpet(self, visitor: Visitor) -> None:
        visitor.visit_class(self)


@dataclass(eq=True)
class EnumDescriptor(Descriptor):
    """
    Describes a generated Enum class.

    Attributes:
        enum_name: The Python class name.
        options:   The enum member names and values.
                   In a dictionary where each key is the member name
                   and each value the member value.
    """
    enum_name: str
    options: dict[str,str]

    @classmethod
    def from_meta_enum(cls, enum: MetaEnum):
        """
        Build an EnumDescriptor for a meta-model enumeration.

        Args:
            enum: The MetaEnum instance to convert.
        """
        enum_values: dict[str, str] = {}
        for meta_enum_literal in enum.values:
            enum_values[meta_enum_literal.name] = meta_enum_literal.value
        return cls(enum_name=enum.name, options=enum_values)
    
    def accpet(self, visitor: Visitor) -> None:
        visitor.visit_enum(self)


@dataclass
class TemplateContext:
    """
    Top-level object passed into every Jinja2 template.

    Bundles all descriptors a template may need, keeping templates
    free of metamodel types. Dependency ordering is the caller's responsibility.

    Attributes:
        classes: All class descriptors, in metamodel order.
        enums:   All enum descriptors, in declaration order.
    """
    classes: list[ClassDescriptor]
    enums: list[EnumDescriptor]

    @classmethod
    def from_meta_model(cls, meta_model: MetaModel) -> "TemplateContext":
        """Build a TemplateContext from a MetaModel instance."""
        return cls(
            classes=[ClassDescriptor.from_meta_class(c) for c in meta_model.classes],
            enums=[EnumDescriptor.from_meta_enum(e) for e in meta_model.enums],
        )
    
    def to_dict(self) -> dict:
        return {
            "classes": self.classes,
            "enums": self.enums,
        }
