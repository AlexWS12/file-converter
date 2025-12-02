from pathlib import Path
from PIL import Image


def any_to_webp(src: Path, dst: Path) -> None:
    """Convert PNG/JPG/JPEG to WEBP (simple and readable).

    Steps:
    - Open the source image
    - Convert to RGB/RGBA (to avoid mode issues)
    - Save as WEBP
    """
    with Image.open(src) as im:
        # If image has an alpha channel, keep it; otherwise use RGB
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        im.save(dst, "WEBP")


def webp_to_any(src: Path, dst: Path) -> None:
    """Convert WEBP to PNG or JPEG based on dst extension.

    Supported outputs: .png, .jpg, .jpeg
    """
    fmt_map = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}
    fmt = fmt_map.get(dst.suffix.lower())
    if not fmt:
        raise ValueError(f"Unsupported target format: {dst.suffix}")

    with Image.open(src) as im:
        # PNG can carry transparency, JPEG cannot
        im = im.convert("RGBA" if fmt == "PNG" else "RGB")
        im.save(dst, fmt)
