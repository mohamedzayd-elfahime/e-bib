# app/application/use_cases/reserve_book.py

from datetime import datetime
from app.domain.entities.reservation import Reservation, ReservationStatus
from app.application.dto.reserve_book import ReserveBookCommand


class ReserveBookResult:
    def __init__(self, success: bool, reason: str | None = None):
        self.success = success
        self.reason = reason


class ReserveBookUseCase:
    def __init__(
        self,
        reservation_repository,
        reservation_policy,
        transaction_manager,
    ):
        self.reservation_repository = reservation_repository
        self.reservation_policy = reservation_policy
        self.tx = transaction_manager

    def execute(self, command: ReserveBookCommand) -> ReserveBookResult:
        decision = self.reservation_policy.can_reserve(
            command.user_id,
            command.isbn,
        )

        if not decision.allowed:
            return ReserveBookResult(
                success=False,
                reason=decision.reason,
            )

        self.tx.begin()
        try:
            reservation = Reservation(
                id=None,
                user_id=command.user_id,
                isbn=command.isbn,
                status=ReservationStatus.ACTIVE,
                created_at=datetime.utcnow(),
            )

            self.reservation_repository.save(reservation)

            self.tx.commit()
            return ReserveBookResult(success=True)

        except Exception:
            self.tx.rollback()
            raise
