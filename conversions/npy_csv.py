from pathlib import Path
import numpy as np
import csv


def npy_to_csv(src: Path, dst: Path):
    arr = np.load(src)

    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in arr:
            # row might be a single number or not a list (like scalar or 1D)
            writer.writerow(np.atleast_1d(row).tolist())
