from typing import List
from src.core.entities.release import Release
from src.core.entities.release_batch import ReleaseBatch


class ReleaseBatcher:
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def run(self, release: Release) -> List[ReleaseBatch]:
        batches = []
        for start in range(1, release.page_count + 1, self.batch_size):
            end = min(start + self.batch_size - 1, release.page_count)
            batch = ReleaseBatch(
                batch_num=(start - 1) // self.batch_size + 1,
                release=release,
                start_page_num=start,
                end_page_num=end,
            )
            batches.append(batch)
        return batches
