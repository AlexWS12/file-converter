from pathlib import Path
from typing import Any, Optional
import numpy as np
import xmltodict


def _find_first_list(obj: Any) -> Optional[list]:
    """Find the first Python list inside a parsed-XML structure.
    Keeps it simple: looks through dict values and nested containers.
    """
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            found = _find_first_list(v)
            if found is not None:
                return found
    return None


def xml_to_npy(src: Path, dst: Path) -> None:
    """XML → NPY (numeric arrays only).

    Heuristic:
    - Parse XML with xmltodict
    - Find the first list in the structure
      • If it's a list of numbers -> 1xN array
      • If it's a list of lists of numbers -> NxM array
    - Otherwise, raise a clear error
    """
    text = Path(src).read_text(encoding="utf-8", errors="ignore")
    data = xmltodict.parse(text)

    arr_like = _find_first_list(data)
    if arr_like is None:
        raise ValueError("Could not find a list in XML to convert to a numeric array")

    # Let NumPy coerce to float; shape nicely
    arr = np.asarray(arr_like, dtype=float)
    if arr.ndim == 0:  # scalar
        arr = arr.reshape(1, 1)
    elif arr.ndim == 1:  # 1D -> 1xN
        arr = arr.reshape(1, -1)

    np.save(dst, arr, allow_pickle=False)


def npy_to_xml(src: Path, dst: Path) -> None:
    """NPY → XML (simple <root> structure).

    - 1D array -> <root><item>v</item>...</root>
    - 2D array -> <root><row><item>v</item>...</row>...</root>
    """
    arr = np.load(src, allow_pickle=False)

    if arr.ndim == 0:
        data_obj = {"root": {"value": float(arr)}}
    elif arr.ndim == 1:
        items = [float(x) for x in arr.tolist()]
        data_obj = {"root": {"item": items}}
    else:
        rows = [{"item": [float(x) for x in row]} for row in arr.tolist()]
        data_obj = {"root": {"row": rows}}

    xml_str = xmltodict.unparse(data_obj, pretty=True)
    Path(dst).write_text(xml_str, encoding="utf-8")
