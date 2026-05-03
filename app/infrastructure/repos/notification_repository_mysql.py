from app.domain.entities.notification import Notification


class NotificationRepositoryMySQL:
    def __init__(self, connection):
        self.connection = connection

    # -----------------------
    # CREATE
    # -----------------------
    def save(self, notification: Notification) -> None:
        cursor = self.connection.cursor()

        query = """
            INSERT INTO notifications (user_id, type, message, is_read, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                notification.user_id,
                notification.type.value,
                notification.message,
                notification.is_read,
                notification.created_at,
            )
        )

        self.connection.commit()
        cursor.close()

    # -----------------------
    # READ ALL BY USER
    # -----------------------
    def get_by_user(self, user_id: int) -> list[Notification]:
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, user_id, type, message, is_read, created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()
        cursor.close()

        return [
            Notification(
                id=row["id"],
                user_id=row["user_id"],
                type=row["type"],  # adapte si enum
                message=row["message"],
                is_read=row["is_read"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    # -----------------------
    # MARK ONE AS READ
    # -----------------------
    def mark_as_read(self, notification_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE notifications
            SET is_read = TRUE
            WHERE id = %s
        """, (notification_id,))

        self.connection.commit()
        cursor.close()

    # -----------------------
    # MARK ALL AS READ
    # -----------------------
    def mark_all_as_read(self, user_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE notifications
            SET is_read = TRUE
            WHERE user_id = %s
              AND is_read = FALSE
        """, (user_id,))

        self.connection.commit()
        cursor.close()

    # -----------------------
    # COUNT UNREAD
    # -----------------------
    def count_unread(self, user_id: int) -> int:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM notifications
            WHERE user_id = %s
              AND is_read = FALSE
        """, (user_id,))

        (count,) = cursor.fetchone()
        cursor.close()

        return count
