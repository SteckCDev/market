from datetime import datetime

from pydantic import BaseModel, Field

from .reply import Reply


class Review(BaseModel):
    id: int
    product_id: int
    review: str = Field(..., min_length=4, max_length=1024)
    rating: int = Field(..., ge=1, le=5)
    posted_on: datetime


class ReviewUI(Review):
    replies: list[Reply] | None = None

    @property
    def posted_on_human_friendly(self):
        return self.posted_on.strftime("%d.%m.%Y %H:%M")
