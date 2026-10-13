"""Unit tests for the meta-model parser.

Import-link / ImportMode validation is covered separately in
tests/unit/test_import_mode_validation.py.
"""

import pytest

from src.metamodel.parser import meta_model_parser as parser_module
from src.metamodel.parser.meta_model_parser import (
    _build_enum,
    _build_enum_literal,
    _find_in_meta_enums,
    _parse_multiplicity,
    _test_enum_value,
    parse_meta_model,
)
from src.metameta.m_m_m_classes import (
    Association,
    AssociationOptions,
    Attribute,
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    MetaModel,
    Multiplicity,
    OpenAssociation,
    TypeOptions,
)


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_parser_caches():
    """Clear the module-level CLASSES/ENUMS caches around every test.

    A successful parse clears them itself, but a parse that raises leaves its
    partial state behind, which would leak into the next test.
    """
    parser_module.CLASSES.clear()
    parser_module.ENUMS.clear()
    yield
    parser_module.CLASSES.clear()
    parser_module.ENUMS.clear()


def model(name: str = "demo", enums: list | None = None, classes: list | None = None):
    """Build a top-level model dict with the given enums and classes."""
    return {
        "name": name,
        "enums": enums if enums is not None else [],
        "classes": classes if classes is not None else [],
    }


def meta_class(name: str, attributes=None, associations=None, inherits=None):
    """Build a class dict with sensible empty defaults."""
    cls = {
        "name": name,
        "attributes": attributes if attributes is not None else [],
        "associations": associations if associations is not None else [],
    }
    if inherits is not None:
        cls["inherits"] = inherits
    return cls


def get_class(parsed: MetaModel, name: str) -> MetaClass:
    return next(c for c in parsed.classes if c.name == name)


def get_enum(parsed: MetaModel, name: str) -> MetaEnum:
    return next(e for e in parsed.enums if e.name == name)


def get_attribute(cls: MetaClass, name: str) -> Attribute:
    return next(a for a in cls.attributes if a.name == name)


def get_association(cls: MetaClass, name: str) -> Association | OpenAssociation:
    return next(a for a in cls.associations if a.name == name)


# ---------------------------------------------------------------------------
# Model level
# ---------------------------------------------------------------------------


def test_parse_meta_model_returns_meta_model():
    """Test that parsing returns a MetaModel instance."""
    parsed = parse_meta_model(model())
    assert isinstance(parsed, MetaModel)


def test_parse_meta_model_sets_model_name():
    """Test that the top-level name key becomes the model name."""
    parsed = parse_meta_model(model(name="library"))
    assert parsed.name == "library"


def test_parse_meta_model_accepts_uppercase_top_level_keys():
    """Test that top-level keys are matched case-insensitively."""
    parsed = parse_meta_model(
        {"Name": "library", "ENUMS": [], "Classes": [meta_class("Book")]}
    )
    assert parsed.name == "library"
    assert [c.name for c in parsed.classes] == ["Book"]


def test_parse_meta_model_ignores_unrecognized_top_level_keys():
    """Test that an unknown top-level key is skipped instead of raising."""
    parsed = parse_meta_model({**model(name="library"), "bogus": 123})
    assert parsed.name == "library"


def test_parse_meta_model_registers_classes_and_enums():
    """Test that all classes and enums of the dict end up in the model."""
    parsed = parse_meta_model(
        model(
            enums=[{"name": "Color", "values": ["RED"]}],
            classes=[meta_class("Person"), meta_class("Address")],
        )
    )
    assert [c.name for c in parsed.classes] == ["Person", "Address"]
    assert [e.name for e in parsed.enums] == ["Color"]


def test_parse_meta_model_clears_caches_after_successful_parse():
    """Test that a successful parse leaves no state in the module caches."""
    parse_meta_model(
        model(enums=[{"name": "Color", "values": ["RED"]}], classes=[meta_class("Person")])
    )
    assert parser_module.CLASSES == {}
    assert parser_module.ENUMS == {}


def test_parse_meta_model_keeps_classes_and_enums_independent():
    """Test that two parses in a row do not accumulate elements."""
    parse_meta_model(model(classes=[meta_class("First")]))
    parsed = parse_meta_model(model(classes=[meta_class("Second")]))
    assert [c.name for c in parsed.classes] == ["Second"]


# ---------------------------------------------------------------------------
# Attributes
# ---------------------------------------------------------------------------


def test_parse_meta_model_builds_string_attribute():
    """Test that an attribute type given as a TypeOptions name is resolved."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Person",
                    attributes=[
                        {
                            "name": "name",
                            "attribute_type": "STRING",
                            "multiplicity": "[1]",
                        }
                    ],
                )
            ]
        )
    )
    attribute = get_attribute(get_class(parsed, "Person"), "name")
    assert attribute.attribute_type is TypeOptions.STRING
    assert attribute.multiplicity == Multiplicity(lower=1, upper=1)
    assert attribute.default_value is None


def test_parse_meta_model_accepts_attribute_type_by_value():
    """Test that an attribute type given as a TypeOptions value is resolved."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Person",
                    attributes=[
                        {"name": "age", "attribute_type": "int", "multiplicity": "[1]"}
                    ],
                )
            ]
        )
    )
    assert (
        get_attribute(get_class(parsed, "Person"), "age").attribute_type
        is TypeOptions.INT
    )


@pytest.mark.parametrize(
    "raw_type, expected",
    [
        ("INT", TypeOptions.INT),
        ("BOOL", TypeOptions.BOOL),
        ("STRING", TypeOptions.STRING),
        ("bool", TypeOptions.BOOL),
        ("str", TypeOptions.STRING),
    ],
)
def test_parse_meta_model_accepts_all_type_options(raw_type, expected):
    """Test that every TypeOptions name and value is accepted."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Thing",
                    attributes=[
                        {"name": "x", "attribute_type": raw_type, "multiplicity": "[1]"}
                    ],
                )
            ]
        )
    )
    assert get_attribute(get_class(parsed, "Thing"), "x").attribute_type is expected


def test_parse_meta_model_keeps_attribute_default_value():
    """Test that an optional default_value is carried over to the attribute."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Person",
                    attributes=[
                        {
                            "name": "age",
                            "attribute_type": "INT",
                            "multiplicity": "[0..1]",
                            "default_value": 42,
                        }
                    ],
                )
            ]
        )
    )
    assert get_attribute(get_class(parsed, "Person"), "age").default_value == 42


def test_parse_meta_model_rejects_unknown_attribute_type():
    """Test that an attribute type outside TypeOptions raises Error."""
    with pytest.raises(ValueError, match="FLOAT"):
        parse_meta_model(
            model(
                classes=[
                    meta_class(
                        "Thing",
                        attributes=[
                            {
                                "name": "x",
                                "attribute_type": "FLOAT",
                                "multiplicity": "[1]",
                            }
                        ],
                    )
                ]
            )
        )


def test_parse_meta_model_rejects_attribute_without_multiplicity():
    """Test that name, attribute_type and multiplicity are all required."""
    with pytest.raises(ValueError, match="multiplicity"):
        parse_meta_model(
            model(
                classes=[
                    meta_class(
                        "Thing", attributes=[{"name": "x", "attribute_type": "STRING"}]
                    )
                ]
            )
        )


def test_parse_meta_model_rejects_attribute_without_name():
    """Test that an attribute definition without a name raises."""
    with pytest.raises(ValueError, match="name"):
        parse_meta_model(
            model(
                classes=[
                    meta_class(
                        "Thing",
                        attributes=[{"attribute_type": "STRING", "multiplicity": "[1]"}],
                    )
                ]
            )
        )


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------




def test_parse_meta_model_builds_enum_from_literal_dicts():
    """Test that literal dicts keep their value and upper-case their name."""
    parsed = parse_meta_model(
        model(
            enums=[
                {
                    "name": "Status",
                    "values": [{"name": "active", "value": "ACTIVE_STATE"}],
                }
            ]
        )
    )
    assert get_enum(parsed, "Status").values == [
        MetaEnumLiteral(name="ACTIVE", value="ACTIVE_STATE")
    ]


def test_parse_meta_model_builds_enum_from_mixed_values():
    """Test that string and dict literals can be mixed in one enum."""
    parsed = parse_meta_model(
        model(
            enums=[
                {
                    "name": "Color",
                    "values": ["red", {"name": "blue", "value": "BLUE_V"}],
                }
            ]
        )
    )
    assert get_enum(parsed, "Color").values == [
        MetaEnumLiteral(name="RED", value="red"),
        MetaEnumLiteral(name="BLUE", value="BLUE_V"),
    ]


def test_parse_meta_model_rejects_enum_that_is_not_a_dict():
    """Test that an enum entry given as a bare string raises."""
    with pytest.raises(ValueError, match="Expected a dict"):
        parse_meta_model(model(enums=["Color"]))


def test_parse_meta_model_rejects_enum_literal_dict_without_value():
    """Test that a literal dict missing the value key raises."""
    with pytest.raises(KeyError, match="value"):
        parse_meta_model(model(enums=[{"name": "Color", "values": [{"name": "RED"}]}]))


def test_parse_meta_model_rejects_enum_without_literals():
    """Test that MetaModel.validate rejects an enum with no literals."""
    with pytest.raises(ValueError, match="no Literals"):
        parse_meta_model(model(enums=[{"name": "Color", "values": []}]))


def test_parse_meta_model_rejects_duplicate_enum_literals():
    """Test that MetaModel.validate rejects repeated literals."""
    with pytest.raises(ValueError, match="duplicate values"):
        parse_meta_model(model(enums=[{"name": "Color", "values": ["RED", "RED"]}]))


# ---------------------------------------------------------------------------
# Associations
# ---------------------------------------------------------------------------




def test_parse_meta_model_builds_composition_association():
    """Test that COMPOSITION (HAS A)is resolved to the matching AssociationOptions member."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Order",
                    associations=[
                        {
                            "name": "items",
                            "multiplicity": "[1..*]",
                            "association_type": "COMPOSITION",
                            "target": "LineItem",
                        }
                    ],
                ),
                meta_class("LineItem"),
            ]
        )
    )
    association = get_association(get_class(parsed, "Order"), "items")
    assert association.association_type is AssociationOptions.COMPOSITION
    assert association.multiplicity == Multiplicity(lower=1, upper=None)


def test_parse_meta_model_does_not_require_target_to_be_defined():
    """Test that targets are name-based, so definition order does not matter.

    An association to a class defined later in the list  (or not at all) still
    parses. Resolving it is the merger's job.
    """
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Person",
                    associations=[
                        {
                            "name": "ghost",
                            "multiplicity": "[1]",
                            "association_type": "REFERENCE",
                            "target": "Ghost",
                        }
                    ],
                )
            ]
        )
    )
    assert (
        get_association(get_class(parsed, "Person"), "ghost").association_target_name
        == "Ghost"
    )





@pytest.mark.parametrize(
    "missing_key", ["name", "multiplicity", "association_type", "target"]
)
def test_parse_meta_model_rejects_association_with_missing_keys(missing_key):
    """Test that every required association key is enforced."""
    association = {
        "name": "home",
        "multiplicity": "[1]",
        "association_type": "REFERENCE",
        "target": "Address",
    }
    del association[missing_key]
    with pytest.raises(ValueError, match=missing_key):
        parse_meta_model(
            model(classes=[meta_class("Person", associations=[association])])
        )


def test_parse_meta_model_leaves_unknown_association_type_unresolved():
    """Document that an unknown association_type yields None instead of raising Eroor.

    _test_enum_value returns None for a value it cannot match, and
    _build_association passes that straight into the OpenAssociation.
    """
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class(
                    "Person",
                    associations=[
                        {
                            "name": "home",
                            "multiplicity": "[1]",
                            "association_type": "AGGREGATION",
                            "target": "Address",
                        }
                    ],
                )
            ]
        )
    )
    assert get_association(get_class(parsed, "Person"), "home").association_type is None


# ---------------------------------------------------------------------------
# Inheritance
# ---------------------------------------------------------------------------


def test_parse_meta_model_wraps_single_inherits_string_in_list():
    """Test that inherits given as a string is normalised to a list."""
    parsed = parse_meta_model(
        model(classes=[meta_class("Child", inherits="Parent"), meta_class("Parent")])
    )
    assert get_class(parsed, "Child").inherits == ["Parent"]


def test_parse_meta_model_keeps_inherits_list():
    """Test that inherits given as a list is kept as is."""
    parsed = parse_meta_model(
        model(
            classes=[
                meta_class("Child", inherits=["ParentA", "ParentB"]),
                meta_class("ParentA"),
                meta_class("ParentB"),
            ]
        )
    )
    assert get_class(parsed, "Child").inherits == ["ParentA", "ParentB"]


def test_parse_meta_model_defaults_inherits_to_empty_list():
    """Test that a class without an inherits key gets an empty list."""
    parsed = parse_meta_model(model(classes=[meta_class("Person")]))
    assert get_class(parsed, "Person").inherits == []


def test_parse_meta_model_rejects_self_inheritance():
    """Test that MetaClass.validate rejects a class inheriting from itself."""
    with pytest.raises(ValueError, match="cannot inherit from itself"):
        parse_meta_model(model(classes=[meta_class("Person", inherits=["Person"])]))


# ---------------------------------------------------------------------------
# Malformed class definitions (Errors)
# ---------------------------------------------------------------------------


def test_parse_meta_model_rejects_class_without_associations_key():
    """Test that a class dict missing the associations key raises."""
    with pytest.raises(KeyError, match="associations"):
        parse_meta_model(model(classes=[{"name": "Person", "attributes": []}]))


def test_parse_meta_model_rejects_class_without_name_key():
    """Test that a class dict missing the name key raises."""
    with pytest.raises(KeyError, match="name"):
        parse_meta_model(model(classes=[{"attributes": [], "associations": []}]))




# ---------------------------------------------------------------------------
# _parse_multiplicity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("[0]", Multiplicity(lower=0, upper=0)),
        ("[1]", Multiplicity(lower=1, upper=1)),
        ("[3]", Multiplicity(lower=3, upper=3)),
        ("[0..1]", Multiplicity(lower=0, upper=1)),
        ("[2..5]", Multiplicity(lower=2, upper=5)),
        ("[1..*]", Multiplicity(lower=1, upper=None)),
        ("[0..*]", Multiplicity(lower=0, upper=None)),
        ("  [1..2]  ", Multiplicity(lower=1, upper=2)),
    ],
)
def test_parse_multiplicity_accepts_valid_formats(raw, expected):
    """Test the supported multiplicity spellings, including surrounding spaces."""
    assert _parse_multiplicity(raw) == expected


@pytest.mark.parametrize("raw", ["MANY", "1", "1..2", "[*]", "[]", "[..1]", "[1..x]"])
def test_parse_multiplicity_rejects_invalid_formats(raw):
    """Test that anything outside the '[lower(..upper)]' shape raises."""
    with pytest.raises(ValueError, match="Invalid multiplicity format"):
        _parse_multiplicity(raw)


def test_parse_multiplicity_rejects_upper_below_lower():
    """Test that an upper bound below the lower bound raises."""
    with pytest.raises(ValueError, match="less than"):
        _parse_multiplicity("[5..2]")


def test_parse_multiplicity_sets_is_list_for_unbounded_upper():
    """Test that '*' upper bounds are reported as lists by Multiplicity."""
    assert _parse_multiplicity("[1..*]").is_list is True
    assert _parse_multiplicity("[1]").is_list is False


def test_parse_multiplicity_sets_is_optional_for_zero_lower():
    """Test that a zero lower bound is reported as optional by Multiplicity."""
    assert _parse_multiplicity("[0..1]").is_optional is True
    assert _parse_multiplicity("[1..1]").is_optional is False


# ---------------------------------------------------------------------------
# _test_enum_value
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "enum, value, expected",
    [
        (TypeOptions, "STRING", TypeOptions.STRING),
        (TypeOptions, "str", TypeOptions.STRING),
        (AssociationOptions, "REFERENCE", AssociationOptions.REFERENCE),
        (AssociationOptions, "COMPOSITION", AssociationOptions.COMPOSITION),
    ],
)
def test_test_enum_value_resolves_names_and_values(enum, value, expected):
    """Test that a member is found by either its name or its value."""
    assert _test_enum_value(enum, value) is expected


def test_test_enum_value_returns_none_for_unknown_value():
    """Test that an unmatched value returns None rather than raising."""
    assert _test_enum_value(TypeOptions, "FLOAT") is None


# ---------------------------------------------------------------------------
# Enum building helpers
# ---------------------------------------------------------------------------


def test_build_enum_literal_from_string():
    """Test that a string literal becomes an upper-cased name with the raw value."""
    assert _build_enum_literal("red") == MetaEnumLiteral(name="RED", value="red")


def test_build_enum_literal_from_dict():
    """Test that a literal dict keeps its value and upper-cases its name."""
    assert _build_enum_literal({"name": "red", "value": "FF0000"}) == MetaEnumLiteral(
        name="RED", value="FF0000"
    )


def test_build_enum_literal_rejects_other_types():
    """Test that a literal that is neither a string nor a dict raises."""
    with pytest.raises(ValueError, match="Invalid enum value"):
        _build_enum_literal(123)


def test_find_in_meta_enums_returns_registered_enum():
    """Test that a built enum can be looked up by name."""
    built = _build_enum("Color", ["RED"])
    assert _find_in_meta_enums("Color") is built


def test_find_in_meta_enums_returns_none_for_unknown_name():
    """Test that an unknown enum name looks up to None."""
    assert _find_in_meta_enums("Missing") is None


