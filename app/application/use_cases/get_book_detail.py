from app.application.ports.book_repository import BookReadRepository
from app.application.ports.book_copy_repository import BookCopyRepository
from app.application.ports.favorite_repository import FavoriteRepository
from app.application.read_models.book import BookDetail
from app.application.ports.borrowing_repository import BorrowingRepository
from app.application.ports.reservation_repository import ReservationRepository


class GetBookDetail:
    """
    Use case: return book detail with USER-CENTRIC status
    and GLOBAL availability (copies).
    """

    def __init__(
        self,
        book_repo: BookReadRepository,
        book_copy_repo: BookCopyRepository,
        favorite_repo: FavoriteRepository,
        borrowing_repo: BorrowingRepository,
        reservation_repo: ReservationRepository,
    ):
        self.book_repo = book_repo
        self.book_copy_repo = book_copy_repo
        self.favorite_repo = favorite_repo
        self.borrowing_repo = borrowing_repo
        self.reservation_repo = reservation_repo

    def execute(
        self,
        *,
        isbn: str,
        user_id: int | None,
    ) -> BookDetail:

        # ---------- Book (catalog) ----------
        book = self.book_repo.get_book_detail(isbn)
        if book is None:
            raise ValueError("Book not found")

        # ---------- Global availability ----------
        available_copies = self.book_copy_repo.count_available(isbn)

        # ---------- Favorite ----------
        is_favorite = (
            self.favorite_repo.exists(user_id=user_id, isbn=isbn)
            if user_id is not None
            else False
        )

        # ---------- USER-CENTRIC STATUS ----------
        status = "available"

        if user_id is not None:

            # 1. Late (highest priority)
            if self.borrowing_repo.has_overdue_borrowing_for_isbn(user_id, isbn):
                status = "late"

            # 2. Borrowed
            elif self.borrowing_repo.has_active_borrowing_for_isbn(user_id, isbn):
                status = "borrowed"

            # 3. Reserved
            elif self.reservation_repo.has_active_reservation(user_id, isbn):
                status = "reserved"

            # 4. Available (default)
            else:
                status = "available"

        return BookDetail(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            description=book.description,
            category=book.category,
            available_copies=available_copies,
            status=status,
            is_favorite=is_favorite,
        )
