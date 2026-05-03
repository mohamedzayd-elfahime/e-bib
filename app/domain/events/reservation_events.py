# domain/events/reservation_events.py
from domain.events.base import DomainEvent


class ReservationCreated(DomainEvent):
    def __init__(self, reservation_id: int, user_id: int, isbn: str):
        super().__init__()
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.isbn = isbn


class ReservationExpired(DomainEvent):
    def __init__(self, reservation_id: int, user_id: int):
        super().__init__()
        self.reservation_id = reservation_id
        self.user_id = user_id


class ReservationFulfilled(DomainEvent):
    def __init__(self, reservation_id: int, user_id: int, book_copy_id: int):
        super().__init__()
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.book_copy_id = book_copy_id
