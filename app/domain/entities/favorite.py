from dataclasses import dataclass


@dataclass(frozen=True)
class Favorite:
    user_id: int
    isbn: str
