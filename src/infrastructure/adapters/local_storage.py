import os
from io import BytesIO


class LocalStorage:
    def __init__(self, base_raw_path: str, base_releases_path: str):
        self.abs_raw_path = os.path.abspath(base_raw_path)
        self.abs_releases_path = os.path.abspath(base_releases_path)

    def save_file(self, storage_path: str, data: BytesIO) -> None:
        self._create_base_dirs()
        full_path = os.path.abspath(storage_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        data.seek(0)
        with open(full_path, 'wb') as f:
            f.write(data.read())

    def load_file(self, storage_path: str) -> BytesIO:
        full_path = os.path.abspath(storage_path)
        with open(full_path, 'rb') as f:
            return BytesIO(f.read())

    def exists(self, storage_path: str) -> bool:
        full_path = os.path.abspath(storage_path)
        return os.path.exists(full_path)

    def _create_base_dirs(self):
        os.makedirs(self.abs_raw_path, exist_ok=True)
        os.makedirs(self.abs_releases_path, exist_ok=True)

