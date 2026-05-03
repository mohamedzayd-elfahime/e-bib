class BorrowingDecision:
    def __init__(self, allowed: bool, reason: str | None = None):
        self.allowed = allowed
        self.reason = reason


class BorrowingPolicy:
    """
    Application-level policy.
    Decides whether a user can borrow a book.
    """

    MAX_ACTIVE_BORROWINGS = 2

    def __init__(self, borrowing_repository):
        self.borrowing_repository = borrowing_repository

    def can_borrow(self, user_id: int, isbn: str) -> BorrowingDecision:
        if self.borrowing_repository.has_overdue_borrowing(user_id):
            return BorrowingDecision(
                allowed=False,
                reason="OVERDUE_BORROWING"
            )

        active_count = self.borrowing_repository.count_active_borrowings(user_id)
        if active_count >= self.MAX_ACTIVE_BORROWINGS:
            return BorrowingDecision(
                allowed=False,
                reason="MAX_ACTIVE_BORROWINGS_REACHED"
            )

        if self.borrowing_repository.has_active_borrowing_for_isbn(user_id, isbn):
            return BorrowingDecision(
                allowed=False,
                reason="BOOK_ALREADY_BORROWED"
            )

        return BorrowingDecision(allowed=True)
