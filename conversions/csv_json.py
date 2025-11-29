from pathlib import Path
import csv
import json


def csv_to_json(src: Path, dst: Path):
    rows = []

    with src.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    dst.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
