"""Helper class to ingest PDF files."""
from typing import List
import subprocess
import os
import random

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingest and parse PDF files."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Create list of quotes from a file."""
        if not cls.can_ingest(path):
            raise Exception('Failed to ingest PDF file')

        tmp = '/tmp/{}.txt'.format(random.randint(0, 100000000))
        p = subprocess.run(['pdftotext', path, tmp], stdout=subprocess.PIPE)

        file_ref = open(tmp, "r")
        quotes = []

        for line in file_ref.readlines():
            line = line.strip('\n\r').strip()
            if len(line) > 0:
                parse = line.split(' - ')
                new_quote = QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)

        file_ref.close()
        os.remove(tmp)
        return quotes
