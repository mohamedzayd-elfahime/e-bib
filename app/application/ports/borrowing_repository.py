from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.borrowing import Borrowing, BorrowingStatus


class BorrowingRepository(ABC):
    """
    Port responsible for persisting and reading Borrowing entities.
    """

    @abstractmethod
    def save(self, borrowing: Borrowing) -> None:
        """
        Persist a Borrowing entity (create or update).
        """
        raise NotImplementedError

    @abstractmethod
    def has_active_borrowing(self, user_id: int) -> bool:
        """
        Return True if the user has an ACTIVE borrowing.
        """
        raise NotImplementedError

    @abstractmethod
    def has_overdue_borrowing(self, user_id: int) -> bool:
        """
        Return True if the user has an OVERDUE borrowing.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, borrowing_id: int) -> Optional[Borrowing]:
        """
        Load a Borrowing by its identifier.
        """
        raise NotImplementedError
