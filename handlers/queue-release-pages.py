import json
import re
import urllib.parse
import logging
from src.logging_config import setup_logging

from src.core.entities.release_page_queue_body import ReleasePageQueueBody
from src.core.use_cases.extract_page_table import ExtractPageTable
from src.core.use_cases.queue_data import QeueuData
from src.infrastructure.adapters.pdf_parser import PDFParser
from src.infrastructure.adapters.s3_storage import S3Storage
from src.infrastructure.adapters.sqs_queue import SQSQueue
from src.infrastructure.adapters.supabase_repository import SupabaseRepository
from src.infrastructure.config import settings
from src.infrastructure.constants import BASE_STORAGE_PATH, DB_BULK_SIZE

# logger
setup_logging()
logger = logging.getLogger(__name__)

# adapters
storage = S3Storage(bucket_name=settings.AWS_S3_BUCKET_NAME,
                    base_storage_path=BASE_STORAGE_PATH)
parser = PDFParser()
queue = SQSQueue(queue_url=settings.AWS_SQS_QUEUE_URL)
repository = SupabaseRepository(db_bulk_size=DB_BULK_SIZE)

# use cases
extract_job = ExtractPageTable(storage=storage, parser=parser)
queue_job = QeueuData(queue=queue)


def lambda_function(event, context):
    logger.info(f"START Batch processing. "
                f"Records: {len(event['Records'])} | "
                f"RequestID: {context.aws_request_id}")

    for sqs_record in event['Records']:
        try:
            body = json.loads(sqs_record['body'])
            payload = body['Records'][0]
            raw_key = payload['s3']['object']['key']
            filename = urllib.parse.unquote_plus(raw_key)
            logger.debug(f"Processing filename: {filename}")

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"Failed to parse SQS/S3 "
                         f"body structure: {e}", exc_info=True)
            continue

        release_id = _create_release_id(filename)

        if not release_id:
            logger.warning(
                f"Skipping file - invalid filename format: {filename}")
            continue

        db_release = repository.get_release(release_id)

        if not db_release:
            logger.warning(f"Skipping file - Release ID "
                           f"{release_id} not found in database")
            continue

        logger.info(
            f"Queueing {db_release.page_count} pages for release: {release_id}")

        for i in range(db_release.page_count):
            try:
                message_body = ReleasePageQueueBody(
                    release=db_release.model_dump(),  # pyright: ignore
                    page_num=i,
                )
                queue_job.run(message_body)

            except Exception as e:
                logger.error(f"Failed to queue page {i} "
                             f"for release {release_id}: {e}",
                             exc_info=True)
                continue

            # <test>
            if i == 5:
                logger.info("Hit test limit of 5 pages. Breaking loop.")
                break
            # </test>

    logger.info("END Batch processing")


def _create_release_id(filename: str) -> str | None:
    match = re.search(r'(\d{4})', filename)
    if not match:
        return None
    year = int(match.group(1))
    return f"id_{year}"
