from etl.loader import load_nca_to_db
from etl.transformer import load_sample_pdf_bytes, parse_nca_bytes


def main():
    # releases = get_nca_pdf_releases()
    pdf_bytes = load_sample_pdf_bytes()
    sample_release = {"title": "SAMPLE NCA", "year": "2025",
                      "filename": "sample_nca.pdf", "url": "#"}
    records = parse_nca_bytes(5, pdf_bytes, sample_release)
    load_nca_to_db(sample_release, records)


if __name__ == "__main__":
    main()
