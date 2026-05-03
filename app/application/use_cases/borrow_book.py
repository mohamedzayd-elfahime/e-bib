from app.application.dto.borrow_book import BorrowBookCommand, BorrowBookResult
from app.domain.entities.borrowing import Borrowing, BorrowingStatus
from datetime import timedelta


class BorrowBookUseCase:
    def __init__(
        self,
        book_copy_repository,
        borrowing_repository,
        borrowing_policy,
        transaction_manager,
        clock,
    ):
        self.book_copy_repository = book_copy_repository
        self.borrowing_repository = borrowing_repository
        self.borrowing_policy = borrowing_policy
        self.tx = transaction_manager
        self.clock = clock

    def execute(self, command: BorrowBookCommand) -> BorrowBookResult:
        # 1) Application policy (NO transaction, NO lock)
        decision = self.borrowing_policy.can_borrow(
            user_id=command.user_id,
            isbn=command.isbn,
        )

        if not decision.allowed:
            return BorrowBookResult(
                success=False,
                reason=decision.reason,
            )

        try:
            # 2) Start transaction
            self.tx.begin()

            # 3) Lock one available copy
            book_copy = self.book_copy_repository.find_available_for_update(
                command.isbn
            )

            if book_copy is None:
                self.tx.rollback()
                return BorrowBookResult(
                    success=False,
                    reason="NO_AVAILABLE_COPY",
                )

            # 4) Change domain state
            if not book_copy.borrow():
                self.tx.rollback()
                return BorrowBookResult(
                    success=False,
                    reason="COPY_NOT_BORROWABLE",
                )

            now = self.clock.now()
            BORROW_DURATION_DAYS = 14

            due_at = now + timedelta(days=BORROW_DURATION_DAYS)
            borrowing = Borrowing(
                id=None,
                user_id=command.user_id,
                book_copy_id=book_copy.id,
                status=BorrowingStatus.PENDING,
                borrowed_at=now,
                due_at=due_at,
            )

            self.book_copy_repository.save(book_copy)
            self.borrowing_repository.save(borrowing)

            self.tx.commit()

            return BorrowBookResult(success=True)

        except Exception:
            self.tx.rollback()
            raise
