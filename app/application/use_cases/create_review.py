from app.application.ports.review_repository import ReviewRepository
from app.domain.entities.review import Review
from app.application.dto.review import CreateReview


class CreateReviewUseCase:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def execute(
        self,
        *,
        user_id: int,
        isbn: str,
        dto: CreateReview
    ) -> Review:
        """
        Create a review for a book by a user.
        Assumes (user_id, isbn) uniqueness is enforced at DB level.
        """

        review = Review(
            id=None,
            user_id=user_id,
            isbn=isbn,
            rating=dto.rating,
            comment=dto.comment,
            created_at=None,  # DB responsibility
        )

        return self.review_repository.create(review)
