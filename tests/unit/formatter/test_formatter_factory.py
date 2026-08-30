import pytest

from src.metamodel.codegenerator.formatter.formatter_factory import get_formatter
from src.metamodel.codegenerator.formatter.snake_case_formatter import SnakeCaseFormatter
from src.metamodel.codegenerator.formatter.camel_case_formatter import CamelCaseFormatter


class TestGetFormatter:
    """Tests for the formatter factory."""

    def test_returns_snake_case_formatter(self):
        assert isinstance(get_formatter("snake_case"), SnakeCaseFormatter)

    def test_returns_camel_case_formatter(self):
        assert isinstance(get_formatter("camelCase"), CamelCaseFormatter)

    def test_raises_value_error_for_unknown_style(self):
        with pytest.raises(ValueError):
            get_formatter("PascalCase")

    def test_error_message_includes_unknown_style(self):
        with pytest.raises(ValueError, match="PascalCase"):
            get_formatter("PascalCase")

    def test_raises_for_empty_string(self):
        with pytest.raises(ValueError):
            get_formatter("")

    def test_raises_for_wrong_casing(self):
        """Format matching is case-sensitive — 'Snake_Case' is not a registered key."""
        with pytest.raises(ValueError):
            get_formatter("Snake_Case")
