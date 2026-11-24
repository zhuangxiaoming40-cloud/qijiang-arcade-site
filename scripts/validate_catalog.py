from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link", "img", "script"}:
            return
        attributes = dict(attrs)
        value = attributes.get("href") or attributes.get("src")
        if value:
            self.links.append(value)


def local_target(source: Path, link: str) -> Path | None:
    if link.startswith(("#", "mailto:", "tel:", "http://", "https://", "data:")):
        return None
    value = link.split("#", 1)[0].split("?", 1)[0]
    if not value:
        return None
    if value.startswith("/"):
        path = SITE / value.lstrip("/")
    else:
        path = source.parent / value
    if value.endswith("/"):
        return path / "index.html"
    if path.suffix:
        return path
    return path.with_suffix(".html")


def main() -> int:
    catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    catalog_pages = sorted((SITE / "products").rglob("index.html"))
    if len(catalog_pages) != 71:
        errors.append(f"expected 71 catalogue pages, found {len(catalog_pages)}")

    for product in catalog["products"]:
        number = product["number"]
        for suffix, expected_size in (("", (600, 450)), ("-320", (320, 240))):
            image_path = SITE / "assets" / "catalog" / f"{number:02d}{suffix}.webp"
            if not image_path.exists():
                errors.append(f"missing image: {image_path}")
                continue
            with Image.open(image_path) as image:
                if image.size != expected_size:
                    errors.append(
                        f"wrong image size: {image_path} {image.size} != {expected_size}"
                    )

        page_path = (
            SITE
            / "products"
            / product["category_slug"]
            / product["slug"]
            / "index.html"
        )
        if not page_path.exists():
            errors.append(f"missing product page: {page_path}")
            continue
        page = page_path.read_text(encoding="utf-8")
        visible_page = unescape(page)
        if product["name"] not in visible_page:
            errors.append(f"product name missing from {page_path}")
        if f"Catalogue item {number:03d}" not in visible_page:
            errors.append(f"catalogue item missing from {page_path}")
        if "US$" in page or "QJ-Q20261115" in page or "Moris Mirzadeh" in page:
            errors.append(f"private quotation data found in {page_path}")
        if "QJ-" in page or "Model number" in page or '"sku"' in page:
            errors.append(f"invented model code or SKU found in {page_path}")
        json_blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', page, re.DOTALL
        )
        if len(json_blocks) != 1:
            errors.append(f"expected one JSON-LD block in {page_path}")
            continue
        json.loads(json_blocks[0])

    sitemap_root = ET.parse(SITE / "sitemap.xml").getroot()
    locations = [element.text for element in sitemap_root.findall("{*}url/{*}loc")]
    if len(locations) != 76:
        errors.append(f"expected 76 sitemap URLs, found {len(locations)}")

    html_files = list(SITE.glob("*.html")) + catalog_pages
    for html_file in html_files:
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for link in parser.links:
            target = local_target(html_file, link)
            if target is not None and not target.exists():
                errors.append(f"broken local link in {html_file}: {link} -> {target}")

    if errors:
        print("\n".join(f"FAIL {error}" for error in errors))
        return 1

    print("PASS 60 products, 10 categories, 71 catalogue pages")
    print("PASS 120 responsive product image files")
    print("PASS 76 sitemap URLs")
    print("PASS JSON-LD, private-data, and local-link checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
