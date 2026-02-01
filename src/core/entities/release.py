from pydantic import BaseModel


class Release(BaseModel):
    id: str
    title: str
    url: str
    filename: str
    year: int
