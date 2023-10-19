from uuid import UUID

from pydantic import BaseModel, PositiveInt


class Product(BaseModel):
    id: UUID
    category_id: UUID
    brand_id: UUID
    name: str
    description: str
    clicks: PositiveInt
