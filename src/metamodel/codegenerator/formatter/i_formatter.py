from abc import ABC, abstractmethod


class Formatter(ABC):
    """The formater class. Base for the strategy pattern."""

    @abstractmethod
    def format_descriptors(self, context: dict) -> dict:
        """Returns formated descriptors"""
