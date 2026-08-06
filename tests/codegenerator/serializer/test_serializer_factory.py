import pytest

from src.metamodel.codegenerator.serializer.serializer_factory import get_serializer
from src.metamodel.codegenerator.serializer.json_serializer import JsonSerializer
from src.metamodel.codegenerator.serializer.xml_serializer import XmlSerializer


class TestSerializerFactory:
    """Tests for the serializer factory."""

    def test_returns_json_serializer_for_json(self):
        assert isinstance(get_serializer("json"), JsonSerializer)

    def test_returns_xml_serializer_for_xml(self):
        assert isinstance(get_serializer("xml"), XmlSerializer)

    def test_raises_value_error_for_unknown_format(self):
        with pytest.raises(ValueError):
            get_serializer("csv")

    def test_error_message_includes_unknown_format(self):
        with pytest.raises(ValueError, match="unknown_fmt"):
            get_serializer("unknown_fmt")

    def test_raises_for_empty_string(self):
        with pytest.raises(ValueError):
            get_serializer("")

    def test_raises_for_uppercase_format(self):
        """Format matching is case-sensitive — 'JSON' is not a registered key."""
        with pytest.raises(ValueError):
            get_serializer("JSON")
