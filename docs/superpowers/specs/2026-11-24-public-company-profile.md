# Public Company Profile Specification

## Outcome

Publish a small English website that makes Guangzhou Qijiang Technology Co., Ltd. and Xiaoming Zhuang understandable as one company-person-product entity. The site must give buyers and AI/search crawlers a plain HTML source for the company name, sales contact, air hockey model range, arcade equipment categories, and Guangzhou location.

## Confirmed Public Data

- Company: Guangzhou Qijiang Technology Co., Ltd.
- Product scope: commercial arcade and amusement equipment.
- Confirmed range from the current quote set: air hockey, skee-ball, video bowling, basketball, boxing and strength games, football tables, and racing/other arcade equipment.
- Sales contact: Xiaoming Zhuang, Export Sales.
- Email: zhuangxiaoming40@gmail.com.
- Phone and WhatsApp: +86 176 9134 2432.
- Location: Guangzhou, Guangdong, China.

## Source Material

- `C:\Users\123\Documents\Codex\2026-11-11\new-chat\work\quote_build\quotation_data.json`
- `C:\Users\123\Documents\Codex\2026-11-11\new-chat\work\catalog_quote\assets_prepared\item_*.jpg`
- The company and product profile in the active `AGENTS.md`.

## Pages

1. `index.html`: commercial arcade equipment manufacturer, air hockey range, FEC use cases, and direct contact.
2. `air-hockey-tables.html`: commercial air hockey tables across arcade, FEC, bowling, family and children's formats.
3. `xiaoming-zhuang.html`: sales contact entity page.
4. `contact.html`: direct quote request methods.
5. `privacy.html`: what the static site does and does not collect.

## Search Entity Graph

- `Organization` for Guangzhou Qijiang Technology Co., Ltd.
- `WebSite` and `WebPage` for each public page.
- `Person` for Xiaoming Zhuang with `worksFor` and `knowsAbout`.
- `Product` and `ItemList` for commercial air hockey models.
- `BreadcrumbList` for inner pages.

No `Offer`, price, availability, review, rating, credential, or customer claim is fabricated.

## Design

- Page type: `product`.
- Site kind: `other`.
- Product photography: the client's existing catalogue images only.
- Tone: technical and factual, with plain product nouns and specifications.
- Main action: `Request a quote`.
- Responsive targets: 1440, 1024, 820, 768, 390, and 320.

## Acceptance

- All public pages return HTTP 200 locally and after deployment.
- Every product name, dimension, power value, email, and phone matches the verified source.
- Robots policy allows Googlebot, Bingbot, OAI-SearchBot, and ChatGPT-User; GPTBot remains independent and disallowed.
- Structured data parses without errors.
- Internal links, email links, and WhatsApp links are valid.
- No customer names, quote totals, private buyer data, or unrelated files are published.
- Deployment is stopped if Cloudflare authentication is unavailable; the static package remains ready for upload.
