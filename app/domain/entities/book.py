# domain/entities/book.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    isbn: str                 # PK métier
    title: str
    author: str
    description: str | None
    category_id: int
    cover_url: str | None = None
