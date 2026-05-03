# app/domain/events/book_returned.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.domain.events.base import DomainEvent

@dataclass(frozen=True)
class BookReturned(DomainEvent):
    borrowing_id: UUID
    book_copy_id: UUID
    user_id: UUID
    returned_at: datetime
