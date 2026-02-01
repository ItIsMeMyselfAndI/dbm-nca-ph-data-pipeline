from copy import Error
from datetime import datetime
import logging
from typing import List
from core.interfaces.scraper import ScraperProvider
from core.interfaces.storage import StorageProvider
from src.core.entities.release import Release
from src.core.interfaces.repository import RepositoryProvider

logger = logging.getLogger(__name__)


class IngestReleases:
    def __init__(self,
                 scraper: ScraperProvider,
                 storage: StorageProvider,
                 repository: RepositoryProvider,
                 base_raw_path: str,
                 base_releases_path: str):
        self.scraper = scraper
        self.storage = storage
        self.repository = repository
        self.base_raw_path = base_raw_path
        self.base_releases_path = base_releases_path

    def run(self, oldest_release_year: int = 2024) -> List[Release]:
        logger.info(f"Starting ingestion for releases since {
                    oldest_release_year}")

        try:
            releases = self.scraper.get_releases(oldest_release_year)
        except Exception as e:
            logger.critical(f"Failed to fetch release list: {e}")
            raise e

        logger.info(f"Found {len(releases)} releases")

        filtered_releases = self._filter_new_or_updated_releases(releases)
        logger.info(
            f"Filtered only new/updated releases: "
            f"{len(filtered_releases)}/{len(releases)} remained")

        success_count = 0
        for release in filtered_releases:
            storage_path = f"{self.base_raw_path}/{release.filename}"
            try:
                self._ingest_release(storage_path, release)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to ingest {storage_path}: {e}")

        logger.info(f"Ingestion complete. Successfully synced {
                    success_count}/{len(filtered_releases)} files.")

        return filtered_releases

    def _ingest_release(self, storage_path: str, release: Release):
        data = self.scraper.download_release(release)
        if data.getbuffer().nbytes == 0:
            raise Error("Downloaded file is empty.")

        self.storage.save_file(storage_path, data)
        logger.info(f"Synced: {storage_path}")

    def _filter_new_or_updated_releases(self, releases: List[Release]):
        """
            - if the database has a last release and its year matches
                    the current year, it updates that release.
            - if the last release is from a previous year, it adds
                    all newer releases.
            - if the database is empty, it initializes it with all
                    available releases.
        """
        last_db_release = self.repository.get_last_release()
        curr_year = datetime.now().year
        filtered_releases = []

        if last_db_release:

            # leave only the latest release & del db last release
            if last_db_release.year == curr_year:
                latest_release = max(releases, key=lambda x: x.year)
                self.repository.delete_release(latest_release.id)
                filtered_releases.append(latest_release)

            # add all new/latest releases
            else:
                for release in releases:
                    if release.year > last_db_release.year:
                        filtered_releases.append(release)
                else:
                    logger.info("No new release found")

        # initialize db w/ all releases
        else:
            filtered_releases = releases

        return filtered_releases
