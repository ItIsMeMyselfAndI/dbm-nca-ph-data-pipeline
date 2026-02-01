from pydantic import BaseModel


class MetaData(BaseModel):
    created_at: str
    modified_at: str
