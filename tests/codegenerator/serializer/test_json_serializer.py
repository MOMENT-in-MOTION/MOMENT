import json
import pytest

from src.metamodel.codegenerator.serializer.json_serializer import JsonSerializer
from tests.codegenerator.utils.setup_desciptors import make_class, make_enum, make_field


class TestJsonSerializer:
    """Tests for the json serializer."""

    @pytest.fixture
    def visitor(self):
        return JsonSerializer()

    def test_render_produces_valid_json(self, visitor):
        result = visitor.render()
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_visit_class_appears_in_output(self, visitor):
        cls = make_class("MyClass")
        visitor.visit_class(cls)
        parsed = json.loads(visitor.render())
        assert any(c["class_name"] == "MyClass" for c in parsed["classes"])

    def test_visit_class_includes_fields(self, visitor):
        field = make_field("my_field", base_type="str")
        cls = make_class("MyClass", fields=[field])
        visitor.visit_class(cls)
        parsed = json.loads(visitor.render())
        fields = parsed["classes"][0]["fields"]
        assert len(fields) == 1
        assert fields[0]["field_name"] == "my_field"
        assert fields[0]["base_type"] == "str"

    def test_visit_enum_appears_in_output(self, visitor):
        enum = make_enum("MyEnum", options={"KEY": "VALUE"})
        visitor.visit_enum(enum)
        parsed = json.loads(visitor.render())
        assert any(e["enum_name"] == "MyEnum" for e in parsed["enums"])

    def test_visit_enum_includes_options(self, visitor):
        enum = make_enum("MyEnum", options={"KEY": "VALUE"})
        visitor.visit_enum(enum)
        parsed = json.loads(visitor.render())
        assert parsed["enums"][0]["options"] == {"KEY": "VALUE"}

    def test_append_api_config_stored_in_output(self, visitor):
        visitor.append_api_config({"package": "com.example"})
        parsed = json.loads(visitor.render())
        assert parsed["api_config"] == {"package": "com.example"}

    def test_multiple_classes_all_appear(self, visitor):
        visitor.visit_class(make_class("ClassA"))
        visitor.visit_class(make_class("ClassB"))
        parsed = json.loads(visitor.render())
        names = [c["class_name"] for c in parsed["classes"]]
        assert "ClassA" in names
        assert "ClassB" in names

    def test_field_extension_is_json(self, visitor):
        assert visitor.file_extension == "json"

    def test_optional_field_attributes_present(self, visitor):
        field = make_field(
            "my_field",
            association_kind="aggregation",
            default="42",
        )
        cls = make_class("MyClass", fields=[field])
        visitor.visit_class(cls)
        parsed = json.loads(visitor.render())
        f = parsed["classes"][0]["fields"][0]
        assert f["association_kind"] == "aggregation"
        assert f["default"] == "42"
