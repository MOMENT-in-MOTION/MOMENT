from typing import Any

from .json_serializer import JsonSerializer
from .xml_serializer import XmlSerializer

from ..mapper import Visitor


def get_serializer(fmt: str) -> Visitor:
    """
    Returns a serializer for the given output format.

    Args:
        fmt: The target format (e.g "json", "xml").

    Returns:
        A concrete Visitor that serializes a context to the requested format.

    Raises:
        ValueError: If `fmt` does not match any registered serializer.
    """
    serializers = {
        "json": JsonSerializer(),
        "xml":  XmlSerializer(),
    }
    serializer = serializers.get(fmt)

    if serializer is None:
        raise ValueError(f"Unknown format style: '{fmt}'")

    return serializer
