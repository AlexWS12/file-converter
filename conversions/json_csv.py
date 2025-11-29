from pathlib import Path
import json
import csv


def json_to_csv(src: Path, dst: Path):
    text = src.read_text(encoding="utf-8")
    data = json.loads(text)

    if not data:
        # if empty list, write empty file
        dst.write_text("", encoding="utf-8")
        return

    # assume data is a list of dicts
    fieldnames = sorted({key for item in data for key in item.keys()})

    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
