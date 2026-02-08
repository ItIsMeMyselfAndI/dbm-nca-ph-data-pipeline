import json
import time
from datetime import timedelta
import logging
from src.logging_config import setup_logging

from src.core.entities.release import Release
from src.core.use_cases.message_queuer import MessageQueuer
from src.core.use_cases.release_batcher import ReleaseBatcher

from src.infrastructure.adapters.sqs_queue import SQSQueue
from src.infrastructure.config import settings
from src.infrastructure.constants import BATCH_SIZE

# <test>
BATCH_COUNT_TO_QUEUE = 1
# </test>


setup_logging()
logger = logging.getLogger(__name__)

# adapters
queue = SQSQueue(queue_url=settings.AWS_SQS_RELEASE_BATCH_QUEUE_URL)

# use cases
queuer_job = MessageQueuer(queue=queue)
batcher_job = ReleaseBatcher(batch_size=BATCH_SIZE)


def lambda_handler(event, context):
    start_time = time.monotonic()

    for record in event.get("Records", []):
        try:
            payload = record.get("body")
            if isinstance(payload, str):
                payload = json.loads(payload)
            release = Release(**payload)

            # batcher
            batches = batcher_job.run(release)
            logger.info(
                f"Batched release: {release.filename} into {len(batches)} batches."
            )

            logger.info("Starting queuer job...")

            # <test>
            if BATCH_COUNT_TO_QUEUE is not None:
                batch_count = min(BATCH_COUNT_TO_QUEUE, len(batches))
                batches = batches[:batch_count]
                logger.info(f"Limiting to {batch_count} batches for testing purposes.")
            # </test>

            for batch in batches:
                logger.debug(
                    f"Queueing {release.id} batch-{batch.batch_num} metadata..."
                )
                queuer_job.run(batch)
                logger.debug(
                    f"Queued {release.filename} "
                    f"batch-{batch.batch_num} metadata: {batch}"
                )

            logger.info(
                f"Queued {len(batches)} batches for release: {release.filename}"
            )
            logger.info("Queuer job completed.")

        except Exception as e:
            logger.error(
                f"Failed to queue release batches: {e}",
                exc_info=True,
            )

    end_time = time.monotonic()
    elapsed_time = timedelta(seconds=end_time - start_time)
    logger.info(f"Total elapsed time: {elapsed_time}")
