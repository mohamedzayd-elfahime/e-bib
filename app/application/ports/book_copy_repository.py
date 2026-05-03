from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.book_copy import BookCopy


class BookCopyRepository(ABC):
    """
    Port responsible for accessing and persisting BookCopy entities.
    """

    @abstractmethod
    def find_available_for_update(self, isbn: str) -> Optional[BookCopy]:
        """
        Return one available BookCopy for the given ISBN
        and lock it for concurrent access.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, book_copy: BookCopy) -> None:
        """
        Persist the current state of a BookCopy.
        """
        raise NotImplementedError

    @abstractmethod
    def count_available(self, isbn: str) -> int:
        """
        Return the number of available copies for a given ISBN.
        """
        raise NotImplementedError
