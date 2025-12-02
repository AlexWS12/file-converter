from pathlib import Path
from html import escape as html_escape
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from PyPDF2 import PdfReader


def _write_lines_to_pdf(lines, dst: Path) -> None:
    c = canvas.Canvas(str(dst), pagesize=LETTER)
    width, height = LETTER

    left_margin = 1 * inch
    top_margin = height - 1 * inch
    line_height = 14  # points
    max_chars = 90

    x = left_margin
    y = top_margin

    for line in lines:
        # simple soft-wrap by character count
        text = line or ""
        while len(text) > max_chars:
            part = text[:max_chars]
            c.drawString(x, y, part)
            y -= line_height
            text = text[max_chars:]
            if y < 1 * inch:
                c.showPage()
                y = top_margin
        c.drawString(x, y, text)
        y -= line_height
        if y < 1 * inch:
            c.showPage()
            y = top_margin

    c.save()


def html_to_pdf(src: Path, dst: Path) -> None:
    """Basic HTML → PDF: extract visible text and render into a simple PDF.

    Note: This does not do full HTML/CSS rendering. It strips tags and lays out text.
    For pixel-perfect rendering, consider wkhtmltopdf or WeasyPrint.
    """
    html_str = Path(src).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html_str, "html.parser")
    text = soup.get_text("\n")
    lines = text.splitlines()
    _write_lines_to_pdf(lines, dst)


def pdf_to_html(src: Path, dst: Path) -> None:
    """PDF → HTML: extract selectable text and wrap in a minimal HTML template.

    Scanned PDFs (images) won't produce text without OCR.
    """
    reader = PdfReader(str(src))
    chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        chunks.append(page_text.rstrip())
    content = "\n\n".join(chunks).strip()

    # escape text and wrap in <pre> to preserve spacing
    body = f"<pre>{html_escape(content)}</pre>" if content else "<pre></pre>"
    html_doc = """<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>Converted from PDF</title>
  <style>body{font-family:system-ui,Segoe UI,Arial,sans-serif;padding:1rem;white-space:pre-wrap}</style>
</head>
<body>
%s
</body>
</html>
""" % body
    Path(dst).write_text(html_doc, encoding="utf-8")
