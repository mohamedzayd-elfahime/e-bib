from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Review:
    id: int
    user_id: int
    isbn: str
    rating: int        # tinyint(3)
    comment: str | None
    created_at: datetime
