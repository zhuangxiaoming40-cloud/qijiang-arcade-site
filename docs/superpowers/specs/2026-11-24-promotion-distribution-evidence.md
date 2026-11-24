# Promotion and Distribution Evidence

Date: 2026-11-24

## Verified official sources

### Organization identity

- Schema.org, `sameAs`: <https://schema.org/sameAs>
  - Primary definition: a URL of a reference page that unambiguously identifies the item, such as
    its official website, Wikipedia page or Wikidata entry.
- Google Search Central, Organization structured data:
  <https://developers.google.com/search/docs/appearance/structured-data/organization>
  - The `sameAs` field can point to an organization's profile on a social media or review site,
    and multiple profile URLs are allowed.
  - Google recommends describing the organization's URL, name, logo, contact and address
    consistently in Organization structured data.
- Applied pattern: add the verified official Facebook Page URL as `Organization.sameAs` on the
  public site and expose the same URL visibly in contact/footer navigation.

### Search quality and link-safety boundary

- Google Search Essentials: <https://developers.google.com/search/docs/essentials>
- Google spam policies: <https://developers.google.com/search/docs/essentials/spam-policies>
  - The spam policy names doorway abuse, link spam, scraped content and other deceptive
    manipulation as violations.
- Applied boundary: publish first-party product facts and human-reviewed distribution, avoid
  automated mass posting, fake profiles, paid link networks and generated doorway pages.

### IndexNow

- Official documentation: <https://www.indexnow.org/documentation>
  - A successful submission returns HTTP 200, but that means only that the search engine received
    the URL set; it is not evidence of indexing or ranking.
- Applied pattern: send the complete public sitemap URL set after deployment, then verify the
  published endpoints separately and report indexing as pending.

### ChatGPT web search and crawler access

- OpenAI Help Center, Searching the web with ChatGPT:
  <https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt>
  - ChatGPT searches the web and can cite sources.
  - Placement is not guaranteed.
  - Eligibility requires allowing `OAI-SearchBot` to crawl and allowing OpenAI's published
    search-bot IP addresses through the host or CDN.
- Applied boundary: expose crawlable public company/product pages and citations; do not claim that
  ChatGPT will recommend or cite the company.

## Safe distribution actions for this project

1. Maintain one consistent company identity across the website, Facebook Page and Organization
   structured data.
2. Publish original, factual product pages and useful buyer information; do not mass-generate
   doorway pages or fabricate reviews.
3. Submit the sitemap through Search Console and IndexNow, then monitor Search Console processing.
4. Post to the company's owned Facebook Page and only to public groups whose stated purpose allows
   buying and selling arcade machines. Do not post repeatedly to unrelated groups.
5. Pursue additional authoritative profiles and directory mentions as the business verifies each
   account. Google Business Profile creation was attempted in the browser, but the setup flow
   returned an international-sanctions restriction for the submitted region; do not work around
   this by using a false address.
6. Track outcomes by verified referrals, enquiries, WhatsApp conversations and Search Console
   impressions/clicks; treat AI citations and ranking as external outcomes pending evidence.

## Delivery boundary

- Owner: root Codex agent.
- Writable scope: `site/index.html`, `site/contact.html`, `site/xiaoming-zhuang.html`,
  `site/privacy.html`, `site/credits.html`, `site/products/**`, `site/llms.txt`,
  `site/assets/catalog.css`, `scripts/build_catalog.py`, `tests/test_catalog_build.py`, and this
  evidence file.
- Forbidden scope: the frozen `$gmap-client-dev` workflow, `run_trade.cmd`, Google Maps automation,
  customer quotation data, prices, credentials, and unrelated design-system files.
- Dependency impact: none. The deployed site remains static and has no runtime dependency.
- Rollback: redeploy the previous verified commit `2dd5b2b1bfacb02074f8889be90af90a2f24e4fd` or the
  prior Cloudflare Production deployment; remove the new commit if a code rollback is required.
- Acceptance commands:
  `python -m unittest tests.test_catalog_build -v`,
  `python scripts/validate_catalog.py`,
  `python scripts/build_site.py`.
- Stop conditions: invalid JSON-LD, missing Organization entity on an indexed page, broken local
  links, private quote data exposure, failed responsive geometry checks, or any deployment mismatch.

## Locally verified facts

- Facebook Page: <https://www.facebook.com/QIJIANGTECHNOLOGY/>
- Page website link: `https://qijiang-arcade.pages.dev/products/`
- Catalogue launch Page post:
  <https://www.facebook.com/QIJIANGTECHNOLOGY/posts/pfbid045nAzVwJjAteCrgtw1ioqTDFTGygNi5iBGe9yacDwANhKrwgJnutUhyGuGEujo1Vl>
- Public group post:
  <https://www.facebook.com/groups/1345904826224051/posts/2372351583579365>
- The public group `Arcade machines for sale` states that it accepts arcade-machine buying and
  selling. A private Philippine arcade group was inspected but not posted to because its promotional
  rules were not clear and existing submissions were awaiting administrator approval.
- IndexNow accepted the complete 76-URL set with HTTP 200. The sitemap source used for the payload
  had SHA-256 `3ee1221829ab8bbdb78953fcb40f3c24018c685508cd486c47439963e277fba2`.
  The earlier six-URL submission recorded in the previous search evidence returned a different
  accepted status; the 200/202 records refer to different URL sets and times.
- Google Search Console accepted the refreshed sitemap; processing remains pending.
- A manual URL indexing request reached Google's daily quota. This is a temporary platform limit,
  not a website error.
- Current automated verification: 18 tests passed after the Facebook identity update.
