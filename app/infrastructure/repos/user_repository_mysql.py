from app.application.ports.UserRepository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.db.session.mysql import get_connection


class MySQLUserRepository(UserRepository):
    def get_by_email(self, email: str) -> User | None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, email, password_hash, is_active FROM users WHERE email=%s LIMIT 1",
            (email,),
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            is_active=row["is_active"],
        )
    def create_google_user(self, email: str, is_active: bool):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (email, password_hash, is_active)
            VALUES (%s, %s, %s)
            """,
            (email, None, is_active),
        )

        conn.commit()

        user_id = cursor.lastrowid

        return User(
            id=user_id,
            email=email,
            password_hash=None,
            is_active=is_active,
        )


