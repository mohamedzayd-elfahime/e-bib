# app/application/dtos/reserve_book.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ReserveBookCommand:
    user_id: int
    isbn: str
