from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .reply import Reply


class Review(BaseModel):
    id: int
    product_id: int
    review: str
    rating: int
    posted_on: datetime


class ReviewUI(Review):
    replies: list[Reply] | None = None
