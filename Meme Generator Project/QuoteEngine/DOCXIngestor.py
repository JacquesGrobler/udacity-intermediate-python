"""Helper class to ingest DOCX files."""
from typing import List
import docx

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DOCXIngestor(IngestorInterface):
    """Ingest and parse DOCX files."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Create list of quotes from a file."""
        if not cls.can_ingest(path):
            raise Exception('Failed to ingest DOCX file')

        quotes = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse = para.text.split(' - ')
                new_quote = QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)

        return quotes
