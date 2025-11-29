from pathlib import Path
from conversions import CONVERSIONS


def normalize_ext(ext: str) -> str:
    ext = ext.strip().lower()                                   # checks for .ext format, if wrong, fixes it (lowercase and adds dot)
    return "." + ext if not ext.startswith(".") else ext 


def convert_all(root: str, from_ext: str, to_ext: str):
    from_ext = normalize_ext(from_ext)
    to_ext = normalize_ext(to_ext)

    func = CONVERSIONS[(from_ext, to_ext)]                      # get the conversion function

    root_path = Path(root)

                                                                # loops through all files in the folder (and subfolders) that match the input extension
    for path in root_path.rglob(f"*{from_ext}"):
        if path.is_file() and path.name != "README.md":         # ensures we don't convert README.md files
            dst = path.with_suffix(to_ext)                      # creates new path with the target extension
            func(path, dst)                                     # calls the conversion function
            print(f"{path} → {dst}")                            # displays conversion result
