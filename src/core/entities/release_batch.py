from pydantic import BaseModel

from src.core.entities.release import Release


class ReleaseBatch(BaseModel):
    batch_num: int
    release: Release
    start_page_num: int
    end_page_num: int
