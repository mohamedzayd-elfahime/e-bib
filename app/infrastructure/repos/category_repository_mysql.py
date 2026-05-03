from app.infrastructure.db.session.mysql import get_connection
from app.application.read_models.category import CategoryFilterItem


class CategoryRepositoryMySQL:

    def list_with_book_count(self) -> list[CategoryFilterItem]:
        query = """
        SELECT
            c.id,
            c.name,
            COUNT(b.isbn) AS total_books
        FROM categories c
        LEFT JOIN books b ON b.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY c.name
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            CategoryFilterItem(
                id=row["id"],
                name=row["name"],
                total_books=row["total_books"],
            )
            for row in rows
        ]
