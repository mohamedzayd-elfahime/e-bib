from abc import ABC, abstractmethod
from app.application.read_models.category import CategoryFilterItem


class CategoryRepositoryMySQL(ABC):

    @abstractmethod
    def list_with_book_count(self) -> list[CategoryFilterItem]:
        """
        Return all categories with number of books per category.
        """
        
