from typing import Iterable
from domain.entities.book_copy import BookCopy, BookCopyStatus


def has_available_copy(copies: Iterable[BookCopy]) -> bool:
    return any(copy.status == BookCopyStatus.AVAILABLE for copy in copies)


def first_available_copy(copies: Iterable[BookCopy]) -> BookCopy | None:
    for copy in copies:
        if copy.status == BookCopyStatus.AVAILABLE:
            return copy
    return None
