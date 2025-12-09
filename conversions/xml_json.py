from pathlib import Path
import json
import xmltodict


def xml_to_json(src: Path, dst: Path) -> None:
    """XML → JSON (pretty)."""
    with open(src, "r", encoding="utf-8") as f:
        data = xmltodict.parse(f.read())
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def json_to_xml(src: Path, dst: Path) -> None:
    """JSON → XML (smart root + proper XML declaration).

    Rules:
    - dict with 1 key → use that key as root tag
    - dict with multiple keys → wrap in <root>
    - list → <root><item>...</item></root>
    - scalar → <root><value>...</value></root>
    """
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Pick the root structure
    if isinstance(data, dict) and len(data) == 1:
        # Single key: use it as root
        root_name, content = next(iter(data.items()))
        obj = {root_name: content}
    elif isinstance(data, dict):
        obj = {"root": data}
    elif isinstance(data, list):
        obj = {"root": {"item": data}}
    else:
        obj = {"root": {"value": data}}

    # Generate XML with declaration
    xml_body = xmltodict.unparse(obj, pretty=True, full_document=False)
    xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_body
    Path(dst).write_text(xml_str, encoding="utf-8")
