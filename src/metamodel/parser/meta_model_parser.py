import logging
from metameta.api.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    MetaModel,
    Association,
    Attribute,
    OpenAssociation,
)

logger = logging.getLogger(__name__)
CLASSES: dict[str, MetaClass] = {}
ENUMS: dict[str, MetaEnum] = {}


MULTIPLICITY_OPTIONS: MetaEnum = MetaEnum(
    name="MultiplicityOptions",
    values=[
        MetaEnumLiteral(name="ONE", value="ONE"),
        MetaEnumLiteral(name="AT_LEAST_ONE", value="AT_LEAST_ONE"),
        MetaEnumLiteral(name="ANY", value="ANY"),
        MetaEnumLiteral(
            name="ZERO_OR_ONE", value="ZERO_OR_ONE"
        ),  # Redundant with "OPTIONAL", but may be useful for readability in some cases.
        MetaEnumLiteral(name="OPTIONAL", value="OPTIONAL"),
    ],
)
ASSOCIATION_OPTIONS: MetaEnum = MetaEnum(
    name="AssociationOptions",
    values=[
        MetaEnumLiteral(name="COMPOSITION", value="COMPOSITION"),
        MetaEnumLiteral(name="REFERENCE", value="REFERENCE"),
    ],
)
TYPE_OPTIONS: MetaEnum = MetaEnum(
    name="TypeOptions",
    values=[
        MetaEnumLiteral(name="INT", value="int"),
        MetaEnumLiteral(name="BOOL", value="bool"),
        MetaEnumLiteral(name="STRING", value="str"),
    ],
)


def parse_meta_model(
    meta_model_dict: dict[str, str], verbose: bool = False
) -> MetaModel:
    """
    Entry point for the parser builds a MetaModel from the given dict.
    """
    logging.basicConfig(
        format="%(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled. Logging set to DEBUG level.")
    if not verbose:
        logger.setLevel(logging.INFO)
        logger.info("Verbose mode disabled. Logging set to INFO level.")

    root = MetaModel()

    for key, body in meta_model_dict.items():
        logger.debug(f"Key: {key} with body: {body} and type: {type(body)}")
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
        _resolve_open_references(clazz)
        root.add_class(clazz)

    logger.debug(f"All Enums: {ENUMS.keys()}")
    for enum in ENUMS.values():
        root.add_enum(enum)

    root.validate()
    return root


def _resolve_open_references(cls: MetaClass) -> None:

    for open_association in cls.associations[:]:
        if isinstance(open_association, OpenAssociation):
            if target_class := CLASSES.get(open_association.association_target):
                cls.associations.append(open_association.to_association(target_class))
                cls.associations.remove(open_association)
            elif target_enum := ENUMS.get(open_association.association_target):
                cls.associations.append(open_association.to_association(target_enum))
                cls.associations.remove(open_association)
            else:
                raise KeyError(
                    f"No class or enum with name '{open_association.association_target}' found for association '{open_association.name}' in class '{cls.name}'."
                )


def _build_classes(class_list: list) -> list[MetaClass]:
    finalised_classes: list[MetaClass] = []

    for cls in class_list:
        finalised_classes.append(
            _build_class(cls["name"], cls["attributes"], cls["associations"])
        )

    return finalised_classes


def _build_class(
    class_name: str, class_attributes: list, class_associations: list
) -> MetaClass:
    """Recursively build a MetaClass and any classes it references."""

    logger.debug(f"Building Class with name: '{class_name}'.")
    clazz = MetaClass(name=class_name)
    attributes: list[Attribute] = []
    associations: list[Association] = []

    for attribute in class_attributes:
        attributes.append(_build_attribute(attribute))

    clazz.attributes = attributes

    for association in class_associations:
        associations.append(_build_association(clazz, association))

    clazz.associations = associations

    CLASSES[class_name] = clazz

    return clazz


def _build_enums(enum_list: list[MetaEnum]) -> list[MetaEnum]:
    enums: list[MetaEnum] = []

    if enum_list is None:
        return
    elif not isinstance(enum_list, list):
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
    """Build a MetaEnum."""

    enum = MetaEnum(name=enum_name)
    ENUMS[enum_name] = enum

    for value in enum_values:
        enum.values.append(_build_enum_literal(value))

    TYPE_OPTIONS.add_value(value_name=enum_name.upper(), value=enum_name)

    return enum


def _build_enum_literal(enum_value) -> MetaEnumLiteral:

    if isinstance(enum_value, str):
        return MetaEnumLiteral(enum_value.upper(), enum_value)
    elif isinstance(enum_value, dict):
        try:
            return MetaEnumLiteral(enum_value["name"].upper(), enum_value["value"])
        except KeyError as e:
            raise ValueError(f"Dict is missing the required Key: {e}")
    else:
        raise ValueError(f"Invalid enum value: {enum_value}")


def _build_attribute(attribute_values: dict) -> Attribute:

    if missing := {"name", "attribute_type", "multiplicity"} - attribute_values.keys():
        raise KeyError(
            f"Missing required keys: {missing} in attribute definition: {attribute_values}"
        )

    return Attribute(
        name=attribute_values["name"],
        attribute_type=_test_enum_value(
            TYPE_OPTIONS, attribute_values["attribute_type"]
        ),
        multiplicity=_test_enum_value(
            MULTIPLICITY_OPTIONS, attribute_values["multiplicity"]
        ),
        default_value=attribute_values.get("default_value"),
    )


def _build_association(cls: MetaClass, association_values: dict) -> Association:
    if (
        missing := {"name", "multiplicity", "association_type", "target"}
        - association_values.keys()
    ):
        raise KeyError(
            f"Missing required keys: {missing} in attribute definition: {association_values}"
        )

    return OpenAssociation(
        # association_origin=cls, #TODO besprechen, für zweiseitige Referenzen?
        name=association_values["name"],
        multiplicity=_test_enum_value(
            MULTIPLICITY_OPTIONS, association_values["multiplicity"]
        ),
        association_type=_test_enum_value(
            ASSOCIATION_OPTIONS, association_values["association_type"]
        ),
        association_target=association_values["target"],
    )


def _test_enum_value(meta_enum: MetaEnum, value: str) -> MetaEnumLiteral:
    for enum_literal in meta_enum.values:
        if value == enum_literal.name or value == enum_literal.value:
            return enum_literal
    raise ValueError(
        f"'{value}' is no valid value for {meta_enum.name}. "
        f"Allowed: {meta_enum.values}"
    )
