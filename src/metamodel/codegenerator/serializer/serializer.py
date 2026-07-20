from abc import ABC, abstractmethod

from ..mapper import Visitor


class Serializer(Visitor, ABC):
    """
    Abstract base visitor that applies naming-convention formatting to descriptors.

    Handles class and enum formatting directly; delegates field formatting to
    subclasses, which may differ in their target conventions (e.g.
    snake_case for Python, camelCase for Java).
    """

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension for the serialized output (without leading dot)."""
        pass

    @abstractmethod
    def append_api_config(self, api_config: dict) -> None:
        pass
