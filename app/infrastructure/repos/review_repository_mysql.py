from app.application.ports.review_repository import ReviewRepository
from app.domain.entities.review import Review


class ReviewRepositoryMySQL(ReviewRepository):

    def __init__(self, connection):
        self.connection = connection

    def get_by_isbn(self, isbn: str) -> list[Review]:
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                isbn,
                rating,
                comment,
                created_at
            FROM reviews
            WHERE isbn = %s
            ORDER BY created_at DESC
            """,
            (isbn,),
        )

        rows = cursor.fetchall()
        cursor.close()

        return [
            Review(
                id=row["id"],
                user_id=row["user_id"],
                isbn=row["isbn"],
                rating=row["rating"],
                comment=row["comment"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def create(self, review: Review) -> Review:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO reviews (user_id, isbn, rating, comment)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                rating = VALUES(rating),
                comment = VALUES(comment),
                created_at = CURRENT_TIMESTAMP
            """,
            (review.user_id, review.isbn, review.rating, review.comment),
        )

        self.connection.commit()
        cursor.close()

        return review
