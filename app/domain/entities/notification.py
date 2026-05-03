# domain/entities/notification.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    BORROWING_OVERDUE = "borrowing_overdue"
    BORROWING_EXPIRED = "borrowing_expired"
    BORROWING_RETURNED = "borrowing_returned"
    BOOK_ADDED = "book_added"


@dataclass
class Notification:
    id: int | None
    user_id: int
    type: NotificationType
    message: str
    is_read: bool
    created_at: datetime
