# domain/entities/borrowing.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from app.domain.events.borrowing_events import BorrowingReturned


class BorrowingStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    OVERDUE = "overdue"
    RETURNED = "returned"


@dataclass
class Borrowing:
    id: int | None
    user_id: int
    book_copy_id: int
    status: BorrowingStatus
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None = None

    # 🔹 événements domaine (NON persistés)
    _events: List[object] = field(default_factory=list, init=False, repr=False)

    def activate(self):
        if self.status != BorrowingStatus.PENDING:
            raise ValueError("Invalid state")
        self.status = BorrowingStatus.ACTIVE

    def mark_overdue(self):
        if self.status == BorrowingStatus.ACTIVE:
            self.status = BorrowingStatus.OVERDUE

    def mark_returned(self):
        if self.status == BorrowingStatus.RETURNED:
            raise ValueError("Already returned")

        self.status = BorrowingStatus.RETURNED
        self.returned_at = datetime.utcnow()

        #  création de l’événement domaine
        self._events.append(
            BorrowingReturned(
                borrowing_id=self.id,
                user_id=self.user_id,
                book_copy_id=self.book_copy_id,
            )
        )

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events
