"""Helper class to ingest TEXT files."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TEXTIngestor(IngestorInterface):
    """Ingest and parse TEXT files."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Create list of quotes from a file."""
        if not cls.can_ingest(path):
            raise Exception('Failed to ingest TXT file')

        quotes = []

        with open(path) as f:
            for line in f.readlines():
                line = line.strip('\n\r').strip()
                if len(line) > 0:
                    parse = line.split('-')
                    new_quote = QuoteModel(parse[0].strip(), parse[1].strip())
                    quotes.append(new_quote)

        return quotes
