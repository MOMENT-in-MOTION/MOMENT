from xml.etree import ElementTree as ET

import pytest

from src.metamodel.codegenerator.serializer.xml_serializer import XmlSerializer
from tests.unit.utils.setup_desciptors import make_class, make_enum, make_field


class TestXmlSerializer:
    """Tests for serializing the descriptors to xml."""

    @pytest.fixture
    def visitor(self):
        return XmlSerializer()

    def _parse(self, visitor: XmlSerializer) -> ET.Element:
        return ET.fromstring(visitor.render())

    def test_render_produces_valid_xml(self, visitor):
        root = self._parse(visitor)
        assert root.tag == "context"

    def test_visit_class_appears_in_output(self, visitor):
        visitor.visit_class(make_class("MyClass"))
        root = self._parse(visitor)
        classes = root.find("classes").findall("class")
        assert any(c.get("name") == "MyClass" for c in classes)

    def test_visit_class_includes_fields(self, visitor):
        field = make_field("my_field", base_type="str")
        cls = make_class("MyClass", fields=[field])
        visitor.visit_class(cls)
        root = self._parse(visitor)
        fields = root.find("classes").find("class").findall("field")
        assert len(fields) == 1
        assert fields[0].get("name") == "my_field"
        assert fields[0].get("base_type") == "str"

    def test_visit_enum_appears_in_output(self, visitor):
        visitor.visit_enum(make_enum("MyEnum", options={"KEY": "VALUE"}))
        root = self._parse(visitor)
        enums = root.find("enums").findall("enum")
        assert any(e.get("name") == "MyEnum" for e in enums)

    def test_visit_enum_includes_options(self, visitor):
        visitor.visit_enum(make_enum("MyEnum", options={"KEY": "VALUE"}))
        root = self._parse(visitor)
        options = root.find("enums").find("enum").findall("option")
        assert len(options) == 1
        assert options[0].get("key") == "KEY"
        assert options[0].get("value") == "VALUE"

    def test_append_api_config_appears_in_output(self, visitor):
        visitor.append_api_config({"package": "com.example"})
        root = self._parse(visitor)
        entries = root.find("api_config").findall("entry")
        assert any(e.get("key") == "package" and e.get("value") == "com.example" for e in entries)

    def test_optional_field_attribute_association_kind(self, visitor):
        field = make_field("my_field", association_kind="composition")
        visitor.visit_class(make_class("MyClass", fields=[field]))
        root = self._parse(visitor)
        f = root.find("classes").find("class").find("field")
        assert f.get("association_kind") == "composition"

    def test_optional_field_attribute_omitted_when_none(self, visitor):
        field = make_field("my_field", association_kind=None, default=None)
        visitor.visit_class(make_class("MyClass", fields=[field]))
        root = self._parse(visitor)
        f = root.find("classes").find("class").find("field")
        assert f.get("association_kind") is None
        assert f.get("default") is None

    def test_file_extension_is_xml(self, visitor):
        assert visitor.file_extension == "xml"

    def test_multiple_classes_all_appear(self, visitor):
        visitor.visit_class(make_class("ClassA"))
        visitor.visit_class(make_class("ClassB"))
        root = self._parse(visitor)
        names = [c.get("name") for c in root.find("classes").findall("class")]
        assert "ClassA" in names
        assert "ClassB" in names
