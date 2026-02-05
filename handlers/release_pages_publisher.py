from src.logging_config import setup_logging
from src.infrastructure.config import settings
from src.infrastructure.adapters.sqs_queue import SQSQueue
from src.core.use_cases.queue_release_page import QueueReleasePage
from src.core.entities.release import Release
import logging
import json

# <test>
MAX_PAGE_COUNT_TO_PUBISH = 5
# </test>


setup_logging()
logger = logging.getLogger(__name__)

# adapters
queue = SQSQueue(queue_url=settings.AWS_SQS_RELEASE_PAGE_QUEUE_URL)

# use case
queue_job = QueueReleasePage(queue=queue)


def lambda_handler(event, context):
    try:
        releases = []
        success_count = 0
        total_releases = len(event['Records'])

        for record in event['Records']:
            try:
                payload = record['body']
                if isinstance(payload, str):
                    payload = json.loads(payload)

                release = Release(**payload)

                for i in range(release.page_count):
                    queue_job.run(release, i)

                    # <test>
                    if i == MAX_PAGE_COUNT_TO_PUBISH and not None:
                        break
                    # </test>

                releases.append(release.filename)
                success_count += 1
                logger.info(f"Successfully queued pages for "
                            f"release: {release.filename}")

            except Exception as e:
                logger.error(f"Failed to process record: {e}", exc_info=True)
                continue

    except Exception as e:
        logger.critical(f"Release pages queuing job "
                        f"failed: {e}", exc_info=True)
        return {"statusCode": 400,
                "body": "Release pages queuing job failed."}

    return {
        'statusCode': 200,
        'body': {
            "filterd_releases_count": success_count,
            "total_releases_count": total_releases,
        }
    }
