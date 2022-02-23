"""Encapsulates quote body and author."""


class QuoteModel():
    """Class to quote body and author."""

    def __init__(self, body, author):
        """Initialize body and author arguments."""
        self.body = body
        self.author = author

    def __repr__(self):
        """Return string in readable format."""
        return '{self.body}, {self.author}'.format(self=self)
