# application/policies/reservation_policy.py

class ReservationDecision:
    def __init__(self, allowed: bool, reason: str | None = None):
        self.allowed = allowed
        self.reason = reason


class ReservationPolicy:
    """
    Application-level policy.
    Decides whether a user can reserve a book.
    """

    def __init__(self, reservation_repository, book_copy_repository):
        self.reservation_repository = reservation_repository
        self.book_copy_repository = book_copy_repository

    def can_reserve(self, user_id: int, isbn: str) -> ReservationDecision:
        # Rule 1: cannot reserve if at least one copy is available
        if self.book_copy_repository.count_available(isbn) > 0:
            return ReservationDecision(
                allowed=False,
                reason="BOOK_AVAILABLE"
            )

        # Rule 2: one active reservation per user per book
        if self.reservation_repository.has_active_reservation(user_id, isbn):
            return ReservationDecision(
                allowed=False,
                reason="RESERVATION_ALREADY_EXISTS"
            )

        return ReservationDecision(allowed=True)
