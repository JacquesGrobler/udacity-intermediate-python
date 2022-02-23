"""Use helper classes to ingest data, based on file type."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .CSVIngestor import CSVIngestor
from .DOCXIngestor import DOCXIngestor
from .PDFIngestor import PDFIngestor
from .TEXTIngestor import TEXTIngestor


class Ingestor(IngestorInterface):
    """Ingest and parse files."""

    ingestors = [CSVIngestor, DOCXIngestor, PDFIngestor, TEXTIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Use helper class to create a list of quotes."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
