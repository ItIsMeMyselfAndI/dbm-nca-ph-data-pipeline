import logging
from tqdm import tqdm
from typing import List, Tuple
from src.core.entities.release import Release
from src.core.interfaces.data_cleaner import DataCleanerProvider
from src.core.interfaces.parser import ParserProvider
from src.core.interfaces.repository import RepositoryProvider
from src.core.interfaces.storage import StorageProvider

logger = logging.getLogger(__name__)


class ProcessReleases:
    def __init__(self,
                 storage: StorageProvider,
                 parser: ParserProvider,
                 repository: RepositoryProvider,
                 data_cleaner: DataCleanerProvider,
                 base_raw_path: str,
                 base_releases_path: str):
        self.storage = storage
        self.parser = parser
        self.data_cleaner = data_cleaner
        self.repository = repository
        self.base_raw_path = base_raw_path
        self.base_releases_path = base_releases_path

    def run(self, releases: List[Release]):
        if len(releases) == 0:
            logger.warning("Skipping processes: No new/updated release found.")
            return

        for release in releases:
            self._process_release(release)

    def _process_release(self, release: Release):
        try:
            logger.info(
                f"Splitting {release.filename} into single-pages...")
            file_count, splitting_success_count = \
                self.__split_release_pages(release)
            logger.info(
                f"Splitting complete for {release.filename}. "
                f"Saved {splitting_success_count}/{file_count} files.")

        except Exception as e:
            logger.error(f"Failed to split pages of {
                         release.filename}: {e}")
            return

        try:
            logger.info(f"Loading {release.filename} data to db...")
            loading_success_count = self.__load_data_to_db(
                file_count, release)
            logger.info(
                f"Loading complete for {release.filename}. "
                f"Loaded {loading_success_count}/{splitting_success_count} files.")

        except Exception as e:
            logger.error(f"Failed to load pages of {release.filename}: {e}")
            return

    def __split_release_pages(self, release: Release) -> Tuple[int, int]:
        raw_storage_path = f"{self.base_raw_path}/{release.filename}"
        raw_data = self.storage.load_file(raw_storage_path)
        pages_list = self.parser.split_pages(raw_data)

        success_count = 0
        for i, page_buffer in tqdm(enumerate(pages_list),
                                   desc="Saved",
                                   unit="file",
                                   leave=False):
            page_filename = f"{release.filename.split(".")[0]}/page_{i}.pdf"
            page_storage_path = f"{self.base_releases_path}/{page_filename}"

            try:
                if page_buffer.getbuffer().nbytes == 0:
                    logger.warning(
                        f"Skipping {page_storage_path}: Empty buffer.")
                    continue

                self.storage.save_file(page_storage_path, page_buffer)

                logger.debug(f"Saved: {page_storage_path}")
                success_count += 1

            except Exception as e:
                logger.error(f"Failed to save {page_storage_path}: {e}")

        return len(pages_list), success_count

    def __load_data_to_db(self, file_count: int, release: Release) -> int:
        self.repository.upsert_release(release)

        success_count = 0
        for i in tqdm(range(file_count),
                      desc="Loaded",
                      unit="file",
                      leave=False):
            filename = f"{release.filename.split(".")[0]}/page_{i}.pdf"
            raw_release_page_path = f"{self.base_releases_path}/{filename}"

            try:
                data = self.storage.load_file(raw_release_page_path)
                raw_rows = self.parser.extract_raw_table_rows(data, i)
                nca_data = self.data_cleaner.clean_raw_data(raw_rows,
                                                            release.id)
                self.repository.bulk_upsert_records(nca_data.records)
                self.repository.bulk_insert_allocations(nca_data.allocations)
                logger.debug(f"Loaded to db: {raw_release_page_path}")
                success_count += 1

            except Exception as e:
                logger.warning(f"Skipped loading {
                             raw_release_page_path} to db: {e}")
        return success_count
