from abc import ABC, abstractmethod
from app.application.read_models.book import BookListItem, BookDetail
from app.application.read_models.pagination import PaginatedResult
from app.application.filters.book_filters import BookFilters


class BookReadRepository(ABC):
    """
    READ-ONLY repository for books.
    Used for SSR pages and public browsing.
    """

    # ---------- HOME PAGE ----------

    @abstractmethod
    async def get_latest_books_by_category(
        self,
        *,
        limit_per_category: int
    ) -> dict[str, list[BookListItem]]:
        """
        Home page:
        Return latest books grouped by category.
        """


    # ---------- ALL BOOKS PAGE ----------

    @abstractmethod
    def list_books(
        self,
        *,
        filters: BookFilters,
        page: int,
        size: int
    ) -> PaginatedResult[BookListItem]:
        """
        Paginated book listing with filters.
        """


    # ---------- BOOK DETAIL PAGE ----------

    @abstractmethod
    async def get_book_detail(
        self,
        isbn: str
    ) -> BookDetail | None:
        """
        Full detail of a single book.
        """


    @abstractmethod
    async def get_suggested_books(
        self,
        *,
        isbn: str,
        limit: int
    ) -> list[BookListItem]:
        """
        Suggested books (same category, exclude current book).
        """


    # ---------- USER PAGES ----------

    @abstractmethod
    async def list_favorite_books(
        self,
        *,
        user_id: int
    ) -> list[BookListItem]:
        """
        User favorites / wishlist.
        """


    @abstractmethod
    async def list_borrowing_history(
        self,
        *,
        user_id: int
    ) -> list[BookListItem]:
        """
        Borrowing history of a user.
        """


    # ---------- INTERNAL / UTILITY ----------

    @abstractmethod
    async def exists_by_isbn(self, *, isbn: str) -> bool:
        """
        Check book existence (validation, admin).
        """
    @abstractmethod
    def get_suggested_by_category(
        self,
        *,
        isbn: str,
        limit: int,
    ) -> list[BookListItem]:
        """
        Return books from the same category as the given ISBN,
        excluding the book itself.
        """
        raise NotImplementedError
