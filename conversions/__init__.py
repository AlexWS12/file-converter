from .md_html import md_to_html
from .html_md import html_to_md
from .csv_json import csv_to_json
from .json_csv import json_to_csv
from .csv_npy import csv_to_npy
from .npy_csv import npy_to_csv
from .image_webp import any_to_webp, webp_to_any
from .docx_txt import docx_to_txt, txt_to_docx
from .txt_pdf import txt_to_pdf
from .pdf_txt import pdf_to_txt
from .image_png_jpeg import png_to_jpeg, jpeg_to_png

CONVERSIONS = {
    (".md", ".html"): md_to_html,
    (".html", ".md"): html_to_md,

    (".csv", ".json"): csv_to_json,
    (".json", ".csv"): json_to_csv,

    (".csv", ".npy"): csv_to_npy,
    (".npy", ".csv"): npy_to_csv,

    (".png", ".webp"): any_to_webp,
    (".jpg", ".webp"): any_to_webp,
    (".jpeg", ".webp"): any_to_webp,
    (".webp", ".png"): webp_to_any,
    (".webp", ".jpg"): webp_to_any,
    (".webp", ".jpeg"): webp_to_any,

    (".docx", ".txt"): docx_to_txt,
    (".txt", ".docx"): txt_to_docx,

    (".txt", ".pdf"): txt_to_pdf,

    (".pdf", ".txt"): pdf_to_txt,

    # PNG ↔ JPG/JPEG
    (".png", ".jpg"): png_to_jpeg,
    (".png", ".jpeg"): png_to_jpeg,
    (".jpg", ".png"): jpeg_to_png,
    (".jpeg", ".png"): jpeg_to_png,
}
