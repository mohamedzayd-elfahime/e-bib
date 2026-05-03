# application/dto/borrow_book.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BorrowBookCommand:
    user_id: int
    isbn: str


@dataclass(frozen=True)
class BorrowBookResult:
    success: bool
    reason: Optional[str] = None
