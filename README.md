# Thrill Wave Website

Static rebuild of the Thrill Wave Wix site, prepared for GitHub + Cloudflare Pages.

## Stack
Semantic HTML5, shared CSS, vanilla JavaScript, optimized WebP/PNG assets, YouTube/Vimeo embeds. No build step.

## Local development
Open `index.html` with VS Code Live Server. Links use explicit `.html` or `index.html` paths so navigation works locally.

## SEO / AEO
Canonical URLs, Open Graph metadata, structured data, `robots.txt`, `sitemap.xml`, `llms.txt`, semantic headings and descriptive metadata are included.

## Cloudflare Pages
No build command is required. Publish the repository root. `_headers` contains basic security/cache headers and `_redirects` maps clean public routes to static files.


## Quality checks
Every push and pull request runs a zero-dependency site audit in GitHub Actions. It checks local links/assets, page titles, descriptions, canonicals, H1 structure, image alt text, duplicate IDs, required production files, and JavaScript syntax.

Run locally:

```bash
python scripts/audit.py
node --check js/main.js
```
