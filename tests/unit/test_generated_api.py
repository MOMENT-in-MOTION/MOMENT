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
from src.metamodel.merger import UnreachableClassError, merge_meta_models
from src.metamodel.parser.meta_model_parser import parse_meta_model
from src.shared.load_json_as_dict import load_json_as_dict
from src.shared.structure import structure_data
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
    "AllowUnreachableClasses": "false",
    "RelativeImports": "true",
    "Inheritance": "native",
}


def generate_api_code(meta_model, api_config, formatter, tmp_path):
    """Generate API code using the current generator signature."""
    return generate_meta_model_api(
        meta_model=meta_model,
        api_config=api_config,
        formatter=formatter,
        templates_dir=TEMPLATES_DIR,
        output_path=tmp_path,
    )


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
    result = generate_api_code(simple_model, default_config, formatter, tmp_path)
    return result["class_code"]


class TestCodeGeneration:
    """Core checks for code generation behavior."""

    def test_generate_meta_model_api_returns_expected_structure(
        self, simple_model, default_config, formatter, tmp_path
    ):
        """Verify generated API code returns dict with class_code and enum_code keys."""
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)

        assert isinstance(result, dict)
        assert {"class_code", "enum_code"}.issubset(set(result))
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
    def test_generate_getters(
        self,
        simple_model,
        default_config,
        getter_enabled,
        expected_names,
        tmp_path,
    ):
        """Verify getter methods are generated only when enabled."""
        default_config["GenerateGetters"] = getter_enabled

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        for getter_name in ("get_name", "get_age"):
            assert (getter_name in code) is (getter_name in expected_names)

    @pytest.mark.parametrize(
        "setter_enabled,expected_names",
        [
            ("true", ["set_name", "set_age"]),
            ("false", []),
        ],
    )
    def test_generate_setters(
        self,
        simple_model,
        default_config,
        setter_enabled,
        expected_names,
        tmp_path,
    ):
        """Verify setter methods are generated only when enabled."""
        default_config["GenerateSetters"] = setter_enabled

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        for setter_name in ("set_name", "set_age"):
            assert (setter_name in code) is (setter_name in expected_names)

    @pytest.mark.parametrize(
        "setter_enabled,getter_enabled,expected_names",
        [
            ("true", "true", ["set_name", "set_age", "get_name", "get_age"]),
            ("true", "false", ["set_name", "set_age"]),
            ("false", "true", ["get_name", "get_age"]),
            ("false", "false", []),
        ],
    )
    def test_getters_and_setters_can_be_independently_disabled(
        self,
        simple_model,
        default_config,
        setter_enabled,
        getter_enabled,
        expected_names,
        tmp_path,
    ):
        """Verify getter and setter generation can be toggled independently."""
        default_config["GenerateSetters"] = setter_enabled
        default_config["GenerateGetters"] = getter_enabled

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        for name in ("set_name", "set_age", "get_name", "get_age"):
            assert (name in code) is (name in expected_names)

    @pytest.mark.parametrize(
        "relative_imports_enabled,expected_import_statement",
        [
            ("true", "from .enum_code import *"),
            ("false", "from enum_code import *"),
        ],
    )
    def test_relative_imports(
        self,
        simple_model,
        default_config,
        relative_imports_enabled,
        expected_import_statement,
        tmp_path,
    ):
        """Verify import statements use relative or absolute paths based on config."""
        default_config["RelativeImports"] = relative_imports_enabled

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert expected_import_statement in code

    def test_allow_unreachable_classes_setting(self):
        """Verify unreachable classes are handled correctly based on settings."""
        metamodel_path = (
            PROJECT_ROOT
            / "tests"
            / "unit"
            / "snapshots"
            / "test_jsons"
            / "snsh_merge_json.json"
        )
        meta_model_dict = structure_data(load_json_as_dict(metamodel_path))
        meta_model = parse_meta_model(meta_model_dict=meta_model_dict)

        with pytest.raises(UnreachableClassError):
            merge_meta_models(
                meta_model, metamodel_path, allow_unreachable_classes=False
            )

        meta_model = parse_meta_model(meta_model_dict=meta_model_dict)
        merged_model = merge_meta_models(
            meta_model,
            metamodel_path,
            allow_unreachable_classes=True,
        )

        assert merged_model is meta_model
        assert any(cls.name == "MetaModelDummy" for cls in merged_model.classes)

    @pytest.mark.parametrize(
        "naming,field_name,expected",
        [
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
        """Verify field names are formatted according to naming convention."""
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

        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert expected in code

    def test_unknown_format_style_raises_value_error(self):
        """Verify ValueError is raised for unsupported naming conventions."""
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

    def test_strict_privacy_enabled_uses_private_fields(
        self, simple_model, default_config, tmp_path
    ):
        """Verify private fields with single underscore prefix when strict privacy enabled."""
        default_config["StrictPrivacy"] = "true"
        default_config["UseDoubleUnderscore"] = "false"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "_name: str" in code
        assert "_age: int" in code
        assert "self._name = name" in code

    def test_double_underscore_privacy_variant(
        self, simple_model, default_config, tmp_path
    ):
        """Verify double underscore prefix for name mangling when option enabled."""
        default_config["StrictPrivacy"] = "true"
        default_config["UseDoubleUnderscore"] = "true"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "__name: str" in code
        assert "self.__name = name" in code

    def test_without_strict_privacy_fields_are_public(
        self, simple_model, default_config, tmp_path
    ):
        """Verify fields are public without privacy modifiers when strict privacy disabled."""
        default_config["StrictPrivacy"] = "false"
        default_config["UseDoubleUnderscore"] = "false"

        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "name: str" in code
        assert "age: int" in code
        assert "self.name = name" in code


class TestConstructor:
    """Constructor generation tests."""

    def test_constructor_generated(self, simple_model, default_config, tmp_path):
        """Verify __init__ method is generated when constructor generation enabled."""
        default_config["GenerateConstructors"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "def __init__(" in code
        assert "self._name = name" in code

    def test_constructor_disabled(self, simple_model, default_config, tmp_path):
        """Verify __init__ method is not generated when constructor generation disabled."""
        default_config["GenerateConstructors"] = "false"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "def __init__(" not in code


class TestSetter:
    """Setter generation and safety checks."""

    def test_setter_exists(self, simple_model, default_config, tmp_path):
        """Verify setter methods are present in generated code."""
        default_config["GenerateSetters"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "def set_name" in code
        assert "def set_age" in code

    def test_setter_not_generated(self, simple_model, default_config, tmp_path):
        """Verify setter methods are not generated when disabled."""
        default_config["GenerateSetters"] = "false"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "def set_name" not in code
        assert "def set_age" not in code

    def test_explicit_type_safety_is_rendered(
        self, simple_model, default_config, tmp_path
    ):
        """Verify type checking with TypeError is included when explicit type safety enabled."""
        default_config["ExplicitTypeSafety"] = "true"
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "TypeError" in code
        assert "Expected type str" in code or "Expected type int" in code


class TestAssociations:
    """Association and reference generation tests."""

    def test_reference_generation(self, simple_model, default_config, tmp_path):
        """Verify reference associations are properly generated in code."""
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "status: Status" in code
        assert "association_kind" not in code or "reference" in code

    def test_association_field_uses_target_name_as_type(
        self, simple_model, default_config, tmp_path
    ):
        """This is the stable contract: association targets become type hints."""
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["class_code"]

        assert "Status" in code
        assert "status" in code


class TestEnums:
    """Enum generation tests."""

    def test_enum_generation(self, simple_model, default_config, tmp_path):
        """Verify enum class with literals is generated correctly."""
        formatter = get_formatter(default_config["NamingConvention"])
        result = generate_api_code(simple_model, default_config, formatter, tmp_path)
        code = result["enum_code"]

        assert "class Status(Enum):" in code
        assert 'ACTIVE = "ACTIVE"' in code
        assert 'INACTIVE = "INACTIVE"' in code


class TestSnapshots:
    """Snapshot checks for generated code from the supported JSON variants."""

    @pytest.mark.parametrize(
        "json_name",
        [
            "snsh_merge_json.json",
            "snsh_variance_base.json",
            "snsh_variance_imported.json",
            "snsh_variance_inheritance.json",
        ],
    )
    def test_complete_model_snapshot(self, default_config, tmp_path, json_name):
        """Verify generated code matches expected snapshots for various model types."""
        metamodel_path = (
            PROJECT_ROOT / "tests" / "unit" / "snapshots" / "test_jsons" / json_name
        )
        assert metamodel_path.exists(), f"Missing snapshot input: {metamodel_path}"

        meta_model_dict = structure_data(load_json_as_dict(metamodel_path))
        meta_model = parse_meta_model(meta_model_dict=meta_model_dict)

        if json_name == "snsh_merge_json.json":
            merge_meta_models(
                meta_model, metamodel_path, allow_unreachable_classes=True
            )

        generated = generate_api_code(
            meta_model,
            default_config,
            get_formatter(default_config["NamingConvention"]),
            tmp_path,
        )

        class_snapshot = (
            PROJECT_ROOT
            / "tests"
            / "unit"
            / "snapshots"
            / f"{metamodel_path.stem}_class_code.py"
        ).read_text(encoding="utf-8")
        enum_snapshot = (
            PROJECT_ROOT
            / "tests"
            / "unit"
            / "snapshots"
            / f"{metamodel_path.stem}_enum_code.py"
        ).read_text(encoding="utf-8")

        assert generated["class_code"] == class_snapshot
        assert generated["enum_code"] == enum_snapshot
