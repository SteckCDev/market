from pydantic import BaseModel


class BrandLink(BaseModel):
    id: int
    brand_id: int
    caption: str
    link: str
