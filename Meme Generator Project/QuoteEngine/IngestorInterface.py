"""Abstract class used as a template by helper classes."""
from abc import ABC, abstractmethod

from typing import List
from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Template class to ingest and parse data from files."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if file extension is valid."""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Logic is in helper classes."""
        pass
