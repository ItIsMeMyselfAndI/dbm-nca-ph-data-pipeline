import logging
from src.core.entities.nca_raw_table import NCARawTable
from src.core.interfaces.data_cleaner import DataCleanerProvider
from src.core.interfaces.repository import RepositoryProvider

logger = logging.getLogger(__name__)


class LoadRelease:
    def __init__(self,
                 repository: RepositoryProvider,
                 data_cleaner: DataCleanerProvider):
        self.data_cleaner = data_cleaner
        self.repository = repository

    def run(self, nca_table: NCARawTable):
        try:
            logger.debug(f"Loading {nca_table.release.filename} data to db: "
                         f"batch-{nca_table.batch_number}...")
            self.repository.upsert_release(nca_table.release)

            nca_data = self.data_cleaner.clean_raw_data(nca_table.rows,
                                                        nca_table.release.id)

            self.repository.bulk_upsert_records(nca_data.records)
            self.repository.bulk_insert_allocations(nca_data.allocations)
            logger.debug(f"Loaded {nca_table.release.filename} data to db: "
                         f"batch-{nca_table.batch_number}")

        except Exception as e:
            logger.warning(f"Skipped loading {nca_table.release.filename} "
                           f"(batch-{nca_table.batch_number}): {e}")
