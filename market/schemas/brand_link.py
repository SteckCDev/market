from uuid import UUID

from pydantic import BaseModel


class BrandLink(BaseModel):
    id: int
    brand_id: UUID
    caption: str
    link: str
