from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    access_code: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
