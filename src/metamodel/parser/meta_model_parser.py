import logging
from sre_constants import RANGE
from sre_constants import RANGE
from typing import TypeVar
from enum import Enum
from pathlib import Path
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
from ...metameta.m_m_m_dicts import (
    MetaModelDict,
    MetaAssociationsDict,
    MetaClassDict,
    MetaAttributesDict,
    MetaEnumLiteralDict,
)

CLASSES: dict[str, MetaClass] = {}
ENUMS: dict[str, MetaEnum] = {}
logger = logging.getLogger(__name__)
E = TypeVar("E", bound=Enum)


def parse_meta_model(meta_model_dict: MetaModelDict) -> MetaModel:
    """Entry point for the parser builds a MetaModel from the given dict.

    Args:
        meta_model_dict (dict[str, str]): Dictionary containing the unstructured data of
        the MetaModel.
        verbose (bool, optional): A flag to enable verbose logging. Defaults to False.

    Returns:
        MetaModel: The parsed MetaModel instance.
    """

    return _parse(meta_model_dict)


def _parse(meta_model_dict: MetaModelDict) -> MetaModel:
    """Parse the given dictionary to build a MetaModel instance."""
    root = MetaModel()

    for key, body in meta_model_dict.items():
        logger.debug(f"Key: '{key}' with body: '{body}' and type: '{type(body)}'")
        match key.lower():
            case "name":
                root.name = body
            case "enums":
                _build_enums(body)
            case "classes":
                _build_classes(body)
            case _:
                logger.warning(f"Unrecognized top-level key: {key}")

    logger.debug(f"All classes: {CLASSES.keys()}")
    for clazz in CLASSES.values():
        root.add_class(clazz)

    logger.debug(f"All Enums: {ENUMS.keys()}")
    for enum in ENUMS.values():
        root.add_enum(enum)

    root.validate()
    CLASSES.clear()
    ENUMS.clear()

    return root


def _build_classes(class_list: list[MetaClassDict]) -> list[MetaClass]:
    """Build MetaClass instances from the given list of class definitions."""
    finalised_classes: list[MetaClass] = []

    for cls in class_list:
        finalised_classes.append(
            _build_class(
                cls["name"],
                cls["attributes"],
                cls["associations"],
                cls["inherits"] if "inherits" in cls else []
            )
        )

    return finalised_classes


def _build_class(
    class_name: str,
    class_attributes: list[MetaAttributesDict],
    class_associations: list[MetaAssociationsDict],
    class_inherits: list[str] | str
) -> MetaClass:
    """Build a MetaClass from the given class definition."""

    logger.debug(f"Building Class with name: '{class_name}'.")
    clazz = MetaClass(name=class_name)
    attributes: list[Attribute] = []
    associations: list[Association]|list[OpenAssociation] = []

    for attribute in class_attributes:
        attributes.append(_build_attribute(attribute))

    clazz.attributes = attributes

    for association in class_associations:
        associations.append(_build_association(association))

    clazz.associations = associations

    if isinstance(class_inherits, str):
        clazz.inherits = [class_inherits]
    else:
        clazz.inherits = class_inherits

    CLASSES[class_name] = clazz

    return clazz


def _build_enums(enum_list: list[MetaModelDict]) -> list[MetaEnum]:
    """Build MetaEnum instances from the given list of enum definitions."""
    enums: list[MetaEnum] = []

    for enum in enum_list:
        if not isinstance(enum, dict):
            raise ValueError(f"Expected a dict, got {type(enum)}")
        enums.append(_build_enum(enum["name"], enum["values"]))

    return enums


def _build_enum(
    enum_name: str,
    enum_values: list[MetaEnumLiteralDict] | list[str],
) -> MetaEnum:
    """Build a MetaEnum from the given enum definition."""

    enum = MetaEnum(name=enum_name)
    ENUMS[enum_name] = enum

    for value in enum_values:
        enum.values.append(_build_enum_literal(value))

    return enum


def _build_enum_literal(enum_value: MetaEnumLiteralDict | str) -> MetaEnumLiteral:
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


def _build_attribute(attribute_values: MetaAttributesDict) -> Attribute:
    """Build an Attribute from the given attribute definition."""

    if missing := {"name", "attribute_type", "multiplicity"} - attribute_values.keys():
        raise ValueError(
            f"Missing required keys: {missing} in attribute definition: {attribute_values}"
        )

    if (
        attribute_type := _test_enum_value(
            TypeOptions, attribute_values["attribute_type"]
        )
    ):
        pass
    else:
        raise ValueError(
            f"The attribute type '{attribute_values['attribute_type']}' is"
            " not a valid TypeOption name."
        )
    
    #if multiplicity is a range or a value, we parse it and set lower and upper bounds accordingly
    #Values are represented by equal lower and upper bounds.
    if "[" in attribute_values["multiplicity"] and "]" in attribute_values["multiplicity"]:
            multiplicity_lower_bound = None
            multiplicity_upper_bound = None
            MultiplicityType = MultiplicityOptions.RANGE
            if ".." in attribute_values["multiplicity"]:
                bounds = attribute_values["multiplicity"].strip("[]").split("..")
                if len(bounds) != 2:
                    raise ValueError(
                        f"Invalid multiplicity format: {attribute_values["multiplicity"]}"
                    )
                try:
                    multiplicity_lower_bound = int(bounds[0])
                    multiplicity_upper_bound = int(bounds[1])
                except ValueError as e:
                    raise ValueError(
                        f"Invalid multiplicity bounds: {attribute_values["multiplicity"]}"
                    ) from e
            elif attribute_values["multiplicity"].strip("[]").isdigit():
                MultiplicityType = MultiplicityOptions.VALUE
                multiplicity_lower_bound = int(attribute_values["multiplicity"].strip("[]"))
                multiplicity_upper_bound = multiplicity_lower_bound
            return Attribute(
                name=attribute_values["name"],
                attribute_type=attribute_type,
                multiplicity=MultiplicityType,
                default_value=attribute_values.get("default_value"),
                multiplicity_lower_bound=multiplicity_lower_bound,
                multiplicity_upper_bound=multiplicity_upper_bound
            )
    else:
        return Attribute(
            name=attribute_values["name"],
            attribute_type=attribute_type,
            multiplicity=_test_enum_value(
                MultiplicityOptions, attribute_values["multiplicity"]
            ),
            default_value=attribute_values.get("default_value"),
            multiplicity_lower_bound=None,
            multiplicity_upper_bound=None
        )


def _build_association(association_values: MetaAssociationsDict) -> OpenAssociation:
    """Build an Association from the given association definition."""
    if (
        missing := {"name", "multiplicity", "association_type", "target"}
        - association_values.keys()
    ):
        raise ValueError(
            f"Missing required keys: {missing} in attribute definition: {association_values}"
        )
    link_value = association_values.get("import_link")

    #if multiplicity is a range or a value, we parse it and set lower and upper bounds accordingly
    #Values are represented by equal lower and upper bounds.
    if "[" in association_values["multiplicity"] and "]" in association_values["multiplicity"]:
            multiplicity_lower_bound = None
            multiplicity_upper_bound = None
            MultiplicityType = MultiplicityOptions.RANGE
            if ".." in association_values["multiplicity"]:
                bounds = association_values["multiplicity"].strip("[]").split("..")
                if len(bounds) != 2:
                    raise ValueError(
                        f"Invalid multiplicity format: {association_values["multiplicity"]}"
                    )
                try:
                    multiplicity_lower_bound = int(bounds[0])
                    multiplicity_upper_bound = int(bounds[1])
                except ValueError as e:
                    raise ValueError(
                        f"Invalid multiplicity bounds: {association_values["multiplicity"]}"
                    ) from e
            elif association_values["multiplicity"].strip("[]").isdigit():
                MultiplicityType = MultiplicityOptions.VALUE
                multiplicity_lower_bound = int(association_values["multiplicity"].strip("[]"))
                multiplicity_upper_bound = multiplicity_lower_bound
            return OpenAssociation(
                name=association_values["name"],
                multiplicity=MultiplicityType,
                association_type=_test_enum_value(
                    AssociationOptions, association_values["association_type"]
                ),
                association_target_name=association_values["target"],
                default_value=association_values.get("default_value"),
                import_link= Path(link_value) if link_value and isinstance(link_value, str) else None,
                multiplicity_lower_bound=multiplicity_lower_bound,
                multiplicity_upper_bound=multiplicity_upper_bound
            )
    else :
        return OpenAssociation(
            name=association_values["name"],
            multiplicity=_test_enum_value(
                MultiplicityOptions, association_values["multiplicity"]
            ),
            association_type=_test_enum_value(
                AssociationOptions, association_values["association_type"]
            ),
            association_target_name=association_values["target"],
            default_value=association_values.get("default_value"),
            import_link= Path(link_value) if link_value and isinstance(link_value, str) else None
        )


def _test_enum_value(enum: E, value: str) -> E:
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


def _find_in_meta_enums(enum_name: str) -> MetaEnum | None:
    """Search for a MetaEnum with the given name and return it if found."""
    return ENUMS.get(enum_name)
