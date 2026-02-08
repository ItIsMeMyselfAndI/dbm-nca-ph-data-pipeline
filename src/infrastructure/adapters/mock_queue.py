import logging

from pydantic import BaseModel

from src.core.interfaces.queue import QueueProvider

logger = logging.getLogger(__name__)


class MockQueue(QueueProvider):
    def __init__(self):
        pass

    def send(self, data: BaseModel) -> None:
        print({"message": data})
