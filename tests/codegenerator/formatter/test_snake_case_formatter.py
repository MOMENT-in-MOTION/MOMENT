import pytest

from src.metamodel.codegenerator.formatter.snake_case_formatter import SnakeCaseFormatter
from tests.codegenerator.utils.setup_desciptors import make_class, make_enum, make_field


class TestSnakeCaseFormatter:
    """Tests for the snake case formatter."""

    @pytest.fixture
    def formatter(self):
        return SnakeCaseFormatter()

    def test_visit_class_converts_name_to_pascal_case(self, formatter):
        cls = make_class("my_class")
        formatter.visit_class(cls)
        assert cls.class_name == "MyClass"

    def test_visit_class_converts_field_names_to_snake_case(self, formatter):
        field = make_field("myFieldName")
        cls = make_class(fields=[field])
        formatter.visit_class(cls)
        assert field.field_name == "my_field_name"

    def test_visit_class_converts_base_type_to_pascal_case(self, formatter):
        field = make_field(base_type="some_type")
        cls = make_class(fields=[field])
        formatter.visit_class(cls)
        assert field.base_type == "SomeType"

    def test_visit_class_ignores_primitive_base_types(self, formatter):
        """Types in TypeOptions (e.g. 'str', 'int') must not be PascalCased."""
        field = make_field(base_type="str")
        cls = make_class(fields=[field])
        formatter.visit_class(cls)
        assert field.base_type == "str"

    def test_visit_class_handles_multiple_fields(self, formatter):
        fields = [make_field("field_one"), make_field("field_two")]
        cls = make_class(fields=fields)
        formatter.visit_class(cls)
        assert fields[0].field_name == "field_one"
        assert fields[1].field_name == "field_two"

    def test_visit_class_handles_no_fields(self, formatter):
        cls = make_class(fields=[])
        formatter.visit_class(cls)
        assert cls.class_name == "MyClass"

    def test_visit_enum_converts_name_to_pascal_case(self, formatter):
        enum = make_enum("my_enum")
        formatter.visit_enum(enum)
        assert enum.enum_name == "MyEnum"

    def test_visit_enum_converts_options_to_upper_snake_case(self, formatter):
        enum = make_enum(options={"optionOne": "valueOne"})
        formatter.visit_enum(enum)
        assert "OPTION_ONE" in enum.options
        assert enum.options["OPTION_ONE"] == "VALUE_ONE"
