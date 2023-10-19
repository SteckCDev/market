from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    category_id: int
    brand_id: UUID
    name: str
    description: str = None
    image_url: str = None
    clicks: int


class ProductUI(Product):
    brand_name: str
    rating: float | None = None
