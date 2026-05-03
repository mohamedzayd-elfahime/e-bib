# domain/entities/book_copy.py
from dataclasses import dataclass
from enum import Enum


class BookCopyStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"


@dataclass
class BookCopy:
    id: int
    isbn: str
    status: BookCopyStatus

    def can_be_borrowed(self) -> bool:
        return self.status == BookCopyStatus.AVAILABLE

    def borrow(self) -> bool:
        if not self.can_be_borrowed():
            return False
        self.status = BookCopyStatus.BORROWED
        return True

    def can_be_returned(self) -> bool:
        return self.status == BookCopyStatus.BORROWED

    def return_copy(self) -> bool:
        if not self.can_be_returned():
            return False
        self.status = BookCopyStatus.AVAILABLE
        return True
