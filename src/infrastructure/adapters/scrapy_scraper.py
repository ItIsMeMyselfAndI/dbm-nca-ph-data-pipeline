from datetime import datetime
from io import BytesIO
import re
from typing import List

from scrapy.selector import Selector
import requests

from src.core.entities.release import Release
from src.infrastructure.constants import BASE_URL, NCA_PAGE
from src.core.interfaces.scraper import ScraperProvider


class ScrapyScraper(ScraperProvider):
    def __init__(self):
        pass

    def get_releases(self, oldest_year: int) -> List[Release]:
        releases: List[Release] = []

        res = requests.get(NCA_PAGE, timeout=30)
        res.raise_for_status()
        hyperlinks = Selector(text=res.text).xpath("//a")
        # print(hyperlinks)

        for elem in hyperlinks:
            url = elem.xpath("@href").extract_first()
            title = elem.xpath("string(.)").extract_first()

            if not url or not title:
                continue
            if not url.lower().endswith(".pdf"):
                continue

            release = self._create_release(url, title)

            if not release:
                continue

            if release.year and release.year >= oldest_year:
                releases.append(release)

        releases.sort(key=lambda x: x.year if x.year else 0)
        return releases

    def download_release(self, release: Release) -> BytesIO:
        res = requests.get(release.url)
        res.raise_for_status()
        return BytesIO(res.content)

    def _create_release(self, url: str, title: str) -> Release | None:
        if url.startswith("/"):
            url = BASE_URL + url
        filename = url.split("/")[-1]

        if "UPDATED" in filename:
            year = datetime.now().year
        else:
            year = None
            match = re.search(r"(\d{4})", filename)
            if match:
                year = int(match.group(1))

        if not year:
            return None

        release = Release(
            id=f"id_{year}", title=title, url=url, filename=filename, year=year
        )
        return release
