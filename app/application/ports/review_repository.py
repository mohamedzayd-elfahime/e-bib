from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.review import Review


class ReviewRepository(ABC):

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> list[Review]:
        """Return all reviews for a book"""
        raise NotImplementedError
    def create(self, review: Review) -> Review:
        """Create a new review and return it with ID"""
        raise NotImplementedError
