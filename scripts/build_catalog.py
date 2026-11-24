from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA_PATH = ROOT / "data" / "catalog.json"
PRODUCT_ROOT = SITE / "products"
BASE_URL = "https://qijiang-arcade.pages.dev"
FACEBOOK_URL = "https://www.facebook.com/QIJIANGTECHNOLOGY/"
IMAGE_MAP_PATH = (
    ROOT / "docs" / "superpowers" / "specs" / "2026-11-24-product-image-map.md"
)

CATEGORY_COPY = {
    "lane-and-ball-games": {
        "title": "Skee-ball and roll-ball machines",
        "summary": "Commercial roll-ball, skee-ball and bowling machines for family entertainment centers.",
    },
    "commercial-air-hockey-tables": {
        "title": "Commercial air hockey tables",
        "summary": "Family and children's air hockey tables with LCD, curved, flat and multi-puck formats.",
    },
    "table-football-machines": {
        "title": "Commercial table football machines",
        "summary": "Two-player table football cabinets for family venues, offices and entertainment spaces.",
    },
    "boxing-strength-machines": {
        "title": "Boxing and strength-test machines",
        "summary": "Commercial boxing, punch and hammer strength-test machines for arcades and FECs.",
    },
    "basketball-arcade-machines": {
        "title": "Commercial basketball arcade machines",
        "summary": "Basketball arcade cabinets for adult players, children and prize-redemption areas.",
    },
    "racing-simulators": {
        "title": "Racing simulators and arcade racers",
        "summary": "Motion racing simulators, linked twin racers and horse-racing arcade games.",
    },
    "shooting-arcade-games": {
        "title": "Shooting arcade games",
        "summary": "Gun shooting, deluxe shooting cabinets and water shooting games for entertainment venues.",
    },
    "dance-machines": {
        "title": "Commercial dance machines",
        "summary": "Dance arcade machines for family entertainment centers and indoor amusement venues.",
    },
    "electronic-dart-machines": {
        "title": "Electronic dart machines",
        "summary": "Online, standalone, touchscreen and compact electronic dart machines with LCD displays.",
    },
    "balloon-shooting-machines": {
        "title": "Balloon shooting machines",
        "summary": "Balloon gun machines for family entertainment centers and carnival-style game areas.",
    },
}


def load_catalog() -> dict[str, Any]:
    catalog = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    products = catalog["products"]
    if len(products) != 60:
        raise ValueError(f"Expected 60 products, found {len(products)}")
    if len(catalog["categories"]) != 10:
        raise ValueError(f"Expected 10 categories, found {len(catalog['categories'])}")
    if len({product["slug"] for product in products}) != 60:
        raise ValueError("Product slugs must be unique")
    return catalog


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def money_free(value: str) -> str:
    return value.replace("US$", "")


def sentence(value: str) -> str:
    text = str(value).strip()
    if not text:
        return text
    return text if text.endswith((".", "!", "?")) else f"{text}."


def count_label(count: int, noun: str = "models") -> str:
    return f"{count} {noun[:-1] if count == 1 else noun}"


def catalogue_item(product: dict[str, Any]) -> str:
    return f"Catalogue item {int(product['number']):03d}"


def dimension_text(value: str) -> str:
    text = str(value).strip()
    return f"{text} cm" if "×" in text else text


def absolute(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def product_url(product: dict[str, Any], trailing_slash: bool = True) -> str:
    suffix = "/" if trailing_slash else ""
    return f"/products/{product['category_slug']}/{product['slug']}{suffix}"


def category_url(category: dict[str, Any], trailing_slash: bool = True) -> str:
    suffix = "/" if trailing_slash else ""
    return f"/products/{category['slug']}{suffix}"


def image_paths(product: dict[str, Any]) -> tuple[str, str, str]:
    number = f"{product['number']:02d}"
    small = f"/assets/catalog/{number}-320.webp"
    large = f"/assets/catalog/{number}.webp"
    srcset = f"{small} 320w, {large} 600w"
    return small, large, srcset


def organization_json() -> dict[str, Any]:
    return {
        "@type": "Organization",
        "@id": f"{BASE_URL}/#organization",
        "name": "Guangzhou Qijiang Technology Co., Ltd.",
        "alternateName": "Qijiang Arcade",
        "url": f"{BASE_URL}/",
        "logo": f"{BASE_URL}/favicon.svg",
        "sameAs": [FACEBOOK_URL],
        "description": "Manufacturer of commercial arcade equipment in Guangzhou, China.",
        "email": "zhuangxiaoming40@gmail.com",
        "telephone": "+86 176 9134 2432",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "No. 18 Nanyuan Avenue, Kengtou, Nancun Town, Panyu District",
            "addressLocality": "Guangzhou",
            "addressRegion": "Guangdong",
            "addressCountry": "CN",
        },
    }


def website_json() -> dict[str, Any]:
    return {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": f"{BASE_URL}/",
        "name": "Qijiang Arcade",
        "publisher": {"@id": f"{BASE_URL}/#organization"},
    }


def person_json() -> dict[str, Any]:
    return {
        "@type": "Person",
        "@id": f"{BASE_URL}/xiaoming-zhuang#person",
        "name": "Xiaoming Zhuang",
        "jobTitle": "Export Sales",
        "email": "zhuangxiaoming40@gmail.com",
        "telephone": "+86 176 9134 2432",
        "url": f"{BASE_URL}/xiaoming-zhuang",
        "worksFor": {"@id": f"{BASE_URL}/#organization"},
    }


def breadcrumb_json(items: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{items[-1][1]}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": index, "name": name, "item": url}
            for index, (name, url) in enumerate(items, start=1)
        ],
    }


def page_head(
    title: str,
    description: str,
    canonical: str,
    image: str,
    structured_data: dict[str, Any],
) -> str:
    payload = json.dumps(structured_data, ensure_ascii=False, separators=(",", ":"))
    payload = (
        payload.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("'", "\\u0027")
    )
    return f"""<!doctype html>
<html lang="en" data-type="product" data-radius="soft" data-buttons="block">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="site-kind" content="other">
<meta name="page-type" content="product">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:site_name" content="Guangzhou Qijiang Technology Co., Ltd.">
<meta property="og:image" content="{esc(BASE_URL + image)}">
<meta property="og:image:alt" content="{esc(title)}">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="450">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Instrument+Sans:wdth,wght@75..100,400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/system.css">
<link rel="stylesheet" href="/assets/ui/cards.css">
<link rel="stylesheet" href="/assets/layout/layout.css">
<link rel="stylesheet" href="/assets/icons/icon.css">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/catalog.css">
<script type="application/ld+json">{payload}</script>
</head>"""


def header_html() -> str:
    return """<body class="catalog-page">
<header class="nav nav--split catalog-nav">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">Skip to content</a>
    <nav class="nav__links" aria-label="Main">
      <div class="nav__item"><a class="nav__link" href="/">Home</a></div>
      <div class="nav__item"><a class="nav__link" href="/products/" aria-current="page">Products</a></div>
      <div class="nav__item"><a class="nav__link" href="/xiaoming-zhuang">Sales contact</a></div>
      <div class="nav__item"><a class="nav__link" href="/contact">Contact</a></div>
    </nav>
    <a class="nav__logo" href="/">Qijiang Arcade</a>
    <div class="nav__actions"><a class="btn btn--primary" href="/contact">Request a quote</a></div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu">
      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>"""


def footer_html(categories: list[dict[str, Any]]) -> str:
    category_links = "".join(
        f'<li><a href="{category_url(category)}">{esc(CATEGORY_COPY[category["slug"]]["title"])}</a></li>'
        for category in categories[:5]
    )
    return f"""<footer class="footer closing footer--dark ground-inverse">
  <div class="wrap">
    <div class="closing__cta close--type">
      <div class="section-head">
        <h2>Request export pricing</h2>
        <p class="t-lead">Send the product name or catalogue item, quantity, destination country and voltage requirement to Xiaoming Zhuang.</p>
      </div>
      <a class="btn btn--primary btn--xl" href="/contact">Request a quote</a>
    </div>
    <div class="closing__links">
      <div class="grid">
        <div class="span-4 stack-4">
          <a class="nav__logo" href="/">Qijiang Arcade</a>
          <p class="footer__lede">Commercial arcade equipment from Guangzhou, China.</p>
        </div>
        <div class="span-4 footer__col">
          <h3>Product catalogue</h3>
          <ul>{category_links}</ul>
        </div>
        <div class="span-4 footer__col">
          <h3>Contact</h3>
          <ul>
            <li><a href="mailto:zhuangxiaoming40@gmail.com">zhuangxiaoming40@gmail.com</a></li>
            <li><a href="tel:+8617691342432">+86 176 9134 2432</a></li>
            <li><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li>
            <li><a href="{FACEBOOK_URL}">Facebook page</a></li>
            <li>Guangzhou, Guangdong, China</li>
          </ul>
        </div>
      </div>
      <div class="footer__legal">
        <span>&copy; 2026 Guangzhou Qijiang Technology Co., Ltd. &nbsp; <a href="/privacy">Privacy</a></span>
        <a class="credits" href="/credits">Product images supplied by Guangzhou Qijiang Technology Co., Ltd.</a>
      </div>
    </div>
  </div>
</footer>
<script type="module" src="/assets/system.js"></script>
</body>
</html>
"""


def product_card(product: dict[str, Any]) -> str:
    small, large, srcset = image_paths(product)
    details = f'{esc(product["dimensions_cm"])} cm · {esc(product["material"] or product["unit"])}'
    return f"""<article class="catalog-product-card">
  <a class="catalog-product-card__link" href="{product_url(product)}">
    <div class="catalog-product-card__media">
      <img src="{large}" srcset="{small} 320w, {large} 600w" sizes="(max-width: 639px) 92vw, (max-width: 1023px) 44vw, 360px" alt="{esc(product['name'])} commercial arcade machine" width="600" height="450" loading="lazy" decoding="async">
    </div>
    <div class="catalog-product-card__body">
      <p class="catalog-model">{catalogue_item(product)}</p>
      <h3>{esc(product['name'])}</h3>
      <p>{esc(product['description'])}</p>
      <p class="catalog-facts">{details}</p>
    </div>
  </a>
</article>"""


def category_card(category: dict[str, Any], products_by_number: dict[int, dict[str, Any]]) -> str:
    first = products_by_number[category["product_numbers"][0]]
    small, large, _ = image_paths(first)
    copy = CATEGORY_COPY[category["slug"]]
    return f"""<article class="catalog-category-card">
  <a href="{category_url(category)}">
    <div class="catalog-category-card__media">
      <img src="{large}" srcset="{small} 320w, {large} 600w" sizes="(max-width: 639px) 92vw, (max-width: 1023px) 44vw, 380px" alt="{esc(first['name'])}" width="600" height="450" loading="lazy" decoding="async">
    </div>
    <div class="catalog-category-card__body">
      <span class="catalog-model">{count_label(category['count'])}</span>
      <h3>{esc(copy['title'])}</h3>
      <p>{esc(copy['summary'])}</p>
      <span class="link">View category</span>
    </div>
  </a>
</article>"""


def build_catalog_page(
    catalog: dict[str, Any],
    products_by_number: dict[int, dict[str, Any]],
) -> None:
    categories = catalog["categories"]
    cards = "".join(category_card(category, products_by_number) for category in categories)
    featured_numbers = [6, 29, 32, 41, 48, 51]
    featured = "".join(product_card(products_by_number[number]) for number in featured_numbers)
    canonical = f"{BASE_URL}/products/"
    structured = {
        "@context": "https://schema.org",
        "@graph": [
            organization_json(),
            website_json(),
            person_json(),
            {
                "@type": "CollectionPage",
                "@id": f"{canonical}#catalog",
                "url": canonical,
                "name": "Qijiang commercial arcade equipment catalogue",
                "description": "60 commercial arcade machines across ten product categories.",
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "mainEntity": {"@id": f"{canonical}#categories"},
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical}#categories",
                "numberOfItems": len(categories),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "name": CATEGORY_COPY[category["slug"]]["title"],
                        "url": absolute(category_url(category)),
                    }
                    for index, category in enumerate(categories, start=1)
                ],
            },
            breadcrumb_json([("Home", f"{BASE_URL}/"), ("Products", canonical)]),
        ],
    }
    page = (
        page_head(
            "Commercial arcade equipment catalogue | Qijiang Arcade",
            "Browse 60 commercial arcade machines from Guangzhou Qijiang Technology, including air hockey, skee-ball, racing, shooting, dance and dart machines.",
            canonical,
            products_by_number[6]["image"].replace("assets", "/assets"),
            structured,
        )
        + header_html()
        + f"""
<main id="top">
  <section class="catalog-hero">
    <div class="wrap catalog-hero__in">
      <div class="catalog-hero__copy">
        <p class="t-label">Product catalogue · 60 models</p>
        <h1>Commercial arcade equipment for entertainment venues</h1>
        <p>Ten product families for family entertainment centers, arcades, bowling venues, indoor parks and route operators.</p>
        <div class="catalog-stats">
          <span><strong>60</strong> machines</span>
          <span><strong>10</strong> categories</span>
          <span><strong>Guangzhou</strong> export sales</span>
        </div>
        <div class="btn-row"><a class="btn btn--primary" href="/contact">Request a quote</a><a class="btn btn--secondary" href="#categories">Browse categories</a></div>
      </div>
      <figure class="catalog-hero__media">
        <img src="/assets/catalog/06.webp" alt="Hockey Sniper commercial air hockey table" width="600" height="450" fetchpriority="high">
      </figure>
    </div>
  </section>
  <section class="catalog-section" id="categories">
    <div class="wrap">
      <div class="section-head section-head--row"><div><h2>Browse by product type</h2><p>Choose a category to compare every model, cabinet size and shipping data.</p></div><a class="link" href="#all-products">See featured models</a></div>
      <div class="catalog-category-grid">{cards}</div>
    </div>
  </section>
  <section class="catalog-section ground-surface" id="all-products">
    <div class="wrap">
      <div class="section-head section-head--row"><div><h2>Featured commercial arcade machines</h2><p>Six selected product formats from the complete 60-model range.</p></div><a class="link" href="#categories">Browse all categories</a></div>
      <div class="catalog-product-grid">{featured}</div>
    </div>
  </section>
</main>
"""
        + footer_html(categories)
    )
    write_page(PRODUCT_ROOT / "index.html", page)


def build_home_page(
    catalog: dict[str, Any],
    products_by_number: dict[int, dict[str, Any]],
) -> None:
    categories = catalog["categories"]
    category_cards = "".join(
        category_card(category, products_by_number) for category in categories
    )
    featured = "".join(
        product_card(products_by_number[number]) for number in [6, 28, 31, 40, 47, 50]
    )
    canonical = f"{BASE_URL}/"
    structured = {
        "@context": "https://schema.org",
        "@graph": [
            organization_json(),
            website_json(),
            person_json(),
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": "Commercial arcade equipment from Guangzhou",
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
                "about": {"@id": f"{BASE_URL}/#organization"},
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical}#categories",
                "numberOfItems": len(categories),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "name": CATEGORY_COPY[category["slug"]]["title"],
                        "url": absolute(category_url(category)),
                    }
                    for index, category in enumerate(categories, start=1)
                ],
            },
        ],
    }
    page = (
        page_head(
            "Commercial arcade equipment from Guangzhou | Qijiang Arcade",
            "Explore 60 commercial arcade models from Guangzhou Qijiang Technology, including air hockey, skee-ball, racing, shooting, dance and dart machines.",
            canonical,
            "/assets/catalog/06.webp",
            structured,
        )
        + header_html()
        + f"""
<main id="top">
  <section class="catalog-hero catalog-home-hero">
    <div class="wrap catalog-hero__in">
      <div class="catalog-hero__copy">
        <p class="t-label">Guangzhou manufacturer · export sales</p>
        <h1>Commercial arcade equipment from Guangzhou</h1>
        <p>60 commercial arcade models for family entertainment centers, bowling venues, indoor parks and route operators.</p>
        <div class="catalog-stats"><span><strong>60</strong> machines</span><span><strong>10</strong> categories</span><span><strong>1</strong> direct sales contact</span></div>
        <div class="btn-row"><a class="btn btn--primary" href="/products/">Browse all products</a><a class="btn btn--secondary" href="/contact">Request a quote</a></div>
      </div>
      <figure class="catalog-hero__media">
        <img src="/assets/catalog/06.webp" alt="Hockey Sniper commercial air hockey table" width="600" height="450" fetchpriority="high">
      </figure>
    </div>
  </section>
  <section class="catalog-section" id="range">
    <div class="wrap">
      <div class="section-head section-head--row"><div><h2>Arcade equipment by product type</h2><p>Start with the game category, then compare every model in the complete catalogue.</p></div><a class="link" href="/products/">View 60 models</a></div>
      <div class="catalog-category-grid">{category_cards}</div>
    </div>
  </section>
  <section class="catalog-section ground-surface" id="equipment">
    <div class="wrap">
      <div class="section-head section-head--row"><div><h2>Featured arcade machines</h2><p>Selected air hockey, basketball, racing, shooting, dance and dart machines from the new catalogue.</p></div><a class="link" href="/products/">See every model</a></div>
      <div class="catalog-product-grid">{featured}</div>
    </div>
  </section>
  <section class="catalog-section" id="sales">
    <div class="wrap grid grid--top">
      <div class="span-8">
        <p class="t-label">Export sales</p>
        <h2>Talk directly to Xiaoming Zhuang</h2>
        <p class="t-lead">Send the product name or catalogue item, quantity, destination country and voltage requirement. Qijiang will confirm export packing, lead time and pricing for the project.</p>
        <div class="contact-links"><a class="btn btn--primary" href="/contact">Request a quote</a><a class="btn btn--secondary" href="/xiaoming-zhuang">See sales profile</a></div>
      </div>
      <div class="span-4">
        <ul class="contact-list">
          <li><span>Email</span><a href="mailto:zhuangxiaoming40@gmail.com">zhuangxiaoming40@gmail.com</a></li>
          <li><span>Phone</span><a href="tel:+8617691342432">+86 176 9134 2432</a></li>
          <li><span>WhatsApp</span><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li>
          <li><span>Facebook</span><a href="{FACEBOOK_URL}">Visit our Facebook page</a></li>
          <li><span>Address</span><strong>No. 18 Nanyuan Avenue, Kengtou, Nancun Town, Panyu District, Guangzhou, Guangdong, China</strong></li>
        </ul>
      </div>
    </div>
  </section>
</main>
"""
        + footer_html(categories)
    )
    write_page(SITE / "index.html", page)


def update_existing_pages(catalog: dict[str, Any]) -> None:
    replacements = {
        'href="air-hockey-tables">Air hockey</a>': 'href="/products/">Products</a>',
        'href="/products/commercial-air-hockey-tables/">Air hockey</a>': 'href="/products/">Products</a>',
        'href="https://qijiang-arcade.pages.dev/air-hockey-tables.html"': (
            'href="https://qijiang-arcade.pages.dev/products/commercial-air-hockey-tables/"'
        ),
        'href="https://qijiang-arcade.pages.dev/air-hockey-tables"': (
            'href="https://qijiang-arcade.pages.dev/products/commercial-air-hockey-tables/"'
        ),
        'href="air-hockey-tables">See air hockey models</a>': (
            'href="/products/">Browse product catalogue</a>'
        ),
    }
    for path in [
        SITE / "xiaoming-zhuang.html",
        SITE / "contact.html",
        SITE / "privacy.html",
        SITE / "credits.html",
    ]:
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")

    contact_copy = (
        "Send the machine type, quantity and destination country for "
        '<a href="/products/">60 catalogue items across ten categories</a>, including '
        "13 air hockey models and other arcade equipment. Enquiries go to Xiaoming Zhuang "
        "at Guangzhou Qijiang Technology Co., Ltd."
    )
    profile_copy = (
        "Commercial arcade equipment for family entertainment centers in Guangzhou. "
        'Browse <a href="/products/">60 catalogue items across ten categories</a>, '
        "including 13 air hockey table models. Ask for specifications, export packing or a quote."
    )
    copy_replacements = {
        "Send the machine type, quantity and destination country for 13 air hockey models and other arcade equipment. Enquiries go to Xiaoming Zhuang at Guangzhou Qijiang Technology Co., Ltd.": contact_copy,
        "Commercial arcade equipment for family entertainment centers in Guangzhou, including 13 air hockey table models. Ask for specifications, export packing or a quote.": profile_copy,
    }
    for path in [
        SITE / "contact.html",
        SITE / "xiaoming-zhuang.html",
        SITE / "privacy.html",
        SITE / "credits.html",
    ]:
        text = path.read_text(encoding="utf-8")
        for old, new in copy_replacements.items():
            text = text.replace(old, new)
        same_as = f'"sameAs": ["{FACEBOOK_URL}"]'
        if same_as not in text:
            text = text.replace(
                '"logo": "https://qijiang-arcade.pages.dev/favicon.svg",',
                f'"logo": "https://qijiang-arcade.pages.dev/favicon.svg",\n'
                f'      {same_as},',
            )
            text = text.replace(
                '{"@type":"Organization","@id":"https://qijiang-arcade.pages.dev/#organization","name":"Guangzhou Qijiang Technology Co., Ltd.","url":"https://qijiang-arcade.pages.dev/"}',
                '{"@type":"Organization","@id":"https://qijiang-arcade.pages.dev/#organization","name":"Guangzhou Qijiang Technology Co., Ltd.","url":"https://qijiang-arcade.pages.dev/","sameAs":["'
                + FACEBOOK_URL
                + '"]}',
            )
        if f'href="{FACEBOOK_URL}"' not in text:
            text = text.replace(
                '<li><span>WhatsApp</span><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li>',
                '<li><span>WhatsApp</span><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li>\n'
                f'          <li><span>Facebook</span><a href="{FACEBOOK_URL}">Visit our Facebook page</a></li>',
            )
            text = text.replace(
                '<li><span>WhatsApp</span><a href="https://wa.me/8617691342432?text=Hello%20Xiaoming%2C%20I%20found%20your%20company%20profile.">Open WhatsApp chat</a></li>',
                '<li><span>WhatsApp</span><a href="https://wa.me/8617691342432?text=Hello%20Xiaoming%2C%20I%20found%20your%20company%20profile.">Open WhatsApp chat</a></li>\n'
                f'          <li><span>Facebook</span><a href="{FACEBOOK_URL}">Visit our Facebook page</a></li>',
            )
            text = text.replace(
                '<li><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li><li>Guangzhou, Guangdong, China</li>',
                '<li><a href="https://wa.me/8617691342432">Open WhatsApp chat</a></li>'
                f'<li><a href="{FACEBOOK_URL}">Facebook page</a></li><li>Guangzhou, Guangdong, China</li>',
            )
        path.write_text(text, encoding="utf-8", newline="\n")

    llms = (
        "# Guangzhou Qijiang Technology Co., Ltd.\n\n"
        "Official company website: https://qijiang-arcade.pages.dev/\n\n"
        f"Official Facebook page: {FACEBOOK_URL}\n\n"
        "Guangzhou Qijiang Technology Co., Ltd. supplies commercial arcade and amusement "
        "equipment from Guangzhou, Guangdong, China.\n\n"
        "Export sales contact:\n"
        "- Xiaoming Zhuang, Export Sales\n"
        "- Email: zhuangxiaoming40@gmail.com\n"
        "- Telephone and WhatsApp: +86 176 9134 2432\n"
        "- Address: No. 18 Nanyuan Avenue, Kengtou, Nancun Town, Panyu District, "
        "Guangzhou, Guangdong, China\n\n"
        "Public product catalogue: https://qijiang-arcade.pages.dev/products/\n\n"
        "Categories:\n"
    )
    for category in catalog["categories"]:
        llms += (
            f"- {CATEGORY_COPY[category['slug']]['title']}: "
            f"{absolute(category_url(category))} ({count_label(category['count'])})\n"
        )
    llms += (
        "\nThe public catalogue contains 60 models with product names, descriptions, "
        "dimensions and packing information from the supplied quotation. Material, gross "
        "weight and power are shown only where provided in that source. Export prices are "
        "provided only in response to an enquiry.\n"
    )
    (SITE / "llms.txt").write_text(llms, encoding="utf-8", newline="\n")

    (SITE / "_redirects").write_text(
        "/air-hockey-tables /products/commercial-air-hockey-tables/ 301\n"
        "/air-hockey-tables.html /products/commercial-air-hockey-tables/ 301\n",
        encoding="utf-8",
        newline="\n",
    )


def build_category_pages(
    catalog: dict[str, Any],
    products_by_number: dict[int, dict[str, Any]],
) -> None:
    for category in catalog["categories"]:
        copy = CATEGORY_COPY[category["slug"]]
        items = [products_by_number[number] for number in category["product_numbers"]]
        canonical = absolute(category_url(category))
        cards = "".join(product_card(product) for product in items)
        structured = {
            "@context": "https://schema.org",
            "@graph": [
                organization_json(),
                website_json(),
                person_json(),
                {
                    "@type": "CollectionPage",
                    "@id": f"{canonical}#category",
                    "url": canonical,
                    "name": copy["title"],
                    "description": copy["summary"],
                    "isPartOf": {"@id": f"{BASE_URL}/#website"},
                    "mainEntity": {"@id": f"{canonical}#products"},
                },
                {
                    "@type": "ItemList",
                    "@id": f"{canonical}#products",
                    "numberOfItems": len(items),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index,
                            "name": product["name"],
                            "url": absolute(product_url(product)),
                        }
                        for index, product in enumerate(items, start=1)
                    ],
                },
                breadcrumb_json(
                    [
                        ("Home", f"{BASE_URL}/"),
                        ("Products", f"{BASE_URL}/products/"),
                        (copy["title"], canonical),
                    ]
                ),
            ],
        }
        page = (
            page_head(
                f"{copy['title']} | Qijiang Arcade",
                copy["summary"],
                canonical,
                items[0]["image"].replace("assets", "/assets"),
                structured,
            )
            + header_html()
            + f"""
<main id="top">
  <section class="catalog-hero catalog-hero--category">
    <div class="wrap catalog-hero__in">
      <div class="catalog-hero__copy">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/products/">Products</a><span>/</span><span>{esc(copy['title'])}</span></nav>
        <p class="t-label">{count_label(category['count'])}</p>
        <h1>{esc(copy['title'])}</h1>
        <p class="catalog-hero__lead">{esc(copy['summary'])}</p>
        <div class="btn-row"><a class="btn btn--primary" href="/contact">Request a quote</a><a class="btn btn--secondary" href="/products/">All product categories</a></div>
      </div>
      <figure class="catalog-hero__media">
        <img src="{image_paths(items[0])[1]}" srcset="{image_paths(items[0])[2]}" sizes="(max-width: 899px) 100vw, 45vw" alt="{esc(items[0]['name'])}" width="600" height="450" fetchpriority="high">
      </figure>
    </div>
  </section>
  <section class="catalog-section">
    <div class="wrap">
      <div class="section-head section-head--row"><div><h2>{esc(category['name'].title())} product range</h2><p>Compare model names, dimensions and export packing data.</p></div><a class="link" href="/#sales">Talk to export sales</a></div>
      <div class="catalog-product-grid">{cards}</div>
    </div>
  </section>
</main>
"""
            + footer_html(catalog["categories"])
        )
        write_page(PRODUCT_ROOT / category["slug"] / "index.html", page)


def build_product_pages(
    catalog: dict[str, Any],
    products_by_number: dict[int, dict[str, Any]],
) -> None:
    for product in catalog["products"]:
        category = next(
            item for item in catalog["categories"] if item["slug"] == product["category_slug"]
        )
        copy = CATEGORY_COPY[category["slug"]]
        canonical = absolute(product_url(product))
        small, large, srcset = image_paths(product)
        related = [
            products_by_number[number]
            for number in category["product_numbers"]
            if number != product["number"]
        ][:3]
        related_cards = "".join(product_card(item) for item in related)
        spec_rows = [
            f"<div><dt>Catalogue item</dt><dd>{int(product['number']):03d}</dd></div>",
            f"<div><dt>Dimensions</dt><dd>{esc(product['dimensions_cm'])} cm</dd></div>",
            f"<div><dt>Packing</dt><dd>{esc(dimension_text(product['packing_cm']))}</dd></div>",
            f"<div><dt>Shipping volume</dt><dd>{esc(product['cbm'])} CBM</dd></div>",
        ]
        if product["material"]:
            spec_rows.insert(
                1,
                f"<div><dt>Material</dt><dd>{esc(product['material'])}</dd></div>",
            )
        if product["gross_weight_kg"]:
            spec_rows.append(
                f"<div><dt>Gross weight</dt><dd>{esc(product['gross_weight_kg'])} kg</dd></div>"
            )
        if product["power_w"]:
            spec_rows.append(
                f"<div><dt>Power</dt><dd>{esc(f'{product['power_w']:g} W')}</dd></div>"
            )
        spec_rows.append(
            f"<div><dt>Sales unit</dt><dd>{esc(product['unit'])}</dd></div>"
        )
        spec_html = "\n        ".join(spec_rows)
        properties = [
            {
                "@type": "PropertyValue",
                "name": "Catalogue item",
                "value": f"{int(product['number']):03d}",
            },
            {"@type": "PropertyValue", "name": "Dimensions", "value": f"{product['dimensions_cm']} cm"},
            {"@type": "PropertyValue", "name": "Packing", "value": dimension_text(product["packing_cm"])},
            {"@type": "PropertyValue", "name": "CBM", "value": product["cbm"]},
        ]
        if product["material"]:
            properties.insert(
                1,
                {
                    "@type": "PropertyValue",
                    "name": "Material",
                    "value": product["material"],
                },
            )
        if product["gross_weight_kg"]:
            properties.append(
                {
                    "@type": "PropertyValue",
                    "name": "Gross weight",
                    "value": f"{product['gross_weight_kg']} kg",
                }
            )
        if product["power_w"]:
            properties.append(
                {"@type": "PropertyValue", "name": "Power", "value": f"{product['power_w']:g} W"}
            )
        product_schema = {
            "@type": "Product",
            "@id": f"{canonical}#product",
            "name": product["name"],
            "identifier": {
                "@type": "PropertyValue",
                "propertyID": "Qijiang catalogue item",
                "value": f"{int(product['number']):03d}",
            },
            "description": product["description"],
            "image": [absolute(f"/assets/catalog/{product['number']:02d}.webp")],
            "category": copy["title"],
            "brand": {"@id": f"{BASE_URL}/#organization"},
            "countryOfOrigin": "CN",
            "additionalProperty": properties,
        }
        if product["material"]:
            product_schema["material"] = product["material"]
        structured = {
            "@context": "https://schema.org",
            "@graph": [
                organization_json(),
                website_json(),
                person_json(),
                product_schema,
                {
                    "@type": "WebPage",
                    "@id": f"{canonical}#webpage",
                    "url": canonical,
                    "name": product["name"],
                    "isPartOf": {"@id": f"{BASE_URL}/#website"},
                    "mainEntity": {"@id": f"{canonical}#product"},
                },
                breadcrumb_json(
                    [
                        ("Home", f"{BASE_URL}/"),
                        ("Products", f"{BASE_URL}/products/"),
                        (copy["title"], absolute(category_url(category))),
                        (product["name"], canonical),
                    ]
                ),
            ],
        }
        whatsapp_text = quote(
            f"Hello Xiaoming, I am interested in {catalogue_item(product)}: {product['name']}."
        )
        page = (
            page_head(
                f"{product['name']} | Qijiang Arcade",
                f"{sentence(product['description'])} {catalogue_item(product)} from Guangzhou Qijiang Technology, {product['dimensions_cm']} cm.",
                canonical,
                large,
                structured,
            )
            + header_html()
            + f"""
<main id="top">
  <section class="catalog-section product-detail">
    <div class="wrap">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/products/">Products</a><span>/</span><a href="{category_url(category)}">{esc(copy['title'])}</a><span>/</span><span>{esc(product['name'])}</span></nav>
      <div class="product-detail__grid">
        <figure class="product-detail__media">
          <img src="{large}" srcset="{small} 320w, {large} 600w" sizes="(max-width: 899px) 100vw, 55vw" alt="{esc(product['name'])} commercial arcade machine" width="600" height="450" fetchpriority="high" decoding="async">
        </figure>
        <div class="product-detail__copy">
          <p class="catalog-model">{catalogue_item(product)} · {esc(copy['title'])}</p>
          <h1>{esc(product['name'])}</h1>
          <p class="t-lead">{esc(product['description'])}</p>
          <div class="btn-row"><a class="btn btn--primary" href="/contact">Request a quote</a><a class="btn btn--secondary" href="https://wa.me/8617691342432?text={whatsapp_text}">WhatsApp Xiaoming</a></div>
        </div>
      </div>
    </div>
  </section>
  <section class="catalog-section ground-surface">
    <div class="wrap product-specs">
      <div>
        <p class="t-label">Specifications</p>
        <h2>Cabinet and export data</h2>
        <p>Specifications below are taken from the current Qijiang product catalogue. Export price is quoted for the requested model, quantity, destination country and voltage.</p>
      </div>
      <dl class="catalog-spec-list">
        {spec_html}
      </dl>
    </div>
  </section>
  <section class="catalog-section">
    <div class="wrap">
      <div class="section-head"><h2>More {esc(copy['title'].lower())}</h2><p>Compare other models in this category.</p></div>
      <div class="catalog-product-grid">{related_cards}</div>
    </div>
  </section>
</main>
"""
            + footer_html(catalog["categories"])
        )
        write_page(PRODUCT_ROOT / category["slug"] / product["slug"] / "index.html", page)


def build_sitemap(catalog: dict[str, Any]) -> None:
    locations = [
        f"{BASE_URL}/",
        f"{BASE_URL}/xiaoming-zhuang",
        f"{BASE_URL}/contact",
        f"{BASE_URL}/privacy",
        f"{BASE_URL}/credits",
        f"{BASE_URL}/products/",
    ]
    for category in catalog["categories"]:
        locations.append(absolute(category_url(category)))
    for product in catalog["products"]:
        locations.append(absolute(product_url(product)))
    entries = "\n".join(
        f"  <url><loc>{esc(location)}</loc><lastmod>2026-11-24</lastmod></url>"
        for location in locations
    )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n",
        encoding="utf-8",
        newline="\n",
    )


def write_image_map(catalog: dict[str, Any]) -> None:
    rows = "\n".join(
        f"| {catalogue_item(product)} | {product['number']} | `{product['name']}` | "
        f"`assets/catalog/{product['number']:02d}.webp` |"
        for product in catalog["products"]
    )
    IMAGE_MAP_PATH.write_text(
        "# Qijiang Product Image Map\n\n"
        f"Source document SHA-256: `{catalog['source']['source_document_sha256']}`\n\n"
        "Each public catalogue item maps to the same PDF row and extracted product image. The PDF "
        "does not provide manufacturer model codes. Prices are not included in the public image "
        "map or website.\n\n"
        "| Catalogue item | PDF row | Product name | Public image |\n"
        "|---|---:|---|---|\n"
        f"{rows}\n",
        encoding="utf-8",
        newline="\n",
    )


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build() -> None:
    catalog = load_catalog()
    products_by_number = {product["number"]: product for product in catalog["products"]}
    if PRODUCT_ROOT.exists():
        shutil.rmtree(PRODUCT_ROOT)
    PRODUCT_ROOT.mkdir(parents=True)
    build_catalog_page(catalog, products_by_number)
    build_home_page(catalog, products_by_number)
    build_category_pages(catalog, products_by_number)
    build_product_pages(catalog, products_by_number)
    update_existing_pages(catalog)
    build_sitemap(catalog)
    write_image_map(catalog)


if __name__ == "__main__":
    build()
    print("Built 1 catalogue hub, 10 category pages, 60 product pages, and sitemap.xml")
