# import json
# import boto3

from src.core.entities.nca_raw_table import NCARawTable


class SQSQueue:
    def __init__(self, queue_url: str):
        # self.sqs = boto3.client('sqs')
        self.queue_url = queue_url

    def send_batch(self, data: NCARawTable) -> None:
        try:
            # response = self.sqs.send_message(
            #     QueueUrl=self.queue_url,
            #     MessageBody=json.dumps({"data": data.model_dump()})
            # )
            print("new queue")
        except Exception as e:
            raise e
