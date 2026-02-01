# src/main.py
from src.core.use_cases.ingest_releases import IngestReleases
from src.core.use_cases.process_releases import ProcessReleases
from src.infrastructure.adapters.supabase_repository import SupabseRepository
from src.infrastructure.adapters.local_storage import LocalStorage
from src.infrastructure.adapters.nca_scraper import NCAScraper
import logging
import sys

from src.infrastructure.adapters.pd_data_cleaner import PdDataCleaner
from src.infrastructure.adapters.pdf_parser import PDFParser
from src.infrastructure.constants import (ALLOCATION_COLUMNS,
                                          BASE_RAW_STORAGE_PATH,
                                          BASE_RELEASES_STORAGE_PATH, DB_BULK_SIZE,
                                          RECORD_COLUMNS,
                                          VALID_COLUMNS)
from src.infrastructure.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


def main():
    logger = logging.getLogger("main")
    logger.info("Initializing NCA Pipeline...")

    # init adapters
    logger.debug("Setting up adapters...")
    scraper = NCAScraper()
    storage = LocalStorage(base_raw_path=BASE_RAW_STORAGE_PATH,
                           base_releases_path=BASE_RELEASES_STORAGE_PATH)
    parser = PDFParser()
    data_cleaner = PdDataCleaner(allocation_comumns=ALLOCATION_COLUMNS,
                                 record_columns=RECORD_COLUMNS,
                                 valid_columns=VALID_COLUMNS)
    repository = SupabseRepository(db_bulk_size=DB_BULK_SIZE)

    # init use cases
    ingest_job = IngestReleases(scraper=scraper,
                                storage=storage,
                                repository=repository,
                                base_raw_path=BASE_RAW_STORAGE_PATH,
                                base_releases_path=BASE_RELEASES_STORAGE_PATH
                                )
    process_job = ProcessReleases(storage=storage,
                                  parser=parser,
                                  data_cleaner=data_cleaner,
                                  repository=repository,
                                  base_raw_path=BASE_RAW_STORAGE_PATH,
                                  base_releases_path=BASE_RELEASES_STORAGE_PATH
                                  )

    # excute
    try:
        logger.info("Starting Ingestion Job...")
        releases = ingest_job.run(oldest_release_year=2024)
        logger.info("Job completed successfully.")
        logger.info("Starting Processing Job...")
        process_job.run(releases)
        logger.info("Job completed successfully.")
    except Exception as e:
        logger.critical(f"Job crashed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
