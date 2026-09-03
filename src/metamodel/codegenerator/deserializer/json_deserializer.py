import json

from .deserializer import Deserializer, DeserializationError, RestoredModel
from .descriptor_builder import build_context


class JsonDeserializer(Deserializer):
    """
    Restores a context from the JSON document written by JsonSerializer.

    JSON carries booleans, numbers and lists natively, so the parsed structure
    is passed to the descriptor factories unchanged.
    """

    @property
    def file_extension(self) -> str:
        return "json"

    def parse(self, raw: str) -> RestoredModel:
        """
        Parse a JSON document into a restored context and api config.

        Raises:
            DeserializationError: If the document is not valid JSON, is not an
                object at the root, or is missing a required key.
        """
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise DeserializationError(f"Invalid JSON document: {e}") from e

        if not isinstance(data, dict):
            raise DeserializationError(
                f"Expected a JSON object at the document root, "
                f"got {type(data).__name__}"
            )

        return RestoredModel(
            context=build_context(data),
            api_config=data.get("api_config", {}),
        )
