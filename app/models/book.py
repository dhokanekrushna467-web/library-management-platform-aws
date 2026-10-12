class Book:
    def __init__(
        self,
        book_id,
        title,
        author,
        total_copies=1,
        available_copies=None
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies

        if available_copies is None:
            self.available_copies = total_copies
        else:
            self.available_copies = available_copies

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }
