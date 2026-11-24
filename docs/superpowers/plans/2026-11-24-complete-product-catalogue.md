# Complete Product Catalogue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the partial product presentation with a complete, crawlable catalogue of the 60
models in `QIJIANG_Quotation_.pdf`.

**Architecture:** Keep the existing dependency-free static site. Extract the PDF into one reviewed
JSON source, then generate a catalogue index, ten category pages, and 60 product pages from that
source. The generated pages use the existing visual system, product-specific JSON-LD, responsive
images, canonical URLs, and sitemap entries.

**Tech Stack:** Python standard library for page generation, Pillow 12.2.0 for development-only image
validation, existing static HTML/CSS, PDF-extracted product images, Google/OpenAI-compatible crawl
metadata.

**Spec:** `docs/superpowers/specs/2026-11-24-product-image-map.md`

## Evidence

- [withastro/astro](https://github.com/withastro/astro), commit
  `28a925e016fa160a8cf60bbd9024af92b26dc25b`, MIT license. Relevant files:
  `examples/blog/src/content.config.ts` and `examples/blog/src/pages/blog/[...slug].astro`.
  Pattern: define typed content once, query the collection, and generate every route from it.
- [11ty/buildawesome](https://github.com/11ty/buildawesome), commit
  `7c4465157465ed78a319d1d5ad478dcb0a3726bd`, MIT license. Relevant files:
  `src/Plugins/Pagination.js`, `test/CoreTest-ComputedData.js`, and
  `test/stubs/pagination-templatecontent/index.njk`. Pattern: page generation from a data set, with
  automated tests.
- [vercel/commerce](https://github.com/vercel/commerce), commit
  `f7521d57d29f0eb3d23c1399cf9bb299d61fcd21`, MIT license. Relevant files:
  `app/product/[handle]/page.tsx`, `app/search/[collection]/page.tsx`, and
  `components/layout/product-grid-items.tsx`. Pattern: one collection route, reusable product cards,
  one product-detail route with Product JSON-LD, and related products. The repository is archived,
  so it is a layout/reference source rather than a runtime dependency.
- Google product structured data:
  <https://developers.google.com/search/docs/appearance/structured-data/product>

## Public Data Rules

- Publish the PDF catalogue item reference, product name, description, and source-stated material,
  dimensions, packing dimensions, CBM, gross weight, power, unit type, and product image.
- Do not invent a model number or SKU: the source PDF exposes row numbers but no manufacturer model
  code.
- Do not publish the quotation number, validity date, unit prices, payment terms, or customer data.
- Use the latest PDF as the source of truth. Its SHA-256 is
  `0dcaf0817b4ce3b39ebac8045cf367e4ea8bdcdb1d438139c4b6f1835ca05fb7`.
- Every product image must map to the row number in the PDF and be checked against the extracted
  image sequence.
- All catalogue pages are static and crawlable without JavaScript.

## Tasks

### Task 1: Canonical Catalogue Data

**Files:**
- Create: `data/catalog.json`
- Create: `scripts/validate_catalog.py`
- Test: `tmp/pdfs/build_catalog_data.py`

- [x] Extract all 60 product rows from the PDF.
- [x] Require 60 unique product numbers, ten categories, and no blank required fields.
- [x] Require 60 matching image files.
- [x] Verify catalogue facts against the rendered PDF pages.

### Task 2: Responsive Product Images

**Files:**
- Create: `site/assets/catalog/01.webp` through `60.webp`
- Create: `site/assets/catalog/01-320.webp` through `60-320.webp`

- [x] Extract the 60 embedded product images in PDF row order.
- [x] Inspect a 10-by-6 contact sheet.
- [x] Export a 600x450 catalogue image and a 320x240 mobile variant for each model.
- [x] Verify every image is non-empty and has the expected dimensions.

### Task 3: Generate the Catalogue

**Files:**
- Create: `scripts/build_catalog.py`
- Create: `site/assets/catalog.css`
- Generate: `site/products/index.html`
- Generate: `site/products/<category>/index.html`
- Generate: `site/products/<category>/<product>/index.html`
- Generate: `site/sitemap.xml`

- [x] Generate one category route and one product route for every verified data row.
- [x] Add canonical, Open Graph, Product, ItemList, CollectionPage, Organization, WebSite, Person,
  and BreadcrumbList metadata.
- [x] Add quote and WhatsApp actions without exposing prices.
- [x] Link each product to related products in the same category.

### Task 4: Integrate Existing Pages

**Files:**
- Modify: `site/index.html`
- Modify: `site/xiaoming-zhuang.html`
- Modify: `site/contact.html`
- Modify: `site/llms.txt`
- Create: `site/_redirects`

- [x] Change the homepage total from 13 models to 60 models across ten categories.
- [x] Link product navigation to the generated catalogue.
- [x] Redirect the old `/air-hockey-tables` route to the new category page.
- [x] Update public contact and profile pages to reference the complete catalogue.

### Task 5: Verification

- [x] Run `python scripts/validate_catalog.py`.
- [x] Run `python scripts/build_catalog.py`.
- [x] Parse all generated JSON-LD and XML.
- [ ] Verify every generated product page and image over live HTTP after deployment.
- [x] Run copy lint on representative catalogue pages.
- [x] Run browser checks at 1440, 1024, 820, 768, 390, and 320 pixels.
- [x] Run the performance check.
- [ ] Deploy to Cloudflare Pages and submit the refreshed sitemap with IndexNow.
