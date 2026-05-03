from typing import Optional

from app.application.ports.book_copy_repository import BookCopyRepository
from app.domain.entities.book_copy import BookCopy, BookCopyStatus


class BookCopyRepositoryMySQL(BookCopyRepository):
    """
    MySQL repository for BookCopy.
    Uses a shared connection managed outside (TransactionManager / session).
    """

    def __init__(self, connection):
        self.connection = connection

    def find_available_for_update(self, isbn: str) -> Optional[BookCopy]:
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, isbn, status
            FROM book_copies
            WHERE isbn = %s
              AND status = %s
            LIMIT 1
            FOR UPDATE
            """,
            (isbn, BookCopyStatus.AVAILABLE.value),
        )

        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return BookCopy(
            id=row["id"],
            isbn=row["isbn"],
            status=BookCopyStatus(row["status"]),
        )

    def save(self, book_copy: BookCopy) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE book_copies
            SET status = %s
            WHERE id = %s
            """,
            (book_copy.status.value, book_copy.id),
        )

        cursor.close()

    def count_available(self, isbn: str) -> int:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM book_copies
            WHERE isbn = %s
              AND status = %s
            """,
            (isbn, BookCopyStatus.AVAILABLE.value),
        )

        (count,) = cursor.fetchone()
        cursor.close()

        return count
    def find_by_id(self, book_copy_id: int) -> Optional[BookCopy]:
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, isbn, status
            FROM book_copies
            WHERE id = %s
            """,
            (book_copy_id,),
        )

        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return BookCopy(
            id=row["id"],
            isbn=row["isbn"],
            status=BookCopyStatus(row["status"]),
        )
