import logging
from metameta.api.m_m_m_classes import (
    MetaClass,
    MetaEnum,
    MetaModel,
    Association,
    Attribute,
    OpenReference,
)

logger = logging.getLogger(__name__)
CLASSES: dict[str, MetaClass] = {}
ENUMS: dict[str, MetaEnum] = {}


MULTIPLICITY_OPTIONS: MetaEnum = MetaEnum(
    name="MultiplicityOptions",
    values=["ONE", "AT_LEAST_ONE", "ANY", "ZERO_OR_ONE", "OPTIONAL"],
)
ASSOCIATION_OPTIONS: MetaEnum = MetaEnum(
    name="AssociationOptions", values=["COMPOSITION", "REFERENCE"]
)
TYPE_OPTIONS: MetaEnum = MetaEnum(name="TypeOptions", values=["INT", "BOOL", "STRING"])


def parse_meta_model(meta_model_dict: dict[str, str], verbose: bool=False) -> MetaModel:
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

    open_references: list[OpenReference] = []

    for class_name, body in meta_model_dict.items():
        if body.__class__ == list:
            _build_enums(class_name, body)
        else:
            _build_classes(class_name, body, open_references)

    _resolve_open_references(open_references)

    for clazz in CLASSES.values():
        root.add_class(clazz)

    for enum in ENUMS.values():
        root.add_enum(enum)

    root.validate()
    return root


def _resolve_open_references(open_refs: list[OpenReference]) -> None:
    for open_ref in open_refs:
        logger.info(
            f"Resolving open reference: {open_ref.association_target}"
            + f"in association {open_ref.name} of class {open_ref.association_origin.name}"
        )

        if open_ref.association_target in CLASSES:
            target_cls = CLASSES[open_ref.association_target]
        elif open_ref.association_target in ENUMS:
            target_cls = ENUMS[open_ref.association_target]
        else:
            continue

        open_ref.association_origin.add_association(
            Association(
                name=open_ref.name,
                multiplicity=open_ref.multiplicity,
                association=open_ref.association,
                association_target=target_cls,
            )
        )


def _build_classes(
    class_name: str, class_body: dict, open_references: list[OpenReference]
) -> MetaClass:
    """Recursively build a MetaClass and any classes it references."""

    clazz = MetaClass(name=class_name)
    CLASSES[class_name] = clazz

    for field_name, field_body in class_body.items():
        logger.info(f"Parsing field: {field_name} with body: {field_body}")

        logger.debug(f"Classifying field {field_name} in class {class_name}: {_classify_field(field_name, field_body)}")
        match _classify_field(field_name, field_body):

            case Attribute() as attr:
                logger.debug(f"Is attribute for {field_name} with type {attr.type} and multiplicity {attr.multiplicity}")
                clazz.add_attribute(attr)

            case ("comp_association", name, multiplicity, target_name, target_body):
                logger.debug(f"Is composition association for {name} with target {target_name} and multiplicity {multiplicity}")
                target_cls = _build_classes(target_name, target_body, open_references)

                logger.debug(f"Building association for {name} with target {target_name} and multiplicity {multiplicity}")

                default = "ANY" if not multiplicity else multiplicity
                multi = _test_enum_value(MULTIPLICITY_OPTIONS, default)

                clazz.add_association(
                    Association(
                        name=name,
                        multiplicity=multi,
                        association=_test_enum_value(
                            ASSOCIATION_OPTIONS, "COMPOSITION"
                        ),
                        association_target=target_cls,
                    )
                )

            case ("ref_association", name, multiplicity, target_name):
                logger.debug(f"Is reference association for {name} with target {target_name} and multiplicity {multiplicity}")
                default = "ANY" if not multiplicity else multiplicity
                multi = _test_enum_value(MULTIPLICITY_OPTIONS, default)

                if target_name in CLASSES:
                    target_cls = CLASSES[target_name]
                elif target_name in ENUMS:
                    target_cls = ENUMS[target_name]
                else:
                    open_references.append(
                        OpenReference(
                            association_origin=clazz,
                            name=name,
                            multiplicity=multi,
                            association=_test_enum_value(
                                ASSOCIATION_OPTIONS, "REFERENCE"
                            ),
                            association_target=target_name,
                        )
                    )
                    logger.debug(f"Appended open reference for {name} with target {target_name}")
                    continue

                clazz.add_association(
                    Association(
                        name=name,
                        multiplicity=multi,
                        association=_test_enum_value(ASSOCIATION_OPTIONS, "REFERENCE"),
                        association_target=target_cls,
                    )
                )

            case None:
                logger.debug(f"Field {field_name} is neither an attribute nor an association.")

    return clazz


def _classify_field(
    name: str, field_def: dict[str, any]
) -> Attribute | Association | None:
    """
    Parse the field and return the matching MetaElement, either a Attribute or Association.

    Patterns:
      Attribute  -> {"type": <str>,  "multiplicity": <str>} | {"type": <str>, "value": <str>}
      Association-> {"type": {<ClassName>: {...}}, "multiplicity": <str>}
    """
    multiplicity = field_def.get("multiplicity")
    value = field_def.get("value")
    type_val = field_def.get("type")

    match type_val:
        case str():
            if type_val == _test_enum_value(ASSOCIATION_OPTIONS, "REFERENCE"):
                target_val = field_def.get("target")
                return ("ref_association", name, multiplicity, target_val)
            if type_val == _test_enum_value(ASSOCIATION_OPTIONS, "COMPOSITION"):
                target_val = field_def.get("target")
                return ("comp_association", name, multiplicity, target_val)
            if type_val not in TYPE_OPTIONS.values:
                return ("ref_association", name, multiplicity, type_val)

            return Attribute(
                # TODO Potentially make Attribute have optional Multiplicity,
                # so that we don't end up wit None fields in the object.
                name=name,
                multiplicity=(
                    _test_enum_value(MULTIPLICITY_OPTIONS, multiplicity)
                    if multiplicity
                    else _test_enum_value(MULTIPLICITY_OPTIONS, "ONE")
                ),
                type=_test_enum_value(TYPE_OPTIONS, type_val),
                default_value=value
            )
        case {**nested} if nested:
            target_name, target_body = next(iter(nested.items()))
            return ("comp_association", name, multiplicity, target_name, target_body)
        case _:
            return None


def _build_enums(
    enum_name: str,
    enum_body: dict,
) -> MetaEnum:
    """Build a MetaEnum."""

    enum = MetaEnum(name=enum_name)
    ENUMS[enum_name] = enum

    enum.values = enum_body

    return enum


def _test_enum_value(meta_enum: MetaEnum, value: str):
    if value not in meta_enum.values:
        raise ValueError(
            f"'{value}' ist kein gültiger Wert für {meta_enum.name}. "
            f"Erlaubt: {meta_enum.values}"
        )
    return value
