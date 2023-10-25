from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from common.utc_now import utc_now
from . import Base


class Reply(Base):
    __tablename__ = "replies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_message_id: Mapped[int] = mapped_column(unique=True)
    message: Mapped[str]
    posted_on: Mapped[datetime] = mapped_column(default=utc_now)
