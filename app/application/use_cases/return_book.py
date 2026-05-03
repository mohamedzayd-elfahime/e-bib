from app.application.dto.return_book import ReturnBookResult
from app.infrastructure.event_bus.null import NullEventBus



class ReturnBookUseCase:
    def __init__(
        self,
        borrowing_repository,
        book_copy_repository,
        transaction_manager,
        event_bus=None,  #  optionnel
    ):
        self.borrowing_repository = borrowing_repository
        self.book_copy_repository = book_copy_repository
        self.tx = transaction_manager
        self.event_bus = event_bus or NullEventBus()  #  fallback propre

    def execute(self, borrowing_id: int) -> ReturnBookResult:
        try:
            self.tx.begin()

            borrowing = self.borrowing_repository.find_by_id(borrowing_id)
            if borrowing is None:
                self.tx.rollback()
                return ReturnBookResult(
                    success=False,
                    reason="BORROWING_NOT_FOUND"
                )

            book_copy = self.book_copy_repository.find_by_id(
                borrowing.book_copy_id
            )
            if book_copy is None:
                self.tx.rollback()
                return ReturnBookResult(
                    success=False,
                    reason="BOOK_COPY_NOT_FOUND"
                )

            try:
                borrowing.mark_returned()
            except ValueError:
                self.tx.rollback()
                return ReturnBookResult(
                    success=False,
                    reason="BORROWING_ALREADY_RETURNED"
                )

            book_copy.return_copy()

            self.borrowing_repository.save(borrowing)
            self.book_copy_repository.save(book_copy)

            self.tx.commit()

            # EVENT-DRIVEN 
            events = borrowing.pull_events()
            self.event_bus.publish_all(events)
            print(f"Published events: {events}")

            return ReturnBookResult(success=True)

        except Exception:
            self.tx.rollback()
            raise
