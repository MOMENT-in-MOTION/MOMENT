import re

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.metamodel.codegenerator.serializer.serialize_context import (
    serialize_context,
    _write_serialized_output
)

@pytest.fixture
def mock_context():
    return MagicMock()


@pytest.fixture
def mock_serializer():
    serializer = MagicMock()
    serializer.file_extension = "json"
    serializer.render.return_value = '{"classes": []}'
    return serializer


@pytest.fixture
def api_config():
    return {"package": "com.example"}


class TestSerializeContext:
    """Tests for serializing the context descriptors."""

    def test_visits_context(self, mock_context, api_config, mock_serializer, tmp_path):
        serialize_context(mock_context, api_config, mock_serializer, tmp_path)
        mock_serializer.visit_context.assert_called_once_with(mock_context)

    def test_appends_api_config(self, mock_context, api_config, mock_serializer, tmp_path):
        serialize_context(mock_context, api_config, mock_serializer, tmp_path)
        mock_serializer.append_api_config.assert_called_once_with(api_config)

    def test_calls_render(self, mock_context, api_config, mock_serializer, tmp_path):
        serialize_context(mock_context, api_config, mock_serializer, tmp_path)
        mock_serializer.render.assert_called_once()

    def test_writes_file_with_correct_extension(
        self,
        mock_context,
        api_config,
        mock_serializer,
        tmp_path
    ):
        serialize_context(mock_context, api_config, mock_serializer, tmp_path)
        expected = tmp_path / "serialized_model.json"
        assert expected.exists()

    def test_written_content_matches_render_output(
        self,
        mock_context,
        api_config,
        mock_serializer,
        tmp_path
    ):
        serialize_context(mock_context, api_config, mock_serializer, tmp_path)
        output_path = tmp_path / "serialized_model.json"
        assert output_path.read_text(encoding="UTF-8") == '{"classes": []}'

    def test_uses_serializer_file_extension_for_filename(self, mock_context, api_config, tmp_path):
        xml_serializer = MagicMock()
        xml_serializer.file_extension = "xml"
        xml_serializer.render.return_value = "<context/>"
        serialize_context(mock_context, api_config, xml_serializer, tmp_path)
        assert (tmp_path / "serialized_model.xml").exists()


class TestWriteSerializedOutput:
    """Tests for the writting the serilized context to a file."""

    def test_writes_content_to_file(self, tmp_path):
        output_path = tmp_path / "output.json"
        _write_serialized_output('{"key": "value"}', output_path)
        assert output_path.read_text(encoding="UTF-8") == '{"key": "value"}'

    def test_writes_utf8_encoding(self, tmp_path):
        content = "Ä Ö Ü ß"
        output_path = tmp_path / "output.json"
        _write_serialized_output(content, output_path)
        assert output_path.read_text(encoding="UTF-8") == content

    def test_raises_os_error_on_write_failure(self, tmp_path):
        output_path = tmp_path / "output.json"
        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            with pytest.raises(OSError, match="Failed to write file"):
                _write_serialized_output("content", output_path)

    def test_os_error_includes_path_in_message(self, tmp_path):
        output_path = tmp_path / "output.json"
        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            with pytest.raises(OSError, match=re.escape(str(output_path))):
                _write_serialized_output("content", output_path)

    def test_os_error_chains_original_exception(self, tmp_path):
        output_path = tmp_path / "output.json"
        original = OSError("disk full")
        with patch.object(Path, "write_text", side_effect=original):
            with pytest.raises(OSError) as exc_info:
                _write_serialized_output("content", output_path)
            assert exc_info.value.__cause__ is original
