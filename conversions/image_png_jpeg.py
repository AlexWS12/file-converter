from pathlib import Path
from PIL import Image


def png_to_jpeg(src: Path, dst: Path) -> None:
    """Convert PNG to JPEG (.jpg/.jpeg). Removes alpha channel."""
    with Image.open(src) as im:
        im = im.convert("RGB")  # JPEG doesn't support alpha
        # Save as JPEG regardless of .jpg/.jpeg
        im.save(dst, "JPEG")


def jpeg_to_png(src: Path, dst: Path) -> None:
    """Convert JPEG (.jpg/.jpeg) to PNG."""
    with Image.open(src) as im:
        # Ensure a consistent mode; PNG can handle RGB
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.save(dst, "PNG")
