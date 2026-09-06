# Soy Yum — release verification

**Verified:** 6 September 2026  
**Application commit:** `5efbdc7d38a2058d74634666312c72bedaf9debc`  
**Live website:** https://prithiraj.github.io/soy-yum/  
**Successful build, browser tests and Pages deployment:** https://github.com/Prithiraj/soy-yum/actions/runs/34053076432

This report documents the released application. This documentation-only commit does not change the deployed site. Publication is a clearly labelled independent design preview, not an assertion of owner approval or commercial image clearance.

## Deployment verification

Both jobs completed successfully: **build** (`101540037203`) and **deploy** (`101540217316`). The post-deployment check fetched the live homepage, `/menu/`, `/credits/` and `/assets/app.js`; all returned HTTP 200 and contained their expected application markers. The Pages URL is the deployment action's confirmed environment URL, not merely a proposed destination.

## Browser and accessibility checks

**18 browser check groups passed**, using headless Google Chrome and Playwright 1.55.0 on GitHub's Ubuntu runner.

Home and menu were checked at **320, 390, 768, 1024 and 1440 CSS pixels**. Checks covered horizontal overflow, one H1, successful image decoding, visible call actions and uncaught JavaScript errors. Responsive screenshots were captured at 320, 390 and 1440 pixels.

Interaction checks passed for mobile navigation, expanded state, Escape/focus return, FAQ disclosure, photo-dialog opening/closing/focus restoration, menu category filtering, search, no-result messaging and reset. Both main pages retain their content and navigation with JavaScript disabled. Reduced-motion behavior and keyboard skip navigation passed. Credits and the custom 404 page passed mobile reflow checks.

| Automated axe scope | Passed rule checks | Violations | Checks requiring manual review |
|---|---:|---:|---:|
| Homepage, desktop | 23 | 0 | 2 |
| Menu, desktop | 27 | 0 | 1 |
| Credits, mobile | 20 | 0 | 0 |
| 404, mobile | 20 | 0 | 0 |

Axe-core 4.10.3 was run with WCAG 2 A/AA, 2.1 A/AA and 2.2 AA tags. These are automated rule results, not certification of full WCAG conformance. Human VoiceOver/NVDA testing, final text-enlargement checks and owner acceptance remain commercial-launch tasks.

The Lighthouse mobile label-in-name audit also passes after correcting the navigation button's accessible name to include its visible label, “Explore.”

## Lighthouse mobile lab results

Lighthouse 12.8.2 audited the generated application on the runner's local HTTP server using its mobile preset. These are **lab measurements**, not field Core Web Vitals or a guarantee of every visitor's performance.

| Metric | Recorded result |
|---|---:|
| Performance score | **97 / 100** |
| Accessibility score | **100 / 100** |
| Best-practices score | **100 / 100** |
| SEO score | **66 / 100** |
| First Contentful Paint | **1.5 s** |
| Largest Contentful Paint | **2.3 s** |
| Cumulative Layout Shift | **0.068** |
| Total Blocking Time | **0 ms** |
| Recorded page transfer | **366 KiB** |

The only failing scored SEO audit is **“Page is blocked from indexing.”** That is deliberate: every page carries `noindex, nofollow` while owner approval, photo rights and current operational details remain unconfirmed. The preview must not be advertised as an indexed official restaurant website. Metadata and structured data still exist for a reviewed future launch.

An earlier lab run scored 88 for performance. Deferring the nonessential Google Fonts stylesheet removed its render-blocking dependency; the final run scored 97. The normal site stylesheet remains immediate, and system-font/noscript fallbacks retain readable content. Final desktop/mobile screenshots for both main pages are pixel-identical to the previously inspected fully loaded screenshots, so the loading optimization did not change the settled layout.

The zero-millisecond Total Blocking Time value is not a measurement of field INP. No real-user performance or conversion data is collected by this release.

## Static checks and build size

Static tests passed for all four generated pages: internal destinations, anchors, unique IDs, image alt text and dimensions, descriptions/Open Graph fields, semantic landmarks, unresolved template tokens and the preview production guard. JavaScript syntax validation passed.

CSS is approximately **6.8 KB gzip** and JavaScript approximately **1.7 KB gzip**, below the 35 KB / 20 KB project budgets. The roughly 4.1 MB generated directory contains alternate sizes and formats for seven photographs, not 4.1 MB of initial page transfer. The browser requests suitable responsive variants.

## Visual review

Desktop and mobile screenshots were inspected for the hero, typography, actual sushi/BBQ/bakery photography, gallery, contact area, closing CTA and menu. The final loaded layouts preserve the vibrant cream/vermilion/blush/lime/forest direction and actual black-and-white brand identity. No Three.js, generated food or stock interior was substituted for business photographs.

The `soy-yum-qa` artifact attached to the workflow contains the browser report, desktop/mobile screenshots and full Lighthouse HTML/JSON reports. GitHub's artifact retention is 14 days; this Markdown summary remains in the repository.

## Remaining commercial-launch gates

Confirm representation of the business, obtain appropriate photograph/logo reuse permissions or replacements, supply the current menu/prices and weekly/holiday hours, confirm the branch contact and reservation process, and approve any dietary/accessibility statements. Complete human accessibility and business acceptance testing before removing the preview-specific safeguards.

Menu entries remain explicitly dated **published highlights**, not a complete live menu. Calls initiate an enquiry; the site never confirms a reservation or displays invented availability. The image-rights register and source evidence remain in [`evidence-and-assets.md`](evidence-and-assets.md), `content/photos.json`, and the visible credits page.
