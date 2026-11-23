# Public Company Profile and Product Discoverability Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish an indexable English website for Guangzhou Qijiang Technology Co., Ltd. and Xiaoming Zhuang that states the company's real products and contact details, and is structured for search engines and ChatGPT search.

**Architecture:** A dependency-free static site in `site/`, built from the installed `design-taste-frontend` kit. The site has a company landing page, a commercial air hockey product page, a personal sales-contact page, and a direct contact page. Each page is plain HTML, links only to real local pages or real contact destinations, and includes crawlable copy. Deployment target is Cloudflare Pages Direct Upload; GitHub is a public source backup only because GitHub Pages documents a commercial-site restriction.

**Tech Stack:** Static HTML, CSS, JavaScript from the installed design kit, JSON-LD, `robots.txt`, `sitemap.xml`, Cloudflare Pages.

**Spec:** `docs/superpowers/specs/2026-11-24-public-company-profile.md`

## Global Constraints

- Public identity: `Guangzhou Qijiang Technology Co., Ltd.` and `Xiaoming Zhuang`.
- Public role: `Export Sales`.
- Public email: `zhuangxiaoming40@gmail.com`.
- Public phone and WhatsApp: `+86 176 9134 2432`.
- Public location: `Guangzhou, Guangdong, China`.
- Do not publish street addresses, certificates, customer names, quotes, reviews, prices, MOQ, lead times, ratings, or ownership claims that are not present in local evidence.
- Product facts come only from `quotation_data.json` and the existing product images.
- Main action on every page: `Request a quote`.
- Write only inside `site/`, `docs/superpowers/plans/`, and `docs/superpowers/specs/`.
- Do not modify the frozen Google Maps workflow, `gmap-client-dev`, its skill files, browser profile, or generated customer workbooks.
- Deploy to Cloudflare Pages; do not deploy a commercial site to GitHub Pages or Vercel Hobby.
- Allow `Googlebot`, `Bingbot`, `OAI-SearchBot`, and `ChatGPT-User` in robots policy. Keep `GPTBot` training access independent and disallowed unless separately authorized.
- Use a real browser at 1440, 1024, 820, 768, 390, and 320 widths for final verification.

## Review Focus

- Personal contact details are public by explicit user request; verify no customer records, quote prices, or private files are copied into the site.
- Search metadata, canonical URLs, sitemap, and structured data must all refer to the same deployed origin.
- Product names, dimensions, and power values must match the existing quotation JSON exactly.
- Internal links and contact links must resolve; mailto and WhatsApp must use the real supplied destinations.
- The site must remain usable without JavaScript and under reduced motion.

---

### Task 1: Scaffold and Configure the Static Site

**Files:**
- Create: `docs/superpowers/specs/2026-11-24-public-company-profile.md`
- Create: `site/assets/` from `C:\Users\123\.agents\skills\taste-skill\assets`
- Create: `site/assets/img/` with selected client-owned product images
- Create: `site/favicon.svg`
- Test: `node C:/Users/123/.agents/skills/taste-skill/scripts/gate.mjs --start site/index.html --kind product --category "Commercial arcade equipment" --primary "Request a quote"`

- [ ] Copy the design-kit assets into `site/assets/`.
- [ ] Copy only the selected product images into `site/assets/img/`.
- [ ] Create a simple QJ favicon from the kit's mark system.
- [ ] Arm the design finish gate before the first page exists.

### Task 2: Build the Company Landing Page

**Files:**
- Create: `site/index.html`
- Consume: `site/assets/img/`
- Test: `node C:/Users/123/.agents/skills/taste-skill/scripts/copy-lint.mjs site/index.html --kind product`

- [ ] Write the page copy with the product category and buyer in the h1.
- [ ] Build the product hero, air hockey line-up, FEC use cases, and Xiaoming Zhuang contact section.
- [ ] Add Organization, WebSite, Person, and Product ItemList JSON-LD.
- [ ] Add Open Graph metadata and a self-canonical placeholder to be finalized after deployment.
- [ ] Run copy lint and inspect at all required widths.

### Task 3: Build the Commercial Air Hockey Page

**Files:**
- Create: `site/air-hockey-tables.html`
- Consume: `site/assets/img/`
- Test: `node C:/Users/123/.agents/skills/taste-skill/scripts/copy-lint.mjs site/air-hockey-tables.html --kind product`

- [ ] Add a focused h1 for commercial air hockey tables.
- [ ] Show six model cards with real images and actual dimensions and power values.
- [ ] Add a compact specification table for the remaining quote-list models.
- [ ] Add a product FAQ that answers only facts present in the source data.
- [ ] Add Product/ItemList, BreadcrumbList, Organization, and Person JSON-LD.

### Task 4: Build the Personal Profile Page

**Files:**
- Create: `site/xiaoming-zhuang.html`
- Test: `node C:/Users/123/.agents/skills/taste-skill/scripts/copy-lint.mjs site/xiaoming-zhuang.html --kind service`

- [ ] State the person's name, role, company, location, product responsibilities, email, phone, and WhatsApp.
- [ ] Link to real company and product pages.
- [ ] Add Person, Organization, ProfilePage, and BreadcrumbList JSON-LD.
- [ ] Use no invented portrait, biography, credentials, or customer claims.

### Task 5: Build Contact and Crawl Files

**Files:**
- Create: `site/contact.html`
- Create: `site/privacy.html`
- Create: `site/robots.txt`
- Create: `site/sitemap.xml`
- Create: `site/llms.txt`
- Create: `site/_headers`
- Create: `site/404.html`

- [ ] Publish direct email, phone, and WhatsApp contact details.
- [ ] State plainly what the site does and does not collect.
- [ ] Allow Googlebot, Bingbot, OAI-SearchBot, and ChatGPT-User; disallow GPTBot training crawl.
- [ ] List every production page in sitemap.xml using the final deployed origin.
- [ ] Add security headers and a useful 404 page.

### Task 6: Verify Locally

**Files:**
- Test: `site/index.html`
- Test: `site/air-hockey-tables.html`
- Test: `site/xiaoming-zhuang.html`
- Test: `site/contact.html`

- [ ] Run `copy-lint.mjs` on all content pages.
- [ ] Run `consistency.mjs` with widths `1440,1024,820,768,390`.
- [ ] Run `assets/layout/check.mjs` with sizes `1440x900,1024x768,820x1180,768x1024,390x844`.
- [ ] Run `perf.mjs`.
- [ ] Run the design finish gate and resolve all actionable failures.
- [ ] Verify every link, mailto, and WhatsApp destination.
- [ ] Validate all JSON-LD blocks and XML.

### Task 7: Publish Source and Deploy

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: public GitHub repository
- Deploy: Cloudflare Pages project

- [ ] Create the Git repository and commit the verified site.
- [ ] Create a public GitHub source repository and push the verified commit.
- [ ] Authenticate Cloudflare Pages or stop if no authenticated account is available.
- [ ] Deploy `site/` using Direct Upload.
- [ ] Fetch the live HTTPS origin and verify all pages and metadata.
- [ ] Update canonical URLs and sitemap to the final live origin, then redeploy if the temporary origin differs from the planned origin.

### Task 8: Independent Review and Acceptance

**Files:**
- Review: all changed files and the live deployment

- [ ] Dispatch an independent reviewer with the original request, source evidence, diff, and live URL.
- [ ] Fix critical and high findings.
- [ ] Re-run fresh HTTP, browser, copy, layout, structured-data, robots, sitemap, and link checks.
- [ ] Report official/repository facts, local verification, deployment state, and remaining constraints separately.
