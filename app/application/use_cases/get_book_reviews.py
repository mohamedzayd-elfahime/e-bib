from app.application.ports.review_repository import ReviewRepository

class GetBookReviews:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    def execute(self, *, isbn: str):
        reviews = self.review_repo.get_by_isbn(isbn)

        total = len(reviews)
        avg = (
            sum(r.rating for r in reviews) / total
            if total > 0 else 0
        )

        breakdown = {i: 0 for i in range(1, 6)}
        for r in reviews:
            breakdown[r.rating] += 1

        return {
            "average": round(avg, 1),
            "total": total,
            "breakdown": breakdown,
            "reviews": reviews,
        }
