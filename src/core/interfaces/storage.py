from typing import Protocol
from io import BytesIO


class StorageProvider(Protocol):

    def save_file(self, storage_path: str, data: BytesIO):
        """saves data to the destination (s3, disk, etc)"""
        ...

    def load_file(self, storage_path: str) -> BytesIO:
        """load data into memory"""
        ...

    def exists(self, storage_path: str) -> bool:
        """checks if file exists"""
        ...
