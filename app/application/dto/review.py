from pydantic import BaseModel, Field


class CreateReview(BaseModel):
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating between 1 and 5"
    )
    comment: str = Field(
        min_length=1,
        description="Review comment (non-empty)"
    )
