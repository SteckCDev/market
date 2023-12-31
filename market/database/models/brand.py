from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from market.database import Base


class BrandModel(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    access_code: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
