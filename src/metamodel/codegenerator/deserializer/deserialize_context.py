from pathlib import Path

from .deserializer import Deserializer, RestoredModel
from .deserializer_factory import get_deserializer


def deserialize_context(
    input_path: Path,
    deserializer: Deserializer | None = None,
) -> RestoredModel:
    """
    Restore a serialized model from a file.

    Args:
        input_path: Path to a previously serialized model document.
        deserializer: Deserializer to use. Defaults to one selected from the
            file suffix.

    Returns:
        The restored context together with the embedded api config.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If no deserializer is registered for the file suffix.
        DeserializationError: If the document is malformed.
    """
    if deserializer is None:
        deserializer = get_deserializer(input_path.suffix.lstrip("."))

    return deserializer.parse(_read_serialized_input(input_path))


def _read_serialized_input(input_path: Path) -> str:
    """Read serialized input (JSON, XML, ...) from a file."""
    try:
        return input_path.read_text(encoding="UTF-8")
    except OSError as e:
        raise OSError(f"Failed to read file '{input_path}': {e}") from e
