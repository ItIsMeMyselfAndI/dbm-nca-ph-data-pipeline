from typing import List, Protocol

from src.core.entities.nca_data import NCAData


class DataCleanerProvider(Protocol):
    def clean_raw_data(self,
                       raw_rows: List[List[str | None]],
                       release_id: str
                       ) -> NCAData:
        """clean list of raw data into list of record and list of allocation"""
        ...
