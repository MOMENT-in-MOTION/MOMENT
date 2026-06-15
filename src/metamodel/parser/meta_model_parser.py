import logging
from enum import Enum
from ...metameta.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    MetaModel,
    Association,
    Attribute,
    OpenAssociation,
    MultiplicityOptions,
    AssociationOptions,
    TypeOptions,
)

from .helper import structure_data

CLASSES: dict[str, MetaClass] = {}
ENUMS: dict[str, MetaEnum] = {}
logger = logging.getLogger(__name__)


def parse_meta_model(
    meta_model_dict: dict[str, str]) -> MetaModel:
    """Entry point for the parser builds a MetaModel from the given dict.

    Args:
        meta_model_dict (dict[str, str]): Dictionary containing the unstructured data of
        the MetaModel.
        verbose (bool, optional): A flag to enable verbose logging. Defaults to False.

    Returns:
        MetaModel: The parsed MetaModel instance.
    """

    return _parse(structure_data(meta_model_dict))


def _parse(meta_model_dict: dict) -> MetaModel:
    """Parse the given dictionary to build a MetaModel instance."""
    root = MetaModel()

    for key, body in meta_model_dict.items():
        logger.debug(f"Key: {key} with body: {body} and type: {type(body)}")
        match key.lower():
            case "name":
                (root.name,) = body
            case "enums":
                _build_enums(body)
            case "classes":
                _build_classes(body)
            case _:
                logger.warning(f"Unrecognized top-level key: {key}")

    logger.debug(f"All classes: {CLASSES.keys()}")
    for clazz in CLASSES.values():
        _resolve_open_references(clazz)
        root.add_class(clazz)

    logger.debug(f"All Enums: {ENUMS.keys()}")
    for enum in ENUMS.values():
        root.add_enum(enum)

    root.validate()
    CLASSES.clear()
    ENUMS.clear()

    return root


def _resolve_open_references(cls: MetaClass) -> None:
    """Check the associations of the given class for any OpenAssociations
    and tries to resolve them."""
    for open_association in cls.associations[:]:
        if isinstance(open_association, OpenAssociation):
            if target_class := CLASSES.get(open_association.association_target_name):
                cls.associations.append(open_association.to_association(target_class))
                cls.associations.remove(open_association)
            elif target_enum := ENUMS.get(open_association.association_target_name):
                cls.associations.append(open_association.to_association(target_enum))
                cls.associations.remove(open_association)
            else:
                raise ValueError(
                    f"No class or enum with name '{open_association.association_target}'"
                    " found for association '{open_association.name}' in class '{cls.name}'."
                )


def _build_classes(class_list: list) -> list[MetaClass]:
    """Build MetaClass instances from the given list of class definitions."""
    finalised_classes: list[MetaClass] = []

    for cls in class_list:
        finalised_classes.append(
            _build_class(cls["name"], cls["attributes"], cls["associations"])
        )

    return finalised_classes


def _build_class(
    class_name: str, class_attributes: list, class_associations: list
) -> MetaClass:
    """Build a MetaClass from the given class definition."""

    logger.debug(f"Building Class with name: '{class_name}'.")
    clazz = MetaClass(name=class_name)
    attributes: list[Attribute] = []
    associations: list[Association] = []

    for attribute in class_attributes:
        attributes.append(_build_attribute(attribute))

    clazz.attributes = attributes

    for association in class_associations:
        associations.append(_build_association(association))

    clazz.associations = associations

    CLASSES[class_name] = clazz

    return clazz


def _build_enums(enum_list: list[MetaEnum]) -> list[MetaEnum]:
    """Build MetaEnum instances from the given list of enum definitions."""
    enums: list[MetaEnum] = []

    if enum_list is None:
        return enums
    if not isinstance(enum_list, list):
        raise ValueError(f"Expected a list, got {type(enum_list)}")

    for enum in enum_list:
        if not isinstance(enum, dict):
            raise ValueError(f"Expected a dict, got {type(enum)}")
        enums.append(_build_enum(enum["name"], enum["values"]))

    return enums


def _build_enum(
    enum_name: str,
    enum_values: dict,
) -> MetaEnum:
    """Build a MetaEnum from the given enum definition."""

    enum = MetaEnum(name=enum_name)
    ENUMS[enum_name] = enum

    for value in enum_values:
        enum.values.append(_build_enum_literal(value))

    return enum


def _build_enum_literal(enum_value) -> MetaEnumLiteral:
    """Build a MetaEnumLiteral from the given enum literal definition."""

    if isinstance(enum_value, str):
        return MetaEnumLiteral(enum_value.upper(), enum_value)
    if isinstance(enum_value, dict):
        try:
            return MetaEnumLiteral(enum_value["name"].upper(), enum_value["value"])
        except KeyError as e:
            raise KeyError(f"Dict is missing required key: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid value type in dict: {e}") from e
    else:
        raise ValueError(f"Invalid enum value: {enum_value}")


def _build_attribute(attribute_values: dict) -> Attribute:
    """Build an Attribute from the given attribute definition."""

    if missing := {"name", "attribute_type", "multiplicity"} - attribute_values.keys():
        raise ValueError(
            f"Missing required keys: {missing} in attribute definition: {attribute_values}"
        )

    if (
        attribute_type := _test_enum_value(
            TypeOptions, attribute_values["attribute_type"]
        )
    ) or (attribute_type := _find_in_meta_enums(attribute_values["attribute_type"])):
        pass
    else:
        raise ValueError(
            f"The attribute type '{attribute_values['attribute_type']}' is"
            " not a valid TypeOption or Enum name."
        )

    return Attribute(
        name=attribute_values["name"],
        attribute_type=attribute_type,
        multiplicity=_test_enum_value(
            MultiplicityOptions, attribute_values["multiplicity"]
        ),
        default_value=attribute_values.get("default_value"),
    )


def _build_association(association_values: dict) -> Association:
    """Build an Association from the given association definition."""
    if (
        missing := {"name", "multiplicity", "association_type", "target"}
        - association_values.keys()
    ):
        raise ValueError(
            f"Missing required keys: {missing} in attribute definition: {association_values}"
        )

    return OpenAssociation(
        # association_origin=cls, #TODO besprechen, für zweiseitige Referenzen?
        name=association_values["name"],
        multiplicity=_test_enum_value(
            MultiplicityOptions, association_values["multiplicity"]
        ),
        association_type=_test_enum_value(
            AssociationOptions, association_values["association_type"]
        ),
        association_target_name=association_values["target"],
    )


def _test_enum_value(enum: Enum, value: str) -> Enum | None:
    """Test if the given value is a valid name or value for the given enum and
    return the corresponding Enum member if it is"""
    for member in enum:
        if member.value == value:
            return member
    try:
        return enum[value]
    except KeyError:
        allowed_values = [m.value for m in enum]
        allowed_names = [m.name for m in enum]
        logger.debug(
            f"'{value}' is no valid name or value for {enum.__name__}. "
            f"Allowed names: {allowed_names}, allowed values: {allowed_values}"
        )
    return None


def _find_in_meta_enums(enum_name: str) -> MetaEnum | None:
    """Search for a MetaEnum with the given name and return it if found."""
    if enum := ENUMS.get(enum_name):
        return enum
    return None
