from pathlib import Path
import csv
import json
import xmltodict
from typing import Any


def xml_to_csv(src: Path, dst: Path) -> None:
    """XML → CSV (simple).

    - Tries to find a list of dicts in the XML to use as rows
    - If not found, writes a single-row table from the root dict
    - Nested values (dict/list) are JSON strings
    """
    text = Path(src).read_text(encoding="utf-8", errors="ignore")
    data: Any = xmltodict.parse(text)

    rows = []
    if isinstance(data, list) and data and isinstance(data[0], dict):
        rows = data
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                rows = v
                break
        if not rows:
            rows = [data]
    else:
        rows = [{"value": str(data)}]

    headers = []
    seen = set()
    for row in rows:
        if isinstance(row, dict):
            for k in row.keys():
                if k not in seen:
                    headers.append(k)
                    seen.add(k)

    def cell(x):
        if isinstance(x, (dict, list)):
            return json.dumps(x, ensure_ascii=False, separators=(",", ":"))
        return "" if x is None else str(x)

    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for row in rows:
            if isinstance(row, dict):
                w.writerow([cell(row.get(h, "")) for h in headers])
            else:
                w.writerow([cell(row)])


def csv_to_xml(src: Path, dst: Path) -> None:
    """CSV → XML (rows under <root><row>...> using header names)."""
    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    obj = {"root": {"row": rows}}
    xml_str = xmltodict.unparse(obj, pretty=True)
    Path(dst).write_text(xml_str, encoding="utf-8")
