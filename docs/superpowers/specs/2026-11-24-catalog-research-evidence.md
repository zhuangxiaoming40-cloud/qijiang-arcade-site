# Catalogue Website Research Evidence

Date: 2026-11-24

## Decision

Use one checked JSON dataset as the source of truth, then generate the catalogue index, category
pages, product pages, structured data, and sitemap from that dataset. This is the common pattern in
the high-star projects below. The current site stays static and gains no runtime dependency.

## Verified references

### Astro content collections and dynamic routes

- Repository: <https://github.com/withastro/astro>
- Commit reviewed: `28a925e016fa160a8cf60bbd9024af92b26dc25b`
- Stars at review: 64,157
- License: MIT (`LICENSE` in the repository)
- Relevant files:
  - `examples/blog/src/content.config.ts`
  - `examples/blog/src/pages/blog/[...slug].astro`
  - `packages/astro/src/content/runtime.ts`
- Evidence: the repository has a large test suite under `packages/astro/test` and runs CI from
  `.github/workflows`.
- Adopted pattern: define a typed collection, call `getCollection`, and map records to routes with
  `getStaticPaths`.

### Eleventy data pagination

- Repository: <https://github.com/11ty/buildawesome>
- Commit reviewed: `7c4465157465ed78a319d1d5ad478dcb0a3726bd`
- Stars at review: 20,056
- License: MIT
- Relevant files:
  - `src/Plugins/Pagination.js`
  - `test/CoreTest-ComputedData.js`
  - `test/stubs/pagination-templatecontent/index.njk`
- Evidence: pagination behavior is covered by repository tests.
- Adopted pattern: create all routes from one data set instead of maintaining repeated HTML.

### Vercel Commerce storefront structure

- Repository: <https://github.com/vercel/commerce>
- Commit reviewed: `f7521d57d29f0eb3d23c1399cf9bb299d61fcd21`
- Stars at review: 14,306
- License: MIT (`license.md` in the repository)
- Relevant files:
  - `app/search/[collection]/page.tsx`
  - `components/layout/product-grid-items.tsx`
  - `app/product/[handle]/page.tsx`
  - `components/product/gallery.tsx`
- Adopted pattern: one collection template, one reusable product-card component, one product route
  with Product JSON-LD and related products.
- Limitation: the upstream repository is archived and its example is commerce-oriented with price
  and availability data. The Qijiang public catalogue deliberately omits prices and availability
  claims, so this repository was used as a layout and route-structure reference rather than a live
  dependency.

### Google product structured data

- Source: <https://developers.google.com/search/docs/appearance/structured-data/product>
- Type: official documentation
- Applied: Product name, description, image, brand, category, material, dimensions, packing, CBM,
  and weight where the source provides them. No SKU is claimed because the quotation exposes only
  row numbers; no Offer object is emitted without a public price.

### Pillow validation dependency

- Package: `Pillow==12.2.0`
- Source: <https://pypi.org/project/pillow/12.2.0/>
- Upstream repository: <https://github.com/python-pillow/Pillow>
- License: MIT-CMU
- Python requirement: 3.10 or later
- Dependency boundary: development validation only; it is not copied to `dist` and the deployed
  site has no runtime dependency on Pillow.
- Applied: `scripts/validate_catalog.py` reads every WebP asset to verify its exact responsive
  dimensions.

## Resulting structure

- `data/catalog.json`: one record for each of the 60 PDF rows, excluding prices and customer data.
- `site/products/index.html`: catalogue hub with ten category cards and featured products.
- `site/products/<category>/index.html`: ten category pages.
- `site/products/<category>/<product>/index.html`: 60 product pages.
- `site/sitemap.xml`: regenerated with 76 indexable URLs.
- `scripts/build_catalog.py`: deterministic generator.
- `scripts/validate_catalog.py`: count, image, JSON-LD, sitemap, private-data, and local-link checks.

## Source-data boundary

- Source PDF SHA-256:
  `0dcaf0817b4ce3b39ebac8045cf367e4ea8bdcdb1d438139c4b6f1835ca05fb7`
- The PDF itself is not copied into the public repository.
- The PDF has row numbers but no manufacturer model codes. Public pages use `Catalogue item 001`
  through `Catalogue item 060` and do not publish a fabricated model number or SKU.
- Prices, quotation number, payment terms, customer data, and source filesystem paths are excluded
  from the public build.
