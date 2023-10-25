from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from market.database.utc_now import utc_now
from market.database import Base


class ReplyModel(Base):
    __tablename__ = "replies"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    reply: Mapped[str]
    posted_on: Mapped[datetime] = mapped_column(default=utc_now)
