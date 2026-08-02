from pathlib import Path

from ..mapper import TemplateContext

from .serializer import Serializer


def serialize_context(
    context: TemplateContext,
    api_config: dict[str],
    serializer: Serializer,
    output_dir: Path,
) -> None:
    """Serialize the formatted context to a file using the given serializer."""
    serializer.visit_context(context)
    serializer.append_api_config(api_config)

    output_path = output_dir / f"serialized_model.{serializer.file_extension}"
    _write_serialized_output(serializer.render(), output_path)


def _write_serialized_output(serialized: str, output_path: Path) -> None:
    """Write serialized output (JSON, XML, ...) to a file."""
    try:
        output_path.write_text(serialized, encoding="UTF-8")
    except OSError as e:
        raise OSError(f"Failed to write file '{output_path}': {e}") from e
