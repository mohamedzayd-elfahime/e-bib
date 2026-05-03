from app.application.ports.book_repository import BookReadRepository
from app.application.ports.book_copy_repository import BookCopyRepository
from app.application.ports.favorite_repository import FavoriteRepository
from app.application.read_models.book import BookListItem


class GetSuggestedBooksUseCase:
    """
    Use case:
    - Suggest books from the same category as the current book
    - Exclude the current book
    - Enrich with availability and favorite status
    """

    def __init__(
        self,
        book_repo: BookReadRepository,
        book_copy_repo: BookCopyRepository,
        favorite_repo: FavoriteRepository,
    ):
        self.book_repo = book_repo
        self.book_copy_repo = book_copy_repo
        self.favorite_repo = favorite_repo

    def execute(
        self,
        *,
        isbn: str,
        user_id: int | None,
        limit: int = 3,
    ) -> list[BookListItem]:

        # 1. Read-only suggestion (same category, exclude ISBN)
        books = self.book_repo.get_suggested_by_category(
            isbn=isbn,
            limit=limit,
        )

        if not books:
            return []

        # 2. Favorites (user-aware)
        favorite_isbns: set[str] = set()
        if user_id is not None:
            favorite_isbns = self.favorite_repo.get_favorite_isbns(user_id)

        # 3. Enrich each book (availability + status)
        for book in books:
            book.available_copies = self.book_copy_repo.count_available(book.isbn)
            book.is_favorite = book.isbn in favorite_isbns

            # status = user-centric availability
            book.status = "available" if book.available_copies > 0 else "unavailable"

        return books
