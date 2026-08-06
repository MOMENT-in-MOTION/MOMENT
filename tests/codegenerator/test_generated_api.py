from pathlib import Path

import pytest
from src.metamodel.merger import merge_meta_models

from src.metameta.m_m_m_classes import (
    MetaModel,
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    Attribute,
    TypeOptions,
    Association,
    MultiplicityOptions,
    TypeOptions,
    MultiplicityOptions,
    AssociationOptions
)

from src.metamodel.codegenerator.codegenerator import (
    generate_meta_model_api,
)

from src.metamodel.codegenerator.formatter import get_formatter


DEFAULT_CONFIG = {
    "GenerateGetters": True,
    "GenerateSetters": True,
    "GenerateConstructors": True,
    "StrictPrivacy": True,
    "UseDoubleUnderscore": False,
    "ExplicitTypeSafety": True,
    "NamingConvention": "snake_case",
}


@pytest.fixture
def simple_model():
    """Simple MetaModel fixture for testing."""
    meta_enum = MetaEnum(
        name="Status",
        values = [
            MetaEnumLiteral(name="ACTIVE", value="active"),
            MetaEnumLiteral(name="INACTIVE", value="inactive"),
        ]
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
            name= "Class_MetaClassDummy_1",
            multiplicity = MultiplicityOptions.ONE,
            association_type = AssociationOptions.COMPOSITION,
            association_target = meta_enum
        )
    ]

    model = MetaModel(name="SimpleModel")
    model.classes = [person]
    model.enums = [meta_enum]

    return model


@pytest.fixture
def default_config():
    """Fixture that returns a copy of the default configuration."""
    return DEFAULT_CONFIG.copy()


@pytest.fixture
def formatter(default_config):
    """Create a formatter based on the default configuration."""

    return get_formatter(default_config["NamingConvention"])


@pytest.fixture
def generated_code(simple_model, default_config, formatter, tmp_path):
    """Fixture that creates generated code for the simple model using the default configuration."""

    result = generate_meta_model_api(
        meta_model=simple_model,
        api_config=default_config,
        formatter=formatter,
        templates_dir=tmp_path,
    )

    return result["class_code"]




class TestCodeGeneration:

    @pytest.mark.parametrize(
        "getter_enabled,expected",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_generate_getters_and_setters(
        self,
        simple_model,
        default_config,
        getter_enabled,
        expected,
        tmp_path,
    ):
        """ Tests the creation of getters and setters.
        """

        default_config["GenerateGetters"] = getter_enabled

        formatter = get_formatter(default_config["NamingConvention"])

        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=tmp_path,
        )

        code = result["class_code"]

        if expected:
            assert "get_name" in code
            assert "set_name" in code
            assert "get_age" in code
            assert "set_age" in code

        else:
            assert "get_name" not in code
            assert "set_name" not in code
            assert "get_age" not in code
            assert "set_age" not in code

    @pytest.mark.parametrize(
        "naming",
        [
            "snake_case",
            "camelCase",
            "PascalCase",
        ],
    )
    def test_naming_convention(
        self,
        simple_model,
        default_config,
        naming,
        tmp_path,
    ):
        """
        """

        default_config["NamingConvention"] = naming

        formatter = get_formatter(naming)

        result = generate_meta_model_api(
            meta_model=simple_model,
            api_config=default_config,
            formatter=formatter,
            templates_dir=tmp_path,
        )

        code = result["class_code"]



        assert isinstance(code, str)



class TestPrivacy:
    """
    """

    def test_strict_privacy_enabled(self):
        """
        Prüft:

            self.__name

        oder

            self._name

        je nach Generator.
        """
        pass


class TestConstructor:
    """
    Tests zur Constructor-Erzeugung.
    """

    def test_constructor_generated(self):
        pass

    def test_constructor_disabled(self):
        pass


class TestSetter:
    """
    Tests zur Setter-Erzeugung.
    """

    def test_setter_exists(self):
        pass

    def test_setter_not_generated(self):
        pass


class TestAssociations:
    """
    Tests für Referenzen und Assoziationen.
    """

    def test_reference_generation(self):
        pass


class TestEnums:
    """
    Tests für Enum-Erzeugung.
    """

    def test_enum_generation(self):
        pass




class TestSnapshots:

    def test_complete_model_snapshot(self, formatter, default_config, tmp_path):
        """
        Tests the generation of a complete model against a snapshot.
        """

        metamodel_dir = Path()

        model = merge_meta_models(path=metamodel_dir, config=default_config)
        meta_model = parse_meta_model(meta_model_dict=model)

        generated = result = generate_meta_model_api(
                meta_model=simple_model,
                api_config=default_config,
                formatter=formatter,
                templates_dir=tmp_path,
            )

        expected_class_code = Path(
            "tests/snapshots/person_model.py" #TODO: Create Snapshot file and specify the path to the snapshot file.
        ).read_text()

        assert generated == expected_class_code

