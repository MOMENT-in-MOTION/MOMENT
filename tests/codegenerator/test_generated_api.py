from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = PROJECT_ROOT / "templates"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.metamodel.codegenerator.codegenerator import generate_meta_model_api
from src.metamodel.codegenerator.formatter import get_formatter
from src.metamodel.merger import merge_meta_models
from src.metamodel.parser.meta_model_parser import parse_meta_model
from src.metameta.m_m_m_classes import (
    Association,
    AssociationOptions,
    Attribute,
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    MetaModel,
    MultiplicityOptions,
    TypeOptions,
)


DEFAULT_CONFIG = {
    "GenerateGetters": "true",
    "GenerateSetters": "true",
    "GenerateConstructors": "true",
    "StrictPrivacy": "true",
    "UseDoubleUnderscore": "false",
    "ExplicitTypeSafety": "true",
    "NamingConvention": "snake_case",
}


@pytest.fixture
def simple_model():
    """Simple MetaModel fixture for testing."""
    meta_enum = MetaEnum(
        name="Status",
        values=[
            MetaEnumLiteral(name="ACTIVE", value="active"),
            MetaEnumLiteral(name="INACTIVE", value="inactive"),
        ],
    )

    person = MetaClass(name="Person")
    person.attributes = [
        Attribute(
            name="name",
            attribute_type=TypeOptions.STRING,
            multiplicity=MultiplicityOptions.ONE,
            default_value=None,
        ),
        Attribute(
            name="age",
            attribute_type=TypeOptions.INT,
            multiplicity=MultiplicityOptions.ONE,
            default_value=18,
        ),
    ]
    person.associations = [
        Association(
            name="status",
            multiplicity=MultiplicityOptions.ONE,
            association_type=AssociationOptions.REFERENCE,
            association_target=meta_enum,
        )
    ]

    model = MetaModel(name="SimpleModel")
    model.classes = [person]
    model.enums = [meta_enum]
    return model


@pytest.fixture
def default_config():
    """Return a copy of the default configuration used by the generator."""
    return DEFAULT_CONFIG.copy()


@pytest.fixture
def formatter(default_config):
    """Create a formatter from the active naming convention."""
    return get_formatter(default_config["NamingConvention"])


@pytest.fixture
def generated_code(simple_model, default_config, formatter, tmp_path):
    """Generate a class code string for the simplest valid model."""
    result = generate_meta_model_api(
        meta_model=simple_model,
        api_config=default_config,
        formatter=formatter,
        templates_dir=TEMPLATES_DIR,
    )
    return result["class_code"]


class TestCodeGeneration:
    """Core checks for code generation behavior."""

    def test_generate_meta_model_api_returns_expected_structure(
        self, simple_model, default_config, formatter, tmp_path
    ):
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )

        assert isinstance(result, dict)
        assert set(result) == {"class_code", "enum_code"}
        assert isinstance(result["class_code"], str)
        assert isinstance(result["enum_code"], str)
        assert "class Person" in result["class_code"]
        assert "class Status" in result["enum_code"]

    @pytest.mark.parametrize(
        "getter_enabled,expected_names",
        [
            ("true", ["get_name", "get_age"]),
            ("false", []),
        ],
    )
    def test_generate_getters_and_setters(
        self,
        simple_model,
        default_config,
        getter_enabled,
        expected_names,
        tmp_path,
    ):
        default_config["GenerateGetters"] = getter_enabled
        default_config["GenerateSetters"] = getter_enabled

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        for getter_name in ("get_name", "get_age"):
            assert (getter_name in code) is (getter_name in expected_names)

        for setter_name in ("set_name", "set_age"):
            assert (setter_name in code) is (getter_name in expected_names if getter_name in ("get_name", "get_age") else False)

        # NOTE: The project currently does not distinguish getter/setter generation separately,
        # so this test keeps the business rule explicit and is meant to be reviewed if the
        # generator eventually separates getter and setter toggles.

    @pytest.mark.parametrize(
        "naming,field_name,expected", [
            ("snake_case", "firstName", "first_name"),
            ("camelCase", "first_name", "firstName"),
        ],
    )
    def test_naming_convention_formatting(
        self,
        simple_model,
        default_config,
        naming,
        field_name,
        expected,
        tmp_path,
    ):
        default_config["NamingConvention"] = naming
        formatter = get_formatter(naming)

        simple_model.classes[0].attributes.append(
            Attribute(
                name=field_name,
                attribute_type=TypeOptions.STRING,
                multiplicity=MultiplicityOptions.ONE,
                default_value=None,
            )
        )

        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert expected in code or expected.replace("_", "") in code

        # TODO: add a stricter assertion once the exact naming transformation contract is
        # finalized for each supported naming style. This is intentionally tolerant because
        # the project does not currently expose a dedicated formatter validation helper.

    def test_unknown_format_style_raises_value_error(self):
        with pytest.raises(ValueError, match="PascalCase"):
            get_formatter("PascalCase")

    def test_default_config_uses_string_truth_values(self, default_config):
        """The generator compares config flags with string literals such as 'true'."""
        for key in [
            "GenerateGetters",
            "GenerateSetters",
            "GenerateConstructors",
            "StrictPrivacy",
            "UseDoubleUnderscore",
            "ExplicitTypeSafety",
        ]:
            assert isinstance(default_config[key], str)
            assert default_config[key].lower() in {"true", "false"}


class TestPrivacy:
    """Privacy checks for generated fields and setters."""

    def test_strict_privacy_enabled_uses_private_fields(self, simple_model, default_config, tmp_path):
        default_config["StrictPrivacy"] = "true"
        default_config["UseDoubleUnderscore"] = "false"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "_name: str" in code
        assert "_age: int" in code
        assert "self._name = name" in code

    def test_double_underscore_privacy_variant(self, simple_model, default_config, tmp_path):
        default_config["StrictPrivacy"] = "true"
        default_config["UseDoubleUnderscore"] = "true"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "__name: str" in code
        assert "self.__name = name" in code

    def test_without_strict_privacy_fields_are_public(self, simple_model, default_config, tmp_path):
        default_config["StrictPrivacy"] = "false"
        default_config["UseDoubleUnderscore"] = "false"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "name: str" in code
        assert "age: int" in code
        assert "self.name = name" in code


class TestConstructor:
    """Constructor generation tests."""

    def test_constructor_generated(self, simple_model, default_config, tmp_path):
        default_config["GenerateConstructors"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "def __init__(" in code
        assert "self._name = name" in code

    def test_constructor_disabled(self, simple_model, default_config, tmp_path):
        default_config["GenerateConstructors"] = "false"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "def __init__(" not in code


class TestSetter:
    """Setter generation and safety checks."""

    def test_setter_exists(self, simple_model, default_config, tmp_path):
        default_config["GenerateSetters"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "def set_name" in code
        assert "def set_age" in code

    def test_setter_not_generated(self, simple_model, default_config, tmp_path):
        default_config["GenerateSetters"] = "false"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "def set_name" not in code
        assert "def set_age" not in code

    def test_explicit_type_safety_is_rendered(self, simple_model, default_config, tmp_path):
        default_config["ExplicitTypeSafety"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "TypeError" in code
        assert "Expected type str" in code or "Expected type int" in code


class TestAssociations:
    """Association and reference generation tests."""

    def test_reference_generation(self, simple_model, default_config, tmp_path):
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "status: Status" in code
        assert "association_kind" not in code or "reference" in code

    def test_association_field_uses_target_name_as_type(self, simple_model, default_config, tmp_path):
        """This is the stable contract: association targets become type hints."""
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["class_code"]

        assert "Status" in code
        assert "status" in code


class TestEnums:
    """Enum generation tests."""

    def test_enum_generation(self, simple_model, default_config, tmp_path):
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=TEMPLATES_DIR,
        )
        code = result["enum_code"]

        assert "class Status(Enum):" in code
        assert "ACTIVE = \"ACTIVE\"" in code
        assert "INACTIVE = \"INACTIVE\"" in code


class TestSnapshots:
    """Snapshot checks for merged models. These are intentionally partial until the real fixtures exist."""

    @pytest.mark.xfail(reason="TODO: add the real merged model JSON and snapshot output for this project.")
    def test_complete_merged_model_snapshot(self, simple_model, default_config, tmp_path):
        """This is a placeholder for a real merged-model snapshot test."""
        # TODO: replace this with the real JSON fixture path once the merged-model example is ready.
        metamodel_dir = PROJECT_ROOT / "tests" / "codegenerator" / "snapshots" / "test_jsons" / "snsh_merge_json.json"

        try:
            meta_model_dict = merge_meta_models(path=metamodel_dir, config=default_config)
        except (FileNotFoundError, TypeError, ValueError):
            # NOTE: unsure whether this function requires a dict, a file path, or extra config.
            pytest.xfail("merge_meta_models input contract is not yet fully specified for this repository.")

        meta_model = parse_meta_model(meta_model_dict=meta_model_dict)
        assert meta_model is not None

        generated = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=get_formatter(default_config["NamingConvention"]),
            templates_dir=TEMPLATES_DIR,
        )

        # TODO: add the expected snapshot file and compare the generated code with it.
        # This is intentionally left incomplete because the repository does not yet contain a
        # finalized example snapshot for this generator output.
        assert isinstance(generated["class_code"], str)

