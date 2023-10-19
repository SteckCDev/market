from pydantic import BaseModel


class Dummy(BaseModel):
    page_name: str
    data: list = None
