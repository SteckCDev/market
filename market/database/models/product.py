from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from market.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[UUID] = mapped_column(ForeignKey("brands.id"))
    name: Mapped[str]
    description: Mapped[str]
    image_path: Mapped[str] = mapped_column(nullable=True)
    clicks: Mapped[int] = mapped_column(default=0)
