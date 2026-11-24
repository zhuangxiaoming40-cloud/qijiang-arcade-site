from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DIST = ROOT / "dist"

ROOT_FILES = [
    "index.html",
    "xiaoming-zhuang.html",
    "contact.html",
    "privacy.html",
    "credits.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "_headers",
    "_redirects",
    "favicon.svg",
    "google7d30a7bf7e88042e.html",
    "5d25396680c6579654783df5540d07e4.txt",
]

ASSET_FILES = [
    "LICENSE.taste-skill.txt",
    "system.css",
    "system.js",
    "site.css",
    "catalog.css",
    "ui/base.css",
    "ui/cards.css",
    "ui/ui.js",
    "motion/motion.css",
    "motion/motion.js",
    "layout/layout.css",
    "layout/layout.js",
    "icons/icon.css",
    "moments/moments.js",
    "moments/lib.js",
    "moments/picture-develops/moment.css",
    "moments/picture-develops/moment.js",
    "moments/picture-develops/meta.json",
    "img/share.jpg",
]


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for name in ROOT_FILES:
        copy_file(SITE / name, DIST / name)

    for name in ASSET_FILES:
        copy_file(SITE / "assets" / name, DIST / "assets" / name)

    catalog_source = SITE / "assets" / "catalog"
    catalog_target = DIST / "assets" / "catalog"
    catalog_target.mkdir(parents=True)
    images = sorted(catalog_source.glob("*.webp"))
    for image in images:
        copy_file(image, catalog_target / image.name)

    shutil.copytree(SITE / "products", DIST / "products")


if __name__ == "__main__":
    build()
    print(f"Built static production site at {DIST}")
