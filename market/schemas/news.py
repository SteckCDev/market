from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: int
    tg_message_id: int
    body: str
    posted_on: datetime
