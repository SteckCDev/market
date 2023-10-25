from sqlalchemy.orm import Mapped, mapped_column

from market.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
