from app.application.ports.favorite_repository import FavoriteRepository
from app.infrastructure.db.session.mysql import get_connection

class MySQLFavoriteRepository(FavoriteRepository):

    def get_favorite_isbns(self, user_id: int) -> set[str]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT isbn FROM favorites WHERE user_id=%s",
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return {row[0] for row in rows}


    def exists(self, user_id: int, isbn: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM favorites WHERE user_id=%s AND isbn=%s LIMIT 1",
            (user_id, isbn)
        )
        found = cur.fetchone() is not None
        cur.close()
        conn.close()
        return found

    def add(self, user_id: int, isbn: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO favorites (user_id, isbn) VALUES (%s, %s)",
            (user_id, isbn)
        )
        conn.commit()
        cur.close()
        conn.close()

    def remove(self, user_id: int, isbn: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM favorites WHERE user_id=%s AND isbn=%s",
            (user_id, isbn)
        )
        conn.commit()
        cur.close()
        conn.close()
