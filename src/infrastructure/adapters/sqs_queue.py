import json
import boto3
import logging

from pydantic import BaseModel

from src.core.interfaces.queue import QueueProvider

logger = logging.getLogger(__name__)


class SQSQueue(QueueProvider):
    def __init__(self, queue_url: str):
        self.sqs = boto3.client("sqs")
        self.queue_url = queue_url

    def send(self, data: BaseModel) -> None:
        try:
            message_body = json.dumps(data.model_dump(mode="json"))

            self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=message_body)

            logger.debug(f"Sent data to queue: {data}")

        except Exception as e:
            logger.error(f"Failed to send data to SQS: {e}")
            raise e
