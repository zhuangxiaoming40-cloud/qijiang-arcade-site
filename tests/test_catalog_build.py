from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class CatalogDataTests(unittest.TestCase):
    def test_catalog_contains_all_sixty_unique_products(self) -> None:
        catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
        numbers = [product["number"] for product in catalog["products"]]

        self.assertEqual(numbers, list(range(1, 61)))
        self.assertEqual(len(catalog["categories"]), 10)
        self.assertEqual(sum(category["count"] for category in catalog["categories"]), 60)

    def test_catalog_images_are_present_and_responsive(self) -> None:
        catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
        image_dir = ROOT / "site" / "assets" / "catalog"

        for product in catalog["products"]:
            number = product["number"]
            self.assertTrue((image_dir / f"{number:02d}.webp").exists())
            self.assertTrue((image_dir / f"{number:02d}-320.webp").exists())

    def test_public_catalog_data_contains_no_quote_prices(self) -> None:
        raw = (ROOT / "data" / "catalog.json").read_text(encoding="utf-8")
        self.assertNotIn("US$", raw)
        self.assertNotIn('"price"', raw.lower())
        self.assertNotIn("QJ-Q20261115", raw)

    def test_public_catalog_data_contains_no_invented_model_codes(self) -> None:
        raw = (ROOT / "data" / "catalog.json").read_text(encoding="utf-8")
        self.assertNotIn('"id"', raw)
        self.assertNotIn("QJ-", raw)


class CatalogGeneratorTests(unittest.TestCase):
    def test_generator_builds_hub_categories_and_products(self) -> None:
        import build_catalog

        build_catalog.build()

        product_root = ROOT / "site" / "products"
        expected = list(product_root.rglob("index.html"))
        self.assertEqual(len(expected), 71)

        catalog_html = (product_root / "index.html").read_text(encoding="utf-8")
        self.assertIn("60", catalog_html)
        self.assertEqual(catalog_html.count('class="catalog-category-card"'), 10)
        self.assertEqual(catalog_html.count('class="catalog-product-card"'), 6)

    def test_generated_product_page_has_product_schema(self) -> None:
        import build_catalog

        build_catalog.build()

        product = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))[
            "products"
        ][0]
        page = (
            ROOT
            / "site"
            / "products"
            / product["category_slug"]
            / product["slug"]
            / "index.html"
        ).read_text(encoding="utf-8")
        json_ld = re.search(
            r'<script type="application/ld\+json">(.*?)</script>', page, re.DOTALL
        )

        self.assertIsNotNone(json_ld)
        payload = json.loads(json_ld.group(1))
        types = [entry["@type"] for entry in payload["@graph"]]
        self.assertIn("Product", types)
        self.assertIn("BreadcrumbList", types)
        self.assertIn(product["name"], page)
        self.assertIn("Catalogue item 001", page)
        self.assertIn("https://wa.me/8617691342432?text=Hello%20Xiaoming", page)
        self.assertNotIn("US$", page)
        product_entity = next(entry for entry in payload["@graph"] if entry["@type"] == "Product")
        self.assertNotIn("sku", product_entity)

    def test_generated_product_pages_omit_missing_source_specs(self) -> None:
        import build_catalog

        build_catalog.build()

        catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
        product = catalog["products"][0]
        page = (
            ROOT
            / "site"
            / "products"
            / product["category_slug"]
            / product["slug"]
            / "index.html"
        ).read_text(encoding="utf-8")

        self.assertNotIn("Not specified", page)
        self.assertNotIn('"name":"Gross weight"', page)
        self.assertNotIn('"name":"Power"', page)

    def test_catalog_cards_use_correct_feature_and_singular_counts(self) -> None:
        import build_catalog

        build_catalog.build()

        catalog_html = (ROOT / "site" / "products" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertEqual(catalog_html.count('class="catalog-product-card"'), 6)
        self.assertIn("Six selected product formats", catalog_html)
        self.assertIn("1 model", catalog_html)
        self.assertNotIn("1 models", catalog_html)
        self.assertNotIn("Eight popular product formats", catalog_html)
        self.assertIn("See featured models", catalog_html)
        self.assertNotIn("See all 60 models", catalog_html)

        llms = (ROOT / "site" / "llms.txt").read_text(encoding="utf-8")
        self.assertNotIn("(1 models)", llms)
        self.assertIn("(1 model)", llms)
        self.assertIn("Material, gross weight and power are shown only where provided", llms)

    def test_public_copy_uses_catalogue_items_instead_of_model_numbers(self) -> None:
        import build_catalog

        build_catalog.build()

        for path in [
            ROOT / "site" / "index.html",
            ROOT / "site" / "products" / "index.html",
            ROOT / "site" / "contact.html",
            ROOT / "site" / "xiaoming-zhuang.html",
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("model numbers", text, path)
            self.assertNotIn("Send the model,", text, path)

        contact = (ROOT / "site" / "contact.html").read_text(encoding="utf-8")
        profile = (ROOT / "site" / "xiaoming-zhuang.html").read_text(encoding="utf-8")
        for page in (contact, profile):
            self.assertIn("60 catalogue items", page)
            self.assertIn('href="/products/"', page)

    def test_screen_free_skee_ball_description_stands_alone(self) -> None:
        import build_catalog

        build_catalog.build()

        page = (
            ROOT
            / "site"
            / "products"
            / "lane-and-ball-games"
            / "flash-toss-party-skee-ball-without-screen-single-lane"
            / "index.html"
        ).read_text(encoding="utf-8")
        self.assertNotIn("Same as above", page)
        self.assertIn("Screen-free version of Flash Toss Party", page)

    def test_generated_text_uses_repository_line_endings(self) -> None:
        import build_catalog

        build_catalog.build()

        generated = [
            ROOT / "site" / "index.html",
            ROOT / "site" / "contact.html",
            ROOT / "site" / "products" / "index.html",
            ROOT / "site" / "sitemap.xml",
        ]
        for path in generated:
            self.assertNotIn(b"\r\n", path.read_bytes(), path)

    def test_sitemap_contains_every_catalogue_route(self) -> None:
        import build_catalog

        build_catalog.build()

        sitemap = (ROOT / "site" / "sitemap.xml").read_text(encoding="utf-8")
        locations = re.findall(r"<loc>(.*?)</loc>", sitemap)
        self.assertEqual(len(locations), 76)
        self.assertIn("https://qijiang-arcade.pages.dev/products/", locations)
        self.assertEqual(len([url for url in locations if "/products/" in url]), 71)

    def test_home_page_exposes_the_complete_catalogue(self) -> None:
        import build_catalog

        build_catalog.build()

        catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
        home = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.assertIn("60 commercial arcade models", home)
        for category in catalog["categories"]:
            self.assertIn(f'/products/{category["slug"]}/', home)

    def test_product_image_map_lists_all_sixty_source_rows(self) -> None:
        import build_catalog

        build_catalog.build()

        mapping = (
            ROOT / "docs" / "superpowers" / "specs" / "2026-11-24-product-image-map.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            len(re.findall(r"^\| Catalogue item \d{3} \|", mapping, re.MULTILINE)),
            60,
        )

    def test_legacy_air_hockey_route_redirects_to_catalogue(self) -> None:
        redirects = (ROOT / "site" / "_redirects").read_text(encoding="utf-8")
        self.assertIn(
            "/air-hockey-tables /products/commercial-air-hockey-tables/ 301",
            redirects,
        )


class SiteBuildTests(unittest.TestCase):
    @staticmethod
    def local_target(root: Path, source: Path, link: str) -> Path | None:
        if link.startswith(("#", "mailto:", "tel:", "http://", "https://", "data:")):
            return None
        value = link.split("#", 1)[0].split("?", 1)[0]
        if not value:
            return None
        path = root / value.lstrip("/") if value.startswith("/") else source.parent / value
        if value.endswith("/"):
            return path / "index.html"
        if path.suffix:
            return path
        return path.with_suffix(".html")

    def test_production_build_contains_catalog_but_not_development_files(self) -> None:
        import build_catalog
        import build_site

        build_catalog.build()
        build_site.build()

        dist = ROOT / "dist"
        self.assertTrue((dist / "index.html").exists())
        self.assertTrue((dist / "products" / "index.html").exists())
        self.assertTrue((dist / "_redirects").exists())
        self.assertFalse((dist / "air-hockey-tables.html").exists())
        self.assertFalse((dist / ".taste-skill").exists())
        self.assertFalse((dist / "assets" / "layout" / "hero-product.html").exists())
        self.assertEqual(
            len(list((dist / "assets" / "catalog").glob("*.webp"))),
            120,
        )
        self.assertTrue((dist / "assets" / "LICENSE.taste-skill.txt").exists())

    def test_production_build_has_no_broken_local_links(self) -> None:
        import build_catalog
        import build_site
        from validate_catalog import LinkParser

        build_catalog.build()
        build_site.build()

        dist = ROOT / "dist"
        for html_file in dist.rglob("*.html"):
            if html_file.name == "404.html":
                continue
            parser = LinkParser()
            parser.feed(html_file.read_text(encoding="utf-8"))
            for link in parser.links:
                target = self.local_target(dist, html_file, link)
                if target is not None:
                    self.assertTrue(target.exists(), f"{html_file}: broken link {link}")


if __name__ == "__main__":
    unittest.main()
