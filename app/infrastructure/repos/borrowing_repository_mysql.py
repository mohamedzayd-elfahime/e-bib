from typing import Optional

from app.application.ports.borrowing_repository import BorrowingRepository
from app.domain.entities.borrowing import Borrowing, BorrowingStatus


class BorrowingRepositoryMySQL(BorrowingRepository):
    """
    MySQL repository for Borrowing.
    Uses a shared connection managed outside (TransactionManager / session).
    """

    def __init__(self, connection):
        self.connection = connection

    def save(self, borrowing: Borrowing) -> None:
        cursor = self.connection.cursor()

        if borrowing.id is None:
            cursor.execute(
                """
                INSERT INTO borrowings (
                    user_id,
                    book_copy_id,
                    status,
                    borrowed_at,
                    due_at,
                    returned_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    borrowing.user_id,
                    borrowing.book_copy_id,
                    borrowing.status.value,
                    borrowing.borrowed_at,
                    borrowing.due_at,
                    borrowing.returned_at,
                ),
            )
            borrowing.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE borrowings
                SET status = %s,
                    returned_at = %s
                WHERE id = %s
                """,
                (
                    borrowing.status.value,
                    borrowing.returned_at,
                    borrowing.id,
                ),
            )

        cursor.close()

    def has_active_borrowing(self, user_id: int) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM borrowings
            WHERE user_id = %s
              AND status = %s
            LIMIT 1
            """,
            (user_id, BorrowingStatus.ACTIVE.value),
        )

        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def has_overdue_borrowing(self, user_id: int) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM borrowings
            WHERE user_id = %s
              AND status = %s
            LIMIT 1
            """,
            (user_id, BorrowingStatus.OVERDUE.value),
        )

        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def find_by_id(self, borrowing_id: int) -> Optional[Borrowing]:
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                book_copy_id,
                status,
                borrowed_at,
                due_at,
                returned_at
            FROM borrowings
            WHERE id = %s
            """,
            (borrowing_id,),
        )

        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return Borrowing(
            id=row["id"],
            user_id=row["user_id"],
            book_copy_id=row["book_copy_id"],
            status=BorrowingStatus(row["status"]),
            borrowed_at=row["borrowed_at"],
            due_at=row["due_at"],
            returned_at=row["returned_at"],
        )
    def count_active_borrowings(self, user_id: int) -> int:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM borrowings
            WHERE user_id = %s
            AND status in ('active','pending')
            """,
            (user_id,),
        )

        (count,) = cursor.fetchone()
        cursor.close()

        return count
    def has_active_borrowing_for_isbn(self, user_id: int, isbn: str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM borrowings b
            JOIN book_copies bc ON bc.id = b.book_copy_id
            WHERE b.user_id = %s
            AND bc.isbn = %s
            AND b.status IN ('active', 'overdue')
            LIMIT 1
            """,
            (user_id, isbn),
        )

        result = cursor.fetchone()
        cursor.close()

        return result is not None

    def has_overdue_borrowing_for_isbn(self, user_id: int, isbn: str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM borrowings b
            JOIN book_copies bc ON bc.id = b.book_copy_id
            WHERE b.user_id = %s
            AND bc.isbn = %s
            AND b.status = %s
            LIMIT 1
            """,
            (user_id, isbn ,"overdue"),
        )

        result = cursor.fetchone()
        cursor.close()

        return result is not None