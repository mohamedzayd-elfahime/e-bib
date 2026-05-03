from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return a user by email or None if not found."""
        pass

    @abstractmethod
    def create_google_user(self, email: str) -> User:
        """Create a user authenticated via OAuth and return it."""
        pass