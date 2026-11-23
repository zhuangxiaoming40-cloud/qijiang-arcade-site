# Qijiang public company profile

Static public profile for Guangzhou Qijiang Technology Co., Ltd. and Xiaoming Zhuang.

Live website: <https://qijiang-arcade.pages.dev/>

Public contact: Xiaoming Zhuang, Export Sales, <zhuangxiaoming40@gmail.com>, WhatsApp <https://wa.me/8617691342432>.

## Site

- Company landing page: `site/index.html`
- Commercial air hockey tables: `site/air-hockey-tables.html`
- Xiaoming Zhuang profile: `site/xiaoming-zhuang.html`
- Contact page: `site/contact.html`
- Crawl files: `site/robots.txt`, `site/sitemap.xml`, `site/llms.txt`

## Deployment

The publication target is Cloudflare Pages Direct Upload. GitHub Pages is intentionally not used because its official usage limits exclude running a commercial website.

Expected public origin:

`https://qijiang-arcade.pages.dev/`

Publish the contents of `site/` as the Cloudflare Pages output directory.

Deploy:

```powershell
npx wrangler pages deploy artifacts/cloudflare-dist-20261124 --project-name qijiang-arcade --branch main
```
