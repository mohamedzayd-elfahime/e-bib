from fastapi import APIRouter
from app.infrastructure.db.session.mysql import get_connection
from app.application.use_cases.get_book_reviews import GetBookReviews
from app.infrastructure.repos.review_repository_mysql import ReviewRepositoryMySQL
from fastapi import Depends, HTTPException, status
from app.application.use_cases.create_review import CreateReviewUseCase
from app.application.dto.review import CreateReview
from app.presentation.api.dependencies import get_current_user_id


router = APIRouter()


@router.get("/api/books/{isbn}/reviews")
def get_book_reviews(isbn: str):
    uc = GetBookReviews(
        review_repo=ReviewRepositoryMySQL(get_connection())
    )
    return uc.execute(isbn=isbn)


@router.post("/api/books/{isbn}/reviews", status_code=status.HTTP_201_CREATED)
def post_review(
    isbn: str,
    payload: CreateReview,
    user_id: int = Depends(get_current_user_id),
    connection=Depends(get_connection),
):
    repo = ReviewRepositoryMySQL(connection)
    use_case = CreateReviewUseCase(repo)

    use_case.execute(
        user_id=user_id,
        isbn=isbn,
        dto=payload
    )

    return {"status": "saved"}