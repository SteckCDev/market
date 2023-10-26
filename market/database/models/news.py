from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from market.database.utc_now import utc_now
from market.database import Base


class NewsModel(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_message_id: Mapped[int] = mapped_column(unique=True)
    message: Mapped[str]
    posted_on: Mapped[datetime] = mapped_column(default=utc_now)
