from uuid import UUID

from pydantic import BaseModel, PositiveInt


class Category(BaseModel):
    id: UUID
    name: str


class CategoryUI(Category):
    products_count: PositiveInt = 0
