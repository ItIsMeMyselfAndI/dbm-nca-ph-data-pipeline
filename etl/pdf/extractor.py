import time
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
from datetime import datetime

from etl.utils.nca_bytes_2_pdf import nca_bytes_2_pdf


BASE_URL = "https://www.dbm.gov.ph"
NCA_PAGE = "https://www.dbm.gov.ph/index.php/notice-of-cash-allocation-nca-listing"
WEBSITE_NAME = "PH-DBM"


def _get_dbm_nca_page():
    max_attempt = 10
    i = 1
    while i <= max_attempt:
        try:
            res = requests.get(NCA_PAGE, timeout=30)
            res.raise_for_status()
            return res
        except Exception as e:
            print(f"[!]\tFailed scraping '{WEBSITE_NAME}'")
            print(f"\t{e}")
            print(f"[*]\tRetrying (attempt-{i})...")
            time.sleep(1)
            i += 1
    print(f"[*]\tMax attempts ({max_attempt}) reached")
    res = None
    return res


def _create_release(url: str, title: str):
    if url.startswith("/"):
        url = BASE_URL + url
    filename = url.split("/")[-1]
    year = None
    if "UPDATED" in filename:
        year = datetime.now().year
    else:
        match = re.search(r'(\d{4})', filename)
        if match:
            year = match.group(1)
    release = {
        "title": title,
        "url": url,
        "filename": filename,
        "year": int(str(year))
    }
    return release


def get_nca_pdf_releases() -> List[Dict]:
    pdf_releases = []
    # scrape
    print(f"[INFO] Scraping '{WEBSITE_NAME}' website for downloadable pdfs...")
    res = _get_dbm_nca_page()
    if not res:
        print("[ERROR] Failed to scrape, try again later")
        return pdf_releases
    soup = BeautifulSoup(res.content, "html.parser")
    for elem in soup.find_all("a", href=re.compile(r".*NCA.*\.pdf$", re.I)):
        url = str(elem.get("href", ""))
        title = elem.get_text(strip=True)
        release = _create_release(url, title)
        pdf_releases.append(release)
    # logs
    length = len(pdf_releases)
    print(f"[*]\tFound {length} {"pdfs" if length > 1 else "pdf"}")
    for i, link in enumerate(pdf_releases):
        print(f"\t({i})\tTitle: {link["title"]}")
        print(f"\t\tFilename: {link["filename"]}")
        print(f"\t\tYear: {link["year"]}")
        print(f"\t\tURL: {link["url"]}")
    print("[INFO] Finished scraping PH-DBM website")
    return pdf_releases


def download_nca_pdf_bytes(release: Dict) -> BytesIO:
    url = release["url"]
    filename = release["filename"]
    print(f"[INFO] Downloading '{filename}' into bytes...")
    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception as e:
        print(f"[!] Failed downlading '{filename}'")
        print(f"\t{e}")
        print("[*] Retrying...")
        download_nca_pdf_bytes(release)
    print(f"[INFO] Finished downloading '{filename}'")
    return BytesIO(res.content)


if __name__ == "__main__":
    pdf_releases = get_nca_pdf_releases()
    for release in pdf_releases:
        bytes = download_nca_pdf_bytes(release)
        # nca_bytes_2_pdf(release, bytes)
