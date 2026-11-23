# Search and ChatGPT Discoverability Evidence

Date: 2026-11-24

Goal: publish a crawlable public identity for Guangzhou Qijiang Technology Co., Ltd. and
Xiaoming Zhuang, without promising search rank, index inclusion, or first-place placement.

## Adopted sources

### 1. OpenAI crawler controls

- Source: <https://developers.openai.com/api/docs/bots>
- Type: official documentation
- Relevant facts: `OAI-SearchBot` controls inclusion in ChatGPT search answers; `GPTBot` controls
  model-training access; the controls are independent.
- Applied: `robots.txt` allows `OAI-SearchBot` and `ChatGPT-User` while disallowing `GPTBot`.
- Limitation: allowing a crawler does not guarantee indexing or ranking.

### 2. Google AI features and Search essentials

- Sources:
  - <https://developers.google.com/search/docs/appearance/ai-features>
  - <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- Type: official documentation
- Relevant facts: Google says there are no special optimizations required for its AI features beyond
  normal Search fundamentals; useful, crawlable text and standard technical SEO still matter.
- Applied: plain-text company and product information, internal links, canonical URLs, sitemap,
  robots policy, and useful product specifications.
- Limitation: AI-feature visibility is not separately controllable or guaranteed.

### 3. Google Organization structured data

- Source: <https://developers.google.com/search/docs/appearance/structured-data/organization>
- Type: official documentation
- Applied: `Organization` data contains the legal name, URL, description, email, telephone, address,
  and a stable `@id`.
- Limitation: structured data helps machines interpret the page but does not guarantee a rich result.

### 4. Schema.org vocabulary

- Repository: <https://github.com/schemaorg/schemaorg>
- Commit reviewed: `ba90187cfadd1b10aa76bcf879910ce05d64960d`
- Relevant files: `data/releases/30.1/schemaorg-current-https.jsonld` and release examples
- License: Apache-2.0
- CI evidence: `.github/workflows/ci_tests.yml`
- Applied: `Organization`, `Person`, `Product`, `ItemList`, `WebPage`, `ProfilePage`, `ContactPage`,
  and `BreadcrumbList` types.
- Limitation: vocabulary definitions do not validate the accuracy of the business data; business
  facts still require local evidence.

### 5. Google-maintained TypeScript schema examples

- Repository: <https://github.com/google/schema-dts>
- Commit reviewed: `0dc1d1f518af5a727ada9d162c714ddf74710686`
- Relevant file: `README.md`
- License: Apache-2.0
- CI evidence: `.github/workflows/ci.yml`
- Applied: stable `@id` references in one JSON-LD `@graph`, with Person connected to Organization and
  WebPage.
- Limitation: examples describe shape and linking, not guaranteed ranking.

### 6. Cloudflare Pages Direct Upload

- Source: <https://developers.cloudflare.com/pages/get-started/direct-upload/>
- Type: official documentation
- Relevant facts: supports deploying pre-built static files, project domains, custom domains,
  production deployments, and rollback.
- Applied: the production site is a static Cloudflare Pages deployment at
  `https://qijiang-arcade.pages.dev/`.
- Limitation: availability and quota remain subject to Cloudflare account and plan terms.

### 7. Google Search Console ownership verification

- Source: <https://support.google.com/webmasters/answer/9008080#html_verification>
- Type: official documentation
- Applied: a URL-prefix property was verified with the generated HTML file.
- Verified live file:
  `https://qijiang-arcade.pages.dev/google7d30a7bf7e88042e.html`
- Limitation: verification and live URL testing do not equal indexing.

### 8. IndexNow

- Source: <https://www.indexnow.org/documentation>
- Type: official protocol documentation
- Relevant facts: an IndexNow key is published in a text file, and a POST request supplies the host,
  key location, and URL list.
- Applied: public key
  `https://qijiang-arcade.pages.dev/5d25396680c6579654783df5540d07e4.txt`; the submission endpoint
  returned HTTP 202.
- Limitation: acceptance means the URLs were received; it does not prove indexing or rank.

### 9. Responsive image delivery

- Sources:
  - <https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images>
  - <https://web.dev/learn/images/>
- Type: official browser and web-platform documentation
- Relevant facts: `srcset` and `sizes` let the browser choose an appropriately sized image instead
  of downloading the largest source for every viewport.
- Applied: 320 px and 640 px product-image variants plus 700 px and 1200 px hero variants.
- Product identity is controlled by the explicit item-number map in
  `docs/superpowers/specs/2026-11-24-product-image-map.md`; the older catalogue export numbering is
  not used for public labels.
- Local verification: the performance checker no longer reports any oversized-image failures at
  1440 px or 390 px; home-page transfer dropped to about 605 KiB and 346 KiB respectively.
- Limitation: device pixel ratio can still select the larger candidate; actual transfer varies by
  browser and connection.

### 10. Design-taste frontend kit

- Repository: <https://github.com/Leonxlnx/taste-skill>
- Commit reviewed: `6c0b5c78f5d31776e2210305abaa210cdc0030bf`
- Relevant paths:
  - `skills/taste-skill/SKILL.md`
  - `skills/taste-skill/assets/system.css`
  - `skills/taste-skill/assets/layout/layout.css`
  - `skills/taste-skill/assets/motion/motion.css`
  - `skills/taste-skill/assets/moments/moments.js`
  - `tests/`
  - `.github/workflows/check-skills.yml`
- License: MIT
- Applied: the static layout system, motion layer, and local browser checkers. The site excludes
  demo pages, stock-photo directories, and unpublished design artifacts from the production build.
- Verification: the copied license is published at
  `https://qijiang-arcade.pages.dev/assets/LICENSE.taste-skill.txt`.
- Limitation: this is a design and validation kit, not a content source. All company and product
  claims still come from user-owned quote data.

## Decision record

- Use Cloudflare Pages for production rather than GitHub Pages because GitHub's official usage limits
  exclude commercial website hosting.
- Publish only company names, role, business email, business phone/WhatsApp, Guangzhou location, and
  product facts already present in the user's quote data.
- Do not publish prices, customer names, quote references, certificates, ratings, reviews, or
  unverified social profiles.
- Keep `GPTBot` disallowed for model training while allowing `OAI-SearchBot` for ChatGPT search.
- Treat indexing, ranking, and ChatGPT citation as pending external outcomes, never as guaranteed
  results.

## Verification boundary

The site's crawlability, HTTP availability, robots policy, sitemap, canonical URLs, structured-data
syntax, and ownership verification can be tested. Google indexing, Bing indexing, search position,
and inclusion in a future ChatGPT answer cannot be guaranteed by the publisher.

## Verification record

Verified on 2026-11-24 against the public Cloudflare Pages deployment:

- The Cloudflare production deployment is published from the repository's final verified `main`
  revision.
- Core page, robots, sitemap, Google verification, and IndexNow key requests return HTTP 200.
- Google Search Console accepted the URL-prefix property after the verification file was live.
- Google's live URL test reported that the home page could be indexed.
- Google Search Console accepted `sitemap.xml`; processing is pending.
- IndexNow accepted the submitted URL list.
- All 21 published product originals match the exact `quotation_data.json` image source for the
  corresponding item number; the older catalogue export order is not used.
- JSON-LD parses on the home, air-hockey, profile, and contact pages.
- `copy-lint.mjs` reports zero failures and zero warnings for all content pages.
- Browser consistency checks at 1440 px and 390 px report zero blocking failures for the home,
  air-hockey, profile, and contact pages after authorized business-contact exceptions are allowed.
- The responsive-image performance check reports no oversized-image failure at 1440 px or 390 px
  after image variants were added.
- The strict design checker still reports intermediate-width screen-rhythm and image-source
  warnings. These do not block page access, contact actions, crawling, or indexing, and are retained
  as non-blocking design debt rather than hidden or waived as search evidence.
