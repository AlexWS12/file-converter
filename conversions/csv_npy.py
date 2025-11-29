from pathlib import Path
import csv
import numpy as np


def csv_to_npy(src: Path, dst: Path):
    rows = []

    with src.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            rows.append([float(x) for x in row])

    arr = np.array(rows, dtype=float)
    np.save(dst, arr)
