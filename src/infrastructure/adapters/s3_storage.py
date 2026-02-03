import logging
import boto3
from io import BytesIO
from botocore.exceptions import ClientError

from src.core.interfaces.storage import StorageProvider
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class S3Storage(StorageProvider):
    def __init__(self, base_storage_path: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.base_storage_path = base_storage_path
        self._create_bucket()

    def get_filename_full_path(self, filename: str) -> str:
        if self.base_storage_path is None or self.base_storage_path == '':
            return filename
        if self.base_storage_path.endswith('/'):
            return f"{self.base_storage_path}{filename}"
        return f"{self.base_storage_path}/{filename}"

    def save_file(self, filename: str, data: BytesIO) -> None:
        self._create_bucket()
        data_copy = BytesIO(data.getvalue())
        data_copy.seek(0)
        full_path = self.get_filename_full_path(filename)
        self.s3.upload_fileobj(data_copy, self.bucket_name, full_path)

    def load_file(self, filename: str) -> BytesIO | None:
        full_path = self.get_filename_full_path(filename)
        try:
            response = self.s3.get_object(Bucket=self.bucket_name,
                                          Key=full_path)
            return BytesIO(response['Body'].read())

        except ClientError:
            return None

    def _create_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            logger.debug(f"Bucket found: {self.bucket_name}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': settings.AWS_REGION
                    }
                )
                logger.info(f"Bucket created: {self.bucket_name}")
