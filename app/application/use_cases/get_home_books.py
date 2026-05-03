from app.application.ports.book_repository import BookReadRepository
from app.application.ports.favorite_repository import FavoriteRepository


class GetHomeBooksUseCase:
    """
    Use case: get latest books per category for home page (stateless UI).
    """

    def __init__(
        self,
        book_repo: BookReadRepository,
        favorite_repo: FavoriteRepository,
    ):
        self.book_repo = book_repo
        self.favorite_repo = favorite_repo

    async def execute(
        self,
        *,
        limit_per_category: int,
        user_id: int | None,
    ):
        books_by_category = await self.book_repo.get_latest_books_by_category(
            limit_per_category=limit_per_category
        )

        favorite_isbns: set[str] = set()
        if user_id is not None:
            favorite_isbns = self.favorite_repo.get_favorite_isbns(user_id)

        for books in books_by_category.values():
            for book in books:
                book.is_favorite = book.isbn in favorite_isbns

        return books_by_category
