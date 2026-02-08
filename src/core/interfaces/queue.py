from typing import Protocol

from pydantic import BaseModel


class QueueProvider(Protocol):
    def send(self, data: BaseModel) -> None:
        """sends a batch of extracted rows to the queue"""
        ...
