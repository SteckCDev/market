from pydantic import BaseModel


class Product(BaseModel):
    id: int
    category_id: int
    brand_id: int
    name: str
    description: str = None
    image_path: str | None = None
    clicks: int


class ProductUI(Product):
    brand_name: str
    rating: float | None = None

    @property
    def link(self) -> str:
        return f"/product/{self.id}"
