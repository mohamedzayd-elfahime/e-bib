# domain/events/borrowing_events.py
from app.domain.events.base import DomainEvent


class BorrowingCreated(DomainEvent):
    def __init__(self, borrowing_id: int, user_id: int, book_copy_id: int):
        super().__init__()
        self.borrowing_id = borrowing_id
        self.user_id = user_id
        self.book_copy_id = book_copy_id


class BorrowingActivated(DomainEvent):
    def __init__(self, borrowing_id: int):
        super().__init__()
        self.borrowing_id = borrowing_id


class BorrowingPendingExpired(DomainEvent):
    def __init__(self, borrowing_id: int, user_id: int):
        super().__init__()
        self.borrowing_id = borrowing_id
        self.user_id = user_id


class BorrowingOverdue(DomainEvent):
    def __init__(self, borrowing_id: int, user_id: int):
        super().__init__()
        self.borrowing_id = borrowing_id
        self.user_id = user_id


class BorrowingReturned(DomainEvent):
    def __init__(self, borrowing_id: int, user_id: int, book_copy_id: int):
        super().__init__()
        self.borrowing_id = borrowing_id
        self.user_id = user_id
        self.book_copy_id = book_copy_id
