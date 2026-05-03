from abc import ABC, abstractmethod

class FavoriteRepository(ABC):

    @abstractmethod
    def exists(self, user_id: int, isbn: int) -> bool:
        pass

    @abstractmethod
    def add(self, user_id: int, isbn: int) -> None:
        pass

    @abstractmethod
    def remove(self, user_id: int, isbn: int) -> None:
        pass
        
    @abstractmethod
    def get_favorite_isbns(self, user_id: int) -> set[str]:
        """Batch READ: return all favorite ISBNs of a user"""
        pass