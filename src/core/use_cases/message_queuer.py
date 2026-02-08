import logging

from pydantic import BaseModel

from src.core.interfaces.queue import QueueProvider

logger = logging.getLogger(__name__)


class MessageQueuer:
    def __init__(self, queue: QueueProvider):
        self.queue = queue

    def run(self, message: BaseModel):
        try:
            self.queue.send(message)

        except Exception as e:
            logger.error(
                f"Failed to queue message: {message}\n" f">> {e}", exc_info=True
            )
            return
