from io import BytesIO
from typing import List
import pdfplumber
from pdfplumber.page import Page
import pandas as pd


def load_sample_pdf_bytes():
    with open("./sample_nca.pdf", "rb") as pdf:
        bytes = pdf.read()
    return BytesIO(bytes)


def _get_vert_lines(page: Page):
    table = page.find_table()
    vert_lines = []
    if table:
        lines = table.rows[0].cells
        if not lines:
            return
        for i, line in enumerate(lines):
            if not line:
                return
            vert_lines.append(line[0])
            if i == len(lines) - 1:
                vert_lines.append(line[2])
    return vert_lines


def _join_col_to_str(col: List[str]):
    filtered = map(lambda x: x if type(x) is str else '', col)
    return ' '.join(filter(None, filtered)).strip()


def _remove_empty_row(df: pd.DataFrame):
    has_nca_number = df["nca_number"] != ''
    has_nca_type = df["nca_type"] != ''
    has_released_date = df["released_date"] != ''
    has_department = df["department"] != ''
    has_agency = df["agency"] != ''
    has_operating_unit = df["operating_unit"] != ''
    has_amount = df["amount"] != ''
    has_purpose = df["purpose"] != ''
    df_filtered = df[
        has_nca_number | has_nca_type
        | has_released_date | has_department
        | has_agency | has_operating_unit
        | has_amount | has_purpose
    ]
    print(df_filtered.values)
    return pd.DataFrame(df_filtered)


def _join_col_to_list_str(col: List[str]):
    op_units = []
    for unit in col:
        if "\n" not in unit:
            pass
    pass


def parse_nca_bytes(bytes: BytesIO):
    with pdfplumber.open(bytes) as pdf:
        records = []
        for page_num, page in enumerate(pdf.pages):
            print(f"[INFO] Parsing table in page {page_num}...")
            vert_lines = _get_vert_lines(page)
            TABLE_SETTINGS = {
                "vertical_strategy": "explicit",
                "explicit_vertical_lines": vert_lines,
                "horizontal_strategy": "text",
                "intersection_tolerance": 50,
                "snap_y_tolerance": 3,
                # "join_y_tolerance": 1,
            }
            # im = page.to_image()
            # im.debug_tablefinder(TABLE_SETTINGS).show()
            header = [
                "nca_number", "nca_type", "released_date", "department",
                "agency", "operating_unit", "amount", "purpose",
            ]
            table = page.extract_table(TABLE_SETTINGS)
            if not table:
                continue
            df = pd.DataFrame(table[1:], columns=header)
            df = _remove_empty_row(df)
            df["nca_number"] = df["nca_number"].replace('', None)
            df["nca_number"] = df["nca_number"].ffill()
            f = df[df["operating_unit"].str.contains("\n")]
            print(f.values)
            # break
            # df_merged = df.groupby("nca_number", as_index=False).agg({
            #     "nca_type": "first",
            #     "released_date": "first",
            #     "department": lambda col: _join_col_to_str(col),
            #     "agency": lambda col: _join_col_to_str(col),
            #     "operating_unit":"",
            #     "amount": "",
            #     "purpose": lambda col: _join_col_to_str(col),
            # })
            # print(df.values)
            # print(df["NCA NUMBER"].count())
            # df_merged = df.groupby("NCA NUMBER", as_index=False).agg({
            #     'NCA TYPE': "first",
            #     'RELEASED DATE': "first",
            #     'DEPARTMENT': lambda x: _join_col_to_str(x),
            #     'AGENCY': lambda x: _join_col_to_str(x),
            #     'OPERATING UNIT': lambda x: _join_col_to_str(x),
            #     'AMOUNT': lambda x: float(_join_col_to_str(x).replace(',', '')),
            #     'PURPOSE': lambda x: _join_col_to_str(x)
            # }).reset_index(drop=True)
            # print("\n-----------------------------------------\n")
            # print(page_num)
            # print(df_merged.values)
            # print(df_merged.info())
            # print(df_merged.shape)
            # print(df_merged.describe())
            # print(df_merged.columns)
            # print(df_merged.index)


bytes = load_sample_pdf_bytes()
parse_nca_bytes(bytes)
