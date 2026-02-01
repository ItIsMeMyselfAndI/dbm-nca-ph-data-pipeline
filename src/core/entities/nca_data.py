from typing import List
from pydantic import BaseModel

from src.core.entities.allocation import Allocation
from src.core.entities.record import Record


class NCAData(BaseModel):
    records: List[Record]
    allocations: List[Allocation]
