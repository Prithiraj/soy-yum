# Soy Yum — Hindustan Park

A vibrant, photo-led restaurant website, built as semantic static HTML/CSS with small progressive enhancements. **No application framework, Three.js, tracker, booking backend or runtime package dependency.**

**GitHub Pages:** https://prithiraj.github.io/soy-yum/

## Status and publication boundary

The requester approved implementation and GitHub Pages publication on **6 September 2026**. This release is an **independent, noindex design preview**, not an owner-approved official commercial site. Seven actual Soy Yum photographs are used with visible preview labels and a credits register. Publication does not establish image rights. Confirm reuse rights or replace the assets before official commercial launch.

The current menu, prices, weekly hours and booking integration have not been supplied. The implementation therefore uses an accurately labelled **menu-highlights page** based on published coverage and **Call for a table**, not a pretend reservation form. No prices, weekly schedule, dietary guarantees, offers, reviews or availability have been fabricated.

## Run locally

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/build.py --base /
python -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. The first build downloads source images using the explicit allowlist in `content/photos.json`; subsequent builds use `.cache/images`. To rebuild without downloading, pass `--offline`. The preview is static after building: any static host can serve `_site/`.

## Edit

| Concern | Location |
|---|---|
| Approved plan, decisions and deviations | `docs/design-plan.md` |
| Evidence and photo-rights ledger | `docs/evidence-and-assets.md`, `content/photos.json` |
| Branch details and canonical external destinations | `content/site.json` |
| Menu highlights and their source dates | `content/menu.json` |
| Homepage, menu, credits, 404 content | `src/` |
| Shared head, header and footer | `src/partials/` |
| Color system, layouts, responsive/reduced-motion behavior | `assets/style.css` |
| Navigation, gallery, menu search and clipboard enhancement | `assets/app.js` |
| Static generation, image variants and launch guard | `scripts/build.py` |
| Build and browser checks | `tests/` |
| GitHub Pages deployment | `.github/workflows/deploy.yml` |

## Pages and behaviors

`/` provides cuisine discovery, BBQ/bakery features, real-space gallery, directions, contact and practical FAQs. `/menu/` has accessible filter/search enhancement; every item remains visible without JavaScript. `/credits/` documents image provenance, evidence gaps, preview status and privacy. `/404.html` provides a real recovery path.

Photographs are downloaded at build time, not hotlinked in visitors’ browsers, and emitted as 480/800/1200-tier WebP plus JPEG fallbacks. The exact source image is preserved without removing brand marks. Google Fonts supplies DM Serif Display and DM Sans; system fonts work when it fails. No font binaries are bundled.

## Tests

For the default Pages base path:

```sh
python scripts/build.py
python tests/static.py
node --check assets/app.js
# Browser checks additionally require Playwright, installed Chrome and a local server.
pip install playwright==1.55.0
mkdir -p _preview/soy-yum
cp -R _site/. _preview/soy-yum/
python -m http.server 8765 --directory _preview
# In a second terminal:
python tests/browser.py
```

CI also injects axe-core and captures desktop/mobile screenshots. Lighthouse results are lab measurements, not a claim of field performance or WCAG certification. Human screen-reader and owner acceptance remain separate release checks.

## Deploy

A push to `main` runs the Pages workflow: build → static checks → browser/accessibility checks → artifact upload → Pages deployment → live HTTP checks. GitHub Pages must already be enabled. The workflow uses `contents: read`, `pages: write` and `id-token: write` where needed; it does not require a stored personal token.

The intended project base is `/soy-yum/`. A custom domain needs coordinated updates to the build origin/base and canonical metadata; no custom domain has been invented.

## Before official commercial launch

Obtain approved originals/rights, correct weekly hours, current menu/prices, the branch’s confirmed booking workflow, permission to represent the business, and any dietary/access statements. Update the preview-specific content and tests. `--production` deliberately refuses release until the launch gate is implemented and reviewed; toggling a boolean alone cannot silently turn the demo into an official site.

No analytics are transmitted. `soy:action` DOM events are local-only hooks; review consent/privacy before adding any collection. Site notes explain the external font, hosting, social and map services.
