from dataclasses import dataclass

@dataclass(frozen=True)
class CategoryFilterItem:
    id: int
    name: str
    total_books: int
