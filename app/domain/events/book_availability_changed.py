from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BookAvailabilityChanged:
    """
    Domain event emitted when the availability of a book changes.
    This event carries factual information only.
    """
    isbn: str
    available_copies: int
    occurred_at: datetime
