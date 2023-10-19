from pydantic import BaseModel


class Ad(BaseModel):
    page_uri: str
    split: bool
    image1_url: str
    image2_url: str
