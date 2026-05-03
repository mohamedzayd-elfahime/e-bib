from datetime import datetime

from app.domain.events.borrowing_events import BorrowingReturned
from app.domain.entities.notification import Notification, NotificationType
from app.infrastructure.db.session.mysql import get_connection
from app.infrastructure.repos.notification_repository_mysql import NotificationRepositoryMySQL
from app.presentation.ws.connection_manager import manager


def on_borrowing_returned(event: BorrowingReturned) -> None:
    """
    Event handler SYNC
    """

    connection = get_connection()
    try:
        repo = NotificationRepositoryMySQL(connection)

        notification = Notification(
            id=None,
            user_id=event.user_id,
            type=NotificationType.BORROWING_RETURNED,
            message="Votre livre a été rendu avec succès.",
            is_read=False,
            created_at=datetime.utcnow(),
        )

        repo.save(notification)

        #  PAYLOAD OBLIGATOIRE
        manager.send_to_user(
            event.user_id,
            {
                "type": "notification",
                "data": {
                    "notification_type": notification.type.value,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat(),
                },
            },
        )

        print(
            "[NOTIFICATION] Livre rendu | "
            f"user_id={event.user_id}, borrowing_id={event.borrowing_id}"
        )

    finally:
        connection.close()
