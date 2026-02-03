from src.core.entities.release_page_queue_body import ReleasePageQueueBody
from src.core.interfaces.queue import QueueProvider


class QeueuData:
    def __init__(self, queue: QueueProvider):
        self.queue = queue
        pass

    def run(self, data: ReleasePageQueueBody):
        self.queue.send_data(data)
