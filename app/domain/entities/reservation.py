from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ReservationStatus(str, Enum):
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


@dataclass
class Reservation:
    id: int | None
    user_id: int
    isbn: str
    status: ReservationStatus
    created_at: datetime
