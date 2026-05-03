from app.domain.entities.reservation import Reservation
from abc import ABC, abstractmethod

class ReservationRepository:
    def save(self, reservation: Reservation) -> None:
        raise NotImplementedError

    def has_active_reservation(self, user_id: int, isbn: str) -> bool:
        raise NotImplementedError
    @abstractmethod
    def cancel(self, *, reservation_id: int) -> None:
        pass