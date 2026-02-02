from typing import List
from pydantic import BaseModel

from src.core.entities.release import Release


class NCARawTable(BaseModel):
    release: Release
    rows: List[List[str | None]]
    batch_number: int
