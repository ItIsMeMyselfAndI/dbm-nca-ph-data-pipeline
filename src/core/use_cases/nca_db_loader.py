import logging
from src.core.entities.nca_data import NCAData
from src.core.entities.release import Release
from src.core.interfaces.data_cleaner import DataCleanerProvider
from src.core.interfaces.repository import RepositoryProvider

logger = logging.getLogger(__name__)


class NCADBLoader:
    def __init__(
        self, repository: RepositoryProvider, data_cleaner: DataCleanerProvider
    ):
        self.data_cleaner = data_cleaner
        self.repository = repository

    def run(self, release: Release, nca_data: NCAData, batch_num: int):
        try:
            if len(nca_data.records) == 0:
                logger.warning(
                    f"No records to load for {release.filename} " f"(page-{batch_num})"
                )
                return
            self.repository.bulk_upsert_records(nca_data.records)

            if len(nca_data.allocations) == 0:
                logger.warning(
                    f"No allocations to load for {release.filename} "
                    f"(page-{batch_num})"
                )
                return
            self.repository.bulk_insert_allocations(nca_data.allocations)

            logger.debug(
                f"Loaded {len(nca_data.records)} records and "
                f"{len(nca_data.allocations)} allocations for "
                f"{release.filename} batch-{batch_num}"
            )

        except Exception as e:
            logger.error(
                f"Failed to load data for {release.filename} "
                f"batch-{batch_num}: {e}",
                exc_info=True,
            )
