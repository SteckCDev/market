from pydantic import BaseModel


class Ad(BaseModel):
    page_id: int
    split: bool
    link1: str | None
    image1_path: str | None
    link2: str | None
    image2_path: str | None
    enabled: bool


class AdUI(Ad):
    name: str
