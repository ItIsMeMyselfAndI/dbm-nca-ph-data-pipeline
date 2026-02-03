from typing import Protocol

from src.core.entities.release_page_queue_body import ReleasePageQueueBody


class QueueProvider(Protocol):
    def send_data(self, data: ReleasePageQueueBody) -> None:
        """sends a batch of extracted rows to the queue"""
        ...
