from dataclasses import dataclass


@dataclass(frozen=True)
class BookFilters:
    """
    Structured filters for book listing.
    """
    category: str | None = None
    author: str | None = None
    search: str | None = None
