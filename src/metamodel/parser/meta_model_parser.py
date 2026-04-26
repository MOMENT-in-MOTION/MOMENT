from metameta.api.m_m_m_classes import *


CLASSES: dict[str, MetaClass] = {}
ENUMS: dict[str, MetaEnum] = {}


def parse_meta_model(meta_model_dict: dict[str, str]) -> MetaMetaModel:
    """
    Entry point for the parser builds a MetaMetaModel from the given dict.
    """
    root = MetaMetaModel()

    for class_name, body in meta_model_dict.items():
        if body.__class__ == list:
            _build_enums(class_name, body)
        else:
            _build_classes(class_name, body)

    for clazz in CLASSES.values():
        root.add_class(clazz)

    for enum in ENUMS.values():
        root.add_enum(enum)

    root.validate()
    return root


def _build_classes(
    class_name: str,
    class_body: dict,
) -> MetaClass:
    """Recursively build a MetaClass and any classes it references."""

    clazz = MetaClass(name=class_name)
    CLASSES[class_name] = clazz

    for field_name, field_body in class_body.items():
        match _classify_field(field_name, field_body):

            case Attribute() as attr:
                clazz.add_attribute(attr)

            case ("comp_association", name, multiplicity, target_name, target_body):
                target_cls = _build_classes(target_name, target_body)
                clazz.add_association(Association(
                    name=name,
                    multiplicity=getattr(MultiplicityOptions, multiplicity).name,
                    association=AssociationOptions.COMPOSITION,
                    associationTarget=target_cls,
                ))
            
            case ("ref_association", name, multiplicity, target_name):
                if target_name in CLASSES:
                    target_cls = CLASSES[target_name]
                elif target_name in ENUMS:
                    target_cls = ENUMS[target_name]

                clazz.add_association(Association(
                    name=name,
                    multiplicity=getattr(MultiplicityOptions, multiplicity).name,
                    association=AssociationOptions.REFERENCE,
                    associationTarget=target_cls,
                ))

            case None:
                pass

    return clazz


def _classify_field(name: str, field_def: dict[str, any]) -> Attribute | Association | None:
    """
    Parse the field and return the matching MetaElement, either a Attribute or Association.
    
    Patterns:
      Attribute  -> {"type": <str>,  "multiplicity": <str>}
      Association-> {"type": {<ClassName>: {...}}, "multiplicity": <str>}
    """
    multiplicity = field_def.get("multiplicity")
    type_val     = field_def.get("type")

    match type_val:
        case str():
            if type_val not in TypeOptions.__members__:
                return ("ref_association", name, multiplicity, type_val)

            return Attribute(
                name=name,
                multiplicity=getattr(MultiplicityOptions, multiplicity).name,
                type=getattr(TypeOptions, type_val).name,
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
