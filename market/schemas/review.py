from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Review(BaseModel):
    id: int
    product_id: UUID
    review: str
    rating: int
    posted_on: datetime
