from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.metameta.m_m_m_classes import (
    MetaModel,
    MetaClass,
    MetaEnum,
    MetaEnumLiteral,
    Attribute,
    Association,
    TypeOptions,
    Multiplicity
)

from src.metamodel.codegenerator.codegenerator import (
    generate_meta_model_api
)
from src.metamodel.codegenerator.formatter import get_formatter


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
            multiplicity=Multiplicity(1, 1),
            default_value=None,
        ),
        Attribute(
            name="age",
            attribute_type=TypeOptions.INT,
            multiplicity=Multiplicity(1, 1),
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
            multiplicity=Multiplicity(1, 1),
            default_value=None,
        ),
    ]
    address_cls.associations = []

    # Add association from Person to Address
    association = Association(
        name="address",
        association_type="reference",
        association_target=address_cls,
        multiplicity=Multiplicity(0, 1),
    )
    person_cls.associations = [association]

    meta_model = MetaModel(name="TestModel")
    meta_model.classes = [person_cls, address_cls]
    meta_model.enums = [simple_meta_enum]

    return meta_model


class TestCodeGeneratorIntegration:
    """Integration tests for the code generation workflow."""

    def test_generate_meta_model_api_returns_dict_with_keys(
        self, meta_model_with_associations
    ):
        """Test that generate_meta_model_api returns expected dictionary keys."""
        with TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            # Create dummy template files
            (templates_dir / "class_template.py.j2").write_text(
                "# Class Template\n{{ classes }}"
            )
            (templates_dir / "enum_template.py.j2").write_text(
                "# Enum Template\n{{ enums }}"
            )

            api_config = {"NamingConvention": "snake_case"}
            formatter = get_formatter(api_config["NamingConvention"])

            result = generate_meta_model_api(
                meta_model=meta_model_with_associations,
                api_config=api_config,
                formatter=formatter,
                templates_dir=templates_dir,
            )

            assert isinstance(result, dict)
            assert "class_code" in result
            assert "enum_code" in result
            assert isinstance(result["class_code"], str)
            assert isinstance(result["enum_code"], str)
