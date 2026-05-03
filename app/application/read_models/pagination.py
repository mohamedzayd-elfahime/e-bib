from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    """
    Generic pagination container.
    """
    items: list[T]
    total: int
    page: int
    size: int
