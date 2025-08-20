"""Extract tables from markdown and HTML documents."""

import re
from dataclasses import dataclass


@dataclass
class Table:
    headers: list[str]
    rows: list[list[str]]
    source: str = ""


def extract_markdown_tables(text: str) -> list[Table]:
    tables = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        if "|" in lines[i] and i + 1 < len(lines) and re.match(r"^[\s|:-]+$", lines[i + 1]):
            headers = [h.strip() for h in lines[i].split("|") if h.strip()]
            i += 2  # skip separator
            rows = []
            while i < len(lines) and "|" in lines[i]:
                row = [c.strip() for c in lines[i].split("|") if c.strip()]
                rows.append(row)
                i += 1
            tables.append(Table(headers=headers, rows=rows))
        else:
            i += 1

    return tables
