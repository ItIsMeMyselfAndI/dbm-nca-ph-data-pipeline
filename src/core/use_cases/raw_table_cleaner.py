import logging
from typing import List
from src.core.entities.nca_data import NCAData
from src.core.interfaces.data_cleaner import DataCleanerProvider

logger = logging.getLogger(__name__)


class RawTableCleaner:
    def __init__(self, data_cleaner: DataCleanerProvider):
        self.data_cleaner = data_cleaner

    def run(self, raw_table: List[List[str | None]], release_id: str) -> NCAData:
        nca_data = self.data_cleaner.clean_raw_data(raw_table, release_id)
        return nca_data
