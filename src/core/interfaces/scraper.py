from io import BytesIO
from typing import List, Protocol
from src.core.entities.release import Release


class ScraperProvider(Protocol):
    def get_releases(self, oldest_year: int) -> List[Release]:
        """get nca release urls from ph-dbm website"""
        ...

    def download_release(self, release: Release) -> BytesIO:
        """download nca release bytes into memory"""
        ...
