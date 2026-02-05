import logging
from src.core.entities.raw_page_table import RawPageTable
from src.core.interfaces.data_cleaner import DataCleanerProvider

logger = logging.getLogger(__name__)


class CleanPageTable:
    def __init__(self, data_cleaner: DataCleanerProvider):
        self.data_cleaner = data_cleaner

    def run(self, raw_table: RawPageTable, release_id: str):
        cleaned_data = self.data_cleaner.clean_raw_data(raw_table.rows,
                                                        release_id)
        return cleaned_data
