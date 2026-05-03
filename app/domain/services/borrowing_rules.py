from datetime import datetime
from domain.entities.borrowing import Borrowing, BorrowingStatus


PENDING_EXPIRATION_DAYS = 2


def should_expire_pending(borrowing: Borrowing, now: datetime) -> bool:
    return (
        borrowing.status == BorrowingStatus.PENDING
        and (now - borrowing.borrowed_at).days > PENDING_EXPIRATION_DAYS
    )


def should_mark_overdue(borrowing: Borrowing, now: datetime) -> bool:
    return (
        borrowing.status == BorrowingStatus.ACTIVE
        and now > borrowing.due_at
    )
