"""A Quote contains a body of text and the author of that text."""

class QuoteModel():
    """Each quote has text and an author."""

    def __init__(self, body: str, author: str):
        """
        :param body: A body of text
        :param author: The author of the text
        """
        self.body = body
        self.author = author
