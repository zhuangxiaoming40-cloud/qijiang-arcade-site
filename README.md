# Qijiang public company profile

Static public profile for Guangzhou Qijiang Technology Co., Ltd. and Xiaoming Zhuang.

Live website: <https://qijiang-arcade.pages.dev/>

Public contact: Xiaoming Zhuang, Export Sales, <zhuangxiaoming40@gmail.com>, WhatsApp <https://wa.me/8617691342432>.

## Site

- Company landing page: `site/index.html`
- Complete catalogue: `site/products/index.html`
- Ten category pages and 60 product pages: generated under `site/products/`
- Xiaoming Zhuang profile: `site/xiaoming-zhuang.html`
- Contact page: `site/contact.html`
- Crawl files: `site/robots.txt`, `site/sitemap.xml`, `site/llms.txt`
- Source catalogue data: `data/catalog.json`

## Build and verify

```powershell
python -m pip install -r requirements-dev.txt
python scripts/build_catalog.py
python -m unittest tests.test_catalog_build -v
python scripts/validate_catalog.py
python scripts/build_site.py
```

The catalogue generator follows the data-driven patterns used by Astro content collections and
11ty pagination, with the collection/product layout used by Vercel Commerce. Prices and customer
data from the source quotation are intentionally excluded from the public build. The source PDF
has catalogue row numbers but no manufacturer model codes, so public pages use `Catalogue item`
references and do not publish a fabricated SKU. Pillow is a development-only validation dependency;
the deployed site has no runtime dependency.

## Deployment

The publication target is Cloudflare Pages Direct Upload. GitHub Pages is intentionally not used because its official usage limits exclude running a commercial website.

Expected public origin:

`https://qijiang-arcade.pages.dev/`

The production build contains only the public pages, crawl files, local assets, and the Google
verification file. Work-in-progress design-kit files under `site/.taste-skill/` are excluded.
