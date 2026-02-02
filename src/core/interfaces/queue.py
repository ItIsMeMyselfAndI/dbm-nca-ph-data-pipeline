from typing import Protocol

from src.core.entities.nca_raw_table import NCARawTable


class QueueProvider(Protocol):
    def send_batch(self, data: NCARawTable) -> None:
        """sends a batch of extracted rows to the queue"""
        ...
