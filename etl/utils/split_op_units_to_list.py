from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()

OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")


def split_op_units_to_list(input: List[List]):
    prompt = f"""
        i will give you a list of lists as input.
        the list contains lists of operating_unit & amount.
        where in the operating_unit is a string
        where in the amount is a list of float.
        the operating units are from the philippines
        department of budget & management
        national cash allocation (nca) report---
        it can be a division, office, university/college/institution,
        headquarters, etc. I want you to split the operating_unit string
        into list of string using "|" no spaces before and after.
        the output should match lenght of amount length.
        no need to add other comments, direct to the output only.
        if the operating_unit is empty, simply respond with [].
        dont copy the format of the example output,
        simply enclose the output rows w/ "--[" & "]---".
        each row are in newline.

        *example 1*
            input: [
                ['Cebu Normal University Bicol State College of Applied Sciences and Technology', [1234.44, 23423.66]],
                ['', [234234.23]],
                ['Cebu Normal University', [1234.44, 23423.66]],
            ]
            output:
                ---[Cebu Normal University|Bicol State College of Applied Sciences and Technology]---
                ---[]---
                ---[Cebu Normal University]---

        here's the inputs:
            input: {input}
    """
    client = OpenAI(
        base_url=OPEN_ROUTER_URL,
        api_key=OPEN_ROUTER_API_KEY,
    )
    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-v3.1-terminus",
        messages=[
            {
              "role": "user",
              "content": prompt
            }
        ]
    )
    content = completion.choices[0].message.content
    col: List[List[str]] = []
    if content:
        for captured in re.findall(r'---\[(.*?)\]---', content):
            values = str(captured).split("|")
            col.append(values)
    # print(f"[INFO] Formatted: {col}")
    return col
