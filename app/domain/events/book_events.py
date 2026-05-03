# domain/events/book_events.py
from domain.events.base import DomainEvent


class BookAdded(DomainEvent):
    def __init__(self, isbn: str):
        super().__init__()
        self.isbn = isbn
