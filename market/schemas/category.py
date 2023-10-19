from uuid import UUID

from pydantic import BaseModel, PositiveInt


class Category(BaseModel):
    id: int
    name: str


class CategoryUI(Category):
    products_count: PositiveInt

    @property
    def link(self) -> str:
        return f"/category/{self.id}"
