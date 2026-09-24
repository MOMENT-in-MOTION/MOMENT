import logging
import re
from sre_constants import RANGE
from typing import TypeVar
from enum import Enum
from pathlib import Path
from typing import Literal
from ...metameta.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    MetaModel,
    Association,
    Attribute,
    OpenAssociation,
    Multiplicity,
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
ImportMode = Literal["merge", "import"]
_MODULE_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*(\.py)?$"
)


def parse_meta_model(
    meta_model_dict: MetaModelDict,
    import_mode: str = "merge",
) -> MetaModel:
    """Entry point for the parser builds a MetaModel from the given dict.

    Args:
        meta_model_dict (dict[str, str]): Dictionary containing the unstructured data of
        the MetaModel.
        import_mode (str): "merge" validates import_link as a path, "import" validates
        it as a Python module name or file name.

    Returns:
        MetaModel: The parsed MetaModel instance.
    """

    return _parse(meta_model_dict, import_mode=import_mode)


def _validate_import_link(
    import_link: str | None, import_mode: ImportMode
) -> str | None:
    """Validate the format of import_link depending on the active import mode.

    Raises:
        ValueError: If import_mode is unsupported or import_link doesn't match
            the expected format for the given mode.
    """
    if import_link is None:
        return None

    match import_mode:
        case "merge":
            return _validate_file_link(import_link)
        case "import":
            return _validate_module_link(import_link)
        case _:
            raise ValueError(
                f"Unsupported ImportMode '{import_mode}'. Allowed values are 'merge' and 'import'."
            )


def _validate_file_link(import_link: str) -> str:
    if not isinstance(import_link, str):
        raise ValueError(
            f"Invalid import_link for ImportMode='merge': expected a string path, got {type(import_link).__name__}."
        )
    if not import_link.strip():
        raise ValueError(
            f"Invalid import_link for ImportMode='merge': expected a file path, got empty string."
        )
    if Path(import_link).is_absolute() or "/" in import_link or "\\" in import_link:
        return import_link
    if _MODULE_PATTERN.fullmatch(import_link) and (
        "." in import_link or not import_link.lower().endswith(".json")
    ):
        raise ValueError(
            "Invalid import_link for ImportMode='merge': detected a module-style import "
            f"'{import_link}'. Merge mode expects a JSON file path. If this is an import-based "
            "model, set the config option 'ImportMode' to 'import'."
        )
    return import_link


def _validate_module_link(import_link: str) -> str:
    if not isinstance(import_link, str):
        raise ValueError(
            f"Invalid import_link for ImportMode='import': expected a module name or module.py, got {type(import_link).__name__}."
        )
    if Path(import_link).is_absolute() or "/" in import_link or "\\" in import_link:
        raise ValueError(
            "Invalid import_link for ImportMode='import': detected a file path "
            f"'{import_link}'. Import mode expects a Python module name. If this is a merge-based "
            "model, set the config option 'ImportMode' to 'merge'."
        )
    if not _MODULE_PATTERN.fullmatch(import_link):
        raise ValueError(
            f"Invalid import_link for ImportMode='import': expected module name, package.module, or module.py, got '{import_link}'."
        )
    return import_link


def _parse(meta_model_dict: MetaModelDict, import_mode: str = "merge") -> MetaModel:
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
                _build_classes(body, import_mode=import_mode)
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


def _build_classes(
    class_list: list[MetaClassDict], import_mode: str = "merge"
) -> list[MetaClass]:
    """Build MetaClass instances from the given list of class definitions."""
    finalised_classes: list[MetaClass] = []

    for cls in class_list:
        finalised_classes.append(
            _build_class(
                cls["name"],
                cls["attributes"],
                cls["associations"],
                cls["inherits"] if "inherits" in cls else [],
                import_mode=import_mode,
            )
        )

    return finalised_classes


def _build_class(
    class_name: str,
    class_attributes: list[MetaAttributesDict],
    class_associations: list[MetaAssociationsDict],
    class_inherits: list[str] | str,
    import_mode: str = "merge",
) -> MetaClass:
    """Build a MetaClass from the given class definition."""

    logger.debug(f"Building Class with name: '{class_name}'.")
    clazz = MetaClass(name=class_name)
    attributes: list[Attribute] = []
    associations: list[Association] | list[OpenAssociation] = []

    for attribute in class_attributes:
        attributes.append(_build_attribute(attribute))

    clazz.attributes = attributes

    for association in class_associations:
        associations.append(_build_association(association, import_mode=import_mode))

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

    if attribute_type := _test_enum_value(
        TypeOptions, attribute_values["attribute_type"]
    ):
        pass
    else:
        raise ValueError(
            f"The attribute type '{attribute_values['attribute_type']}' is"
            " not a valid TypeOption name."
        )

    return Attribute(
        name=attribute_values["name"],
        attribute_type=attribute_type,
        multiplicity=_parse_multiplicity(attribute_values["multiplicity"]),
        default_value=attribute_values.get("default_value"),
    )


_MULTIPLICITY_RE = re.compile(r"^\[(?P<lower>\d+)(?:\.\.(?P<upper>\d+|\*))?\]$")


def _parse_multiplicity(raw: str) -> Multiplicity:
    """Parse '[lower]', '[lower..upper]', or '[lower..*]'."""
    m = _MULTIPLICITY_RE.match(raw.strip())
    if not m:
        raise ValueError(
            f"Invalid multiplicity format: {raw!r}. "
            "Expected '[value]', '[lower..upper]', or '[lower..*]'."
        )
    lower = int(m.group("lower"))
    upper_raw = m.group("upper")  # None when no '..' present

    if upper_raw is None:
        # [1] case -> lower=1, upper=1
        upper = lower
    elif upper_raw == "*":
        # [1..*] case -> lower=1, upper=None
        upper = None
    else:
        # [1..4] case -> lower=1, upper=4
        upper = int(upper_raw)
        if upper < lower:
            raise ValueError(
                f"Multiplicity upper bound ({upper}) is less than "
                f"lower bound ({lower}) in {raw!r}."
            )

    mul = Multiplicity(lower=lower, upper=upper)
    return mul


def _build_association(
    association_values: MetaAssociationsDict,
    import_mode: str = "merge",
) -> OpenAssociation:
    """Build an Association from the given association definition."""
    if (
        missing := {"name", "multiplicity", "association_type", "target"}
        - association_values.keys()
    ):
        raise ValueError(
            f"Missing required keys: {missing} in association definition: {association_values}"
        )
    link_value = association_values.get("import_link")
    validated_link = _validate_import_link(link_value, import_mode)

    return OpenAssociation(
        name=association_values["name"],
        multiplicity=_parse_multiplicity(association_values["multiplicity"]),
        association_type=_test_enum_value(
            AssociationOptions, association_values["association_type"]
        ),
        association_target_name=association_values["target"],
        default_value=association_values.get("default_value"),
        import_link=validated_link,
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
