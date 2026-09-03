from .deserializer import Deserializer
from .json_deserializer import JsonDeserializer
from .xml_deserializer import XmlDeserializer


def get_deserializer(fmt: str) -> Deserializer:
    """
    Returns a deserializer for the given input format.

    Args:
        fmt: The source format (e.g "json", "xml").

    Returns:
        A concrete Deserializer that restores a context from the requested format.

    Raises:
        ValueError: If `fmt` does not match any registered deserializer.
    """
    deserializers = {
        "json": JsonDeserializer,
        "xml":  XmlDeserializer,
    }
    deserializer = deserializers.get(fmt)

    if deserializer is None:
        raise ValueError(f"Unknown format style: '{fmt}'")

    return deserializer()
