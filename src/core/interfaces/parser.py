from typing import List, Protocol
from io import BytesIO

from src.core.entities.metadata import MetaData


class ParserProvider(Protocol):
    def get_metadata(self, storage_path: str) -> MetaData:
        """extract the metadata of a file"""
        ...

    def split_pages(self, data: BytesIO) -> List[BytesIO]:
        """split multi-page file into single-page pdfs"""
        ...

    def extract_raw_table_rows(self,
                               data: BytesIO,
                               page_num: int,
                               ) -> List[List[str | None]]:
        """extract file table/s and return list of string lists"""
        ...
