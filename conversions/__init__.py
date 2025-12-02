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
from .json_yaml import json_to_yaml, yaml_to_json
from .yaml_npy import yaml_to_npy, npy_to_yaml
from .yaml_csv import yaml_to_csv, csv_to_yaml
from .json_toon import json_to_toon, toon_to_json
from .html_pdf import html_to_pdf, pdf_to_html
from .xml_json import xml_to_json, json_to_xml
from .xml_csv import xml_to_csv, csv_to_xml
from .xml_yaml import xml_to_yaml, yaml_to_xml
from .xml_npy import xml_to_npy, npy_to_xml

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

    # JSON → YAML/YML
    (".json", ".yaml"): json_to_yaml,
    (".json", ".yml"): json_to_yaml,

    # YAML/YML → JSON
    (".yaml", ".json"): yaml_to_json,
    (".yml", ".json"): yaml_to_json,

    # HTML ↔ PDF (text-only rendering)
    (".html", ".pdf"): html_to_pdf,
    (".pdf", ".html"): pdf_to_html,

    # XML ↔ JSON
    (".xml", ".json"): xml_to_json,
    (".json", ".xml"): json_to_xml,

    # XML ↔ CSV
    (".xml", ".csv"): xml_to_csv,
    (".csv", ".xml"): csv_to_xml,

    # XML ↔ YAML/YML
    (".xml", ".yaml"): xml_to_yaml,
    (".xml", ".yml"): xml_to_yaml,
    (".yaml", ".xml"): yaml_to_xml,
    (".yml", ".xml"): yaml_to_xml,

    # XML ↔ NPY
    (".xml", ".npy"): xml_to_npy,
    (".npy", ".xml"): npy_to_xml,

    # YAML/YML ↔ NPY
    (".yaml", ".npy"): yaml_to_npy,
    (".yml", ".npy"): yaml_to_npy,
    (".npy", ".yaml"): npy_to_yaml,
    (".npy", ".yml"): npy_to_yaml,

    # YAML/YML ↔ CSV
    (".yaml", ".csv"): yaml_to_csv,
    (".yml", ".csv"): yaml_to_csv,
    (".csv", ".yaml"): csv_to_yaml,
    (".csv", ".yml"): csv_to_yaml,

    # JSON ↔ TOON (minified JSON)
    (".json", ".toon"): json_to_toon,
    (".toon", ".json"): toon_to_json,
}
