from datetime import datetime

from pydantic import BaseModel


class Reply(BaseModel):
    id: int
    review_id: int
    reply: str
    posted_on: datetime
