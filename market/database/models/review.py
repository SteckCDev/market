from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from market.database.utc_now import utc_now
from market.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    review: Mapped[str]
    rating: Mapped[int]
    posted_on: Mapped[datetime] = mapped_column(default=utc_now)
