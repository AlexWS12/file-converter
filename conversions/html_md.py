from pathlib import Path
import re


def html_to_md(src: Path, dst: Path):
    # Read HTML
    html = src.read_text(encoding="utf-8")
    # Remove all tags like <p>, <div>, <h1>, etc.
    text = re.sub(r"<[^>]+>", "", html)
    # Save as plain markdown text (really just text)
    dst.write_text(text, encoding="utf-8")
