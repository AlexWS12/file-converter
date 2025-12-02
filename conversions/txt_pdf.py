from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch


def txt_to_pdf(src: Path, dst: Path):
    # Render a TXT file into a simple paginated PDF
    text = Path(src).read_text(encoding="utf-8")
    lines = text.splitlines()

    c = canvas.Canvas(str(dst), pagesize=LETTER)
    width, height = LETTER

    left_margin = 1 * inch
    top_margin = height - 1 * inch
    line_height = 14  # points

    x = left_margin
    y = top_margin

    for line in lines:
        # Split long lines
        max_chars = 90
        while len(line) > max_chars:
            part = line[:max_chars]
            c.drawString(x, y, part)
            y -= line_height
            line = line[max_chars:]
            if y < 1 * inch:
                c.showPage()
                y = top_margin
        c.drawString(x, y, line)
        y -= line_height
        if y < 1 * inch:
            c.showPage()
            y = top_margin

    c.save()
