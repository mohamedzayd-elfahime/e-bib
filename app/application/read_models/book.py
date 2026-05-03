from dataclasses import dataclass
from typing import Literal


@dataclass
class BookListItem:
    """
    Lightweight read model for book listings:
    - home page
    - all books
    - favorites
    - suggestions
    """
    isbn: str
    title: str
    author: str
    category: str
    cover_url: str | None
    is_favorite: bool = False
    available_copies: int = 0
    status: Literal["available", "borrowed", "reserved", "late"] = "available"



@dataclass(frozen=True)
class BookDetail:
    isbn: str
    title: str
    author: str
    description: str
    category: str
    available_copies: int
    status: Literal["available", "borrowed", "reserved", "late"] = "available"
    is_favorite: bool = False
