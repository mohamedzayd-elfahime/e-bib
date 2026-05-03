from abc import ABC, abstractmethod
from app.domain.entities.notification import Notification

class NotificationRepository(ABC):

    @abstractmethod
    def save(self, notification: Notification) -> None:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> list[Notification]:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int) -> None:
        pass

    @abstractmethod
    def count_unread(self, user_id: int) -> int:
        pass
