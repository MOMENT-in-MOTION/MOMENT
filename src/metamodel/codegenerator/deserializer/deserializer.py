from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..mapper import TemplateContext


class DeserializationError(Exception):
    """Raised when a serialized document cannot be restored into a TemplateContext."""


@dataclass
class RestoredModel:
    """
    A restored context together with the api config it was serialized with.

    Attributes:
        context:    The rebuilt TemplateContext. Already formatted, since the
                    serializer runs after the formatter, so the restore path
                    must not format it again.
        api_config: The api configuration embedded in the document, empty if
                    the document carries none.
    """
    context: TemplateContext
    api_config: dict[str, str]


class Deserializer(ABC):
    """
    Abstract base for restoring a serialized model.

    Counterpart to Serializer, but deliberately not a Visitor: there are no
    descriptors to traverse until parsing has produced them. Concrete
    deserializers reduce their format to the dictionary shape understood by
    descriptor_builder.build_context, which keeps descriptor reconstruction
    in a single place.
    """

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension this deserializer reads (without leading dot)."""
        pass

    @abstractmethod
    def parse(self, raw: str) -> RestoredModel:
        """Rebuild a TemplateContext and api config from a serialized document."""
        pass
