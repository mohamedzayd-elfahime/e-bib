from app.application.ports.reservation_repository import ReservationRepository
from app.domain.services.reservation_policy import (
    ReservationCancellationService,
)

class CancelReservationUseCase:

    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, *, user_id: int, isbn: str) -> None:
        has_active = self.reservation_repository.has_active_reservation(
            user_id, isbn
        )

        if not ReservationCancellationService.can_cancel(has_active):
            raise ValueError("NO_ACTIVE_RESERVATION")

        self.reservation_repository.cancel_by_user_and_isbn(
            user_id=user_id,
            isbn=isbn,
        )
