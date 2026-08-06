import pytest

from src.metamodel.codegenerator.formatter.camel_case_formatter import CamelCaseFormatter
from tests.codegenerator.utils.setup_desciptors import make_class, make_enum, make_field


class TestCamelCaseFormatter:
    """Tests for the camel case formatter."""

    @pytest.fixture
    def formatter(self):
        return CamelCaseFormatter()

    def test_visit_class_converts_name_to_pascal_case(self, formatter):
        cls = make_class("my_class")
        formatter.visit_class(cls)
        assert cls.class_name == "MyClass"

    def test_visit_field_converts_name_to_camel_case(self, formatter):
        field = make_field("my_field_name")
        cls = make_class(fields=[field])
        formatter.visit_class(cls)
        assert field.field_name == "myFieldName"

    def test_visit_class_ignores_primitive_base_types(self, formatter):
        field = make_field(base_type="int")
        cls = make_class(fields=[field])
        formatter.visit_class(cls)
        assert field.base_type == "int"

    def test_visit_enum_converts_options_to_upper_snake_case(self, formatter):
        enum = make_enum(options={"optionOne": "valueOne"})
        formatter.visit_enum(enum)
        assert "OPTION_ONE" in enum.options
