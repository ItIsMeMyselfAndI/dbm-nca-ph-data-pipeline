from typing import List, Protocol
from io import BytesIO


class ParserProvider(Protocol):
    def split_pages(self, data: BytesIO) -> List[BytesIO]:
        """split multi-page file into single-page pdfs"""
        ...

    def extract_raw_table_rows(self,
                               data: BytesIO,
                               page_num: int,
                               ) -> List[List[str | None]]:
        """extract file table/s and return list of string lists"""
        ...
