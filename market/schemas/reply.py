from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Reply(BaseModel):
    id: UUID
    review_id: UUID
    reply: str
    posted_on: datetime
