from typing import List, Protocol
from src.core.entities.record import Record
from src.core.entities.allocation import Allocation
from src.core.entities.release import Release


class RepositoryProvider(Protocol):
    def get_last_release(self) -> Release | None:
        """get release with an id"""
        ...

    def upsert_release(self, release: Release) -> None:
        """insert/upsert new release"""
        ...

    def delete_release(self, id: str) -> None:
        """delete release with an id"""
        ...

    def bulk_upsert_records(self, records: List[Record]) -> None:
        """insert/update multiple new records"""
        ...

    def bulk_insert_allocations(self, allocations: List[Allocation]) -> None:
        """insert multiple new allocations"""
        ...
