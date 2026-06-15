from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import pytest

from src.metameta.m_m_m_classes import (
    MetaModel,
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    Attribute,
    Association,
    TypeOptions,
    MultiplicityOptions
)

from src.metamodel.codegenerator.codegenerator import (
    generate_meta_model_api,
)
from src.metamodel.codegenerator.formatter import Formatter


@pytest.fixture
def simple_meta_enum():
    """Create a simple MetaEnum for testing."""
    enum = MetaEnum(name="Status")
    enum.values = [
        MetaEnumLiteral(name="ACTIVE", value="active"),
        MetaEnumLiteral(name="INACTIVE", value="inactive"),
    ]
    return enum


@pytest.fixture
def simple_meta_class():
    """Create a simple MetaClass with attributes."""
    cls = MetaClass(name="Person")
    cls.attributes = [
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
            default_value=None,
        ),
    ]
    cls.associations = []
    return cls


@pytest.fixture
def meta_model_with_associations(simple_meta_class, simple_meta_enum):
    """Create a MetaModel with classes and associations."""
    person_cls = simple_meta_class

    address_cls = MetaClass(name="Address")
    address_cls.attributes = [
        Attribute(
            name="street",
            attribute_type=TypeOptions.STRING,
            multiplicity=MultiplicityOptions.ONE,
            default_value=None,
        ),
    ]
    address_cls.associations = []

    # Add association from Person to Address
    association = Association(
        name="address",
        association_type="reference",
        association_target=address_cls,
        multiplicity=MultiplicityOptions.ZERO_OR_ONE,
    )
    person_cls.associations = [association]

    meta_model = MetaModel(name="TestModel")
    meta_model.classes = [person_cls, address_cls]
    meta_model.enums = [simple_meta_enum]

    return meta_model


@pytest.fixture
def mock_formatter():
    """Create a mock formatter."""
    formatter = Mock(spec=Formatter)
    formatter.format_descriptors = Mock()
    return formatter


class TestCodeGeneratorIntegration:
    """Integration tests for the code generation workflow."""

    def test_generate_meta_model_api_returns_dict_with_keys(
        self, meta_model_with_associations, mock_formatter
    ):
        """Test that generate_meta_model_api returns expected dictionary keys."""
        with TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            # Create dummy template files
            (templates_dir / "dataclass_template.py.j2").write_text(
                "# Dataclass Template\n{{ classes }}"
            )
            (templates_dir / "enum_template.py.j2").write_text(
                "# Enum Template\n{{ enums }}"
            )

            api_config = {"naming_convention": "snake_case"}

            result = generate_meta_model_api(
                meta_model=meta_model_with_associations,
                api_config=api_config,
                formatter=mock_formatter,
                templates_dir=templates_dir,
            )

            assert isinstance(result, dict)
            assert "dataclass_code" in result
            assert "enum_code" in result
            assert isinstance(result["dataclass_code"], str)
            assert isinstance(result["enum_code"], str)

    def test_generate_meta_model_api_calls_formatter(
        self, meta_model_with_associations, mock_formatter
    ):
        """Test that generate_meta_model_api invokes the formatter."""
        with TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            (templates_dir / "dataclass_template.py.j2").write_text("")
            (templates_dir / "enum_template.py.j2").write_text("")

            api_config = {}

            generate_meta_model_api(
                meta_model=meta_model_with_associations,
                api_config=api_config,
                formatter=mock_formatter,
                templates_dir=templates_dir,
            )

            mock_formatter.format_descriptors.assert_called_once()

    def test_generate_meta_model_api_with_api_config(
        self, simple_meta_class, mock_formatter
    ):
        """Test that api_config is passed to the rendering context."""
        meta_model = MetaModel(name="TestModel")
        meta_model.classes = [simple_meta_class]
        meta_model.enums = []

        with TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            (templates_dir / "dataclass_template.py.j2").write_text(
                "{{ api_config.naming_convention }}"
            )
            (templates_dir / "enum_template.py.j2").write_text("")

            api_config = {"naming_convention": "pascal_case"}

            result = generate_meta_model_api(
                meta_model=meta_model,
                api_config=api_config,
                formatter=mock_formatter,
                templates_dir=templates_dir,
            )

            assert "pascal_case" in result["dataclass_code"]
