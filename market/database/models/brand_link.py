from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from market.database import Base


class BrandLink(Base):
    __tablename__ = "brand_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[UUID] = mapped_column(ForeignKey("brands.id"))
    caption: Mapped[str]
    link: Mapped[str]
