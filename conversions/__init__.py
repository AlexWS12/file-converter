from .md_html import md_to_html
from .html_md import html_to_md

CONVERSIONS = {
    (".md", ".html"): md_to_html,
    (".html", ".md"): html_to_md,
}
