from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Review(BaseModel):
    id: UUID
    product_id: UUID
    review: str
    posted_on: datetime
