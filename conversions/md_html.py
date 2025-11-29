from pathlib import Path


def md_to_html(src: Path, dst: Path):
    # Read markdown text
    text = src.read_text(encoding="utf-8")
    # Wrap it in HTML
    html = "<html><body>\n" + text + "\n</body></html>\n"
    # Save result
    dst.write_text(html, encoding="utf-8")
