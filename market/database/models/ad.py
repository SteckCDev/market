from sqlalchemy.orm import Mapped, mapped_column

from market.database import Base


class AdModel(Base):
    __tablename__ = "ads"

    page_id: Mapped[int] = mapped_column(primary_key=True)
    split: Mapped[bool] = mapped_column(default=False)
    link1: Mapped[str] = mapped_column(nullable=True)
    image1_path: Mapped[str] = mapped_column(nullable=True)
    link2: Mapped[str] = mapped_column(nullable=True)
    image2_path: Mapped[str] = mapped_column(nullable=True)
    enabled: Mapped[bool] = mapped_column(default=False)
