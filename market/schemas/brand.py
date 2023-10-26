from uuid import UUID

from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    name: str
    links: str
    access_code: UUID
