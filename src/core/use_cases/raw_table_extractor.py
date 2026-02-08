import logging
from typing import List

from src.core.entities.release_batch import ReleaseBatch
from src.core.interfaces.parser import ParserProvider
from src.core.interfaces.storage import StorageProvider

logger = logging.getLogger(__name__)


class RawTableExtractor:
    def __init__(self, storage: StorageProvider, parser: ParserProvider):
        self.storage = storage
        self.parser = parser
        self.raw_data = None

    def run(self, batch: ReleaseBatch) -> List[List[str | None]] | None:
        try:
            self.raw_data = self.storage.load_file(batch.release.filename)
            extracted_tables = []
            for i in range(batch.start_page_num, batch.end_page_num + 1):
                table = self._extract_tables(batch.release.filename, i)
                if not table:
                    continue
                extracted_tables.extend(table)

            return extracted_tables

        except Exception as e:
            logger.error(
                f"Failed to extract tables from {batch.release.filename} "
                f"pages {batch.start_page_num}-{batch.end_page_num}: {e}",
                exc_info=True,
            )
            return None

    def _extract_tables(
        self, filename: str, page_num: int
    ) -> List[List[str | None]] | None:
        logger.debug(f"Extracting raw data from {filename}: " f"page-{page_num}...")

        if not self.raw_data:
            logger.error(f"No raw data loaded for {filename} " f"page-{page_num}")
            return None

        rows = self.parser.extract_table_by_page_num(self.raw_data, page_num)

        if len(rows) == 0:
            logger.warning(f"No tables extracted from {filename} " f"page-{page_num}")
            return None

        logger.debug(f"Extracted {len(rows)} rows from {filename} " f"page-{page_num}")
        return rows
