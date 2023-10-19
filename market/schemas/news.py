from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: UUID
    tg_message_id: int
    body: str
    posted_on: datetime
