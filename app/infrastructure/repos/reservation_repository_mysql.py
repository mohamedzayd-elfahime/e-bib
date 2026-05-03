from app.application.ports.reservation_repository import ReservationRepository
from app.domain.entities.reservation import Reservation


class ReservationRepositoryMySQL(ReservationRepository):
    def __init__(self, connection):
        self.connection = connection

    def save(self, reservation: Reservation) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO reservations (user_id, isbn, status, reserved_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                reservation.user_id,
                reservation.isbn,
                reservation.status,
                reservation.created_at,
            ),
        )
        cursor.close()

    def has_active_reservation(self, user_id: int, isbn: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM reservations
            WHERE user_id = %s
              AND isbn = %s
              AND status = 'active'
            LIMIT 1
            """,
            (user_id, isbn),
        )
        row = cursor.fetchone()
        cursor.close()
        return row is not None
    def cancel_by_user_and_isbn(self, *, user_id: int, isbn: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE reservations
            SET status = 'cancelled'
            WHERE user_id = %s
            AND isbn = %s
            AND status = 'active'
            """,
            (user_id, isbn),
        )
        cursor.close()


