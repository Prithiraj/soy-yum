# Soy Yum — approved design and implementation plan

**Branch:** Hindustan Park / Keyatala Road, Kolkata  
**Research and approval:** 6 September 2026  
**Repository:** https://github.com/Prithiraj/soy-yum  
**Publication:** GitHub Pages, independent design preview; not an owner-approved commercial website.

The original direction was approved with an explicit request to make the site more vibrant, use actual photographs, implement in this repository and publish on GitHub Pages. This document records the implemented interpretation and the remaining commercial-launch gates. The earlier warm-editorial concept, factual discipline, mobile-first structure and progressive enhancement remain intact.

## 1. Evidence baseline

The brand-linked profile (https://linktr.ee/soyyumkol) identifies Japanese izakaya dining, sushi, Korean BBQ, an Asian cafe and in-house Asian bakery, with the Hindustan Park address. The branch listing (https://www.zomato.com/kolkata/soy-yum-hindustan-park) supplies the telephone and dated dining-rating snapshot. The May 2024 Indulge restaurant visit supplies named menu highlights; it is historical coverage, not proof of today's inventory.

Implemented facts: Soy Yum, Hindustan Park; P353B, Keyatala Road, Kolkata 700029; +91 81005 81884; the cuisine/bakery proposition; exact user-supplied Google Maps destination; brand-linked social profiles. Zomato 4.7/5 from 1,980 dining ratings is explicitly attributed and checked 6 September 2026. The rating is not represented as live or used in aggregate-rating structured data.

Unresolved: commercial photograph rights, owner representation approval, current menu/prices, seven-day hours, holiday exceptions, BBQ inclusions, booking provider, alcohol, parking and step-free access. Conflicting listings and unavailable brand menu are not silently reconciled. See `evidence-and-assets.md` and the machine-readable content files.

## 2. Audience

Planning hypotheses, not demographic research: nearby diners choosing a venue; couples and friends exploring Japanese/Korean food; small groups asking about grill tables; returning visitors who need menu, phone and directions immediately. Show the food and real room before requiring commitment. Keep important actions available without reading the story.

## 3. Conversion goals

Primary: **Call for a table**, opening the branch telephone; no false claim of a completed reservation. Secondary: **Explore the menu**, accurately labelled published highlights while the current menu is unavailable. Supporting: exact-branch directions, address copy and social links. Header, hero, visit section, closing invitation and mobile action bar repeat this hierarchy.

Optional `soy:action` DOM events distinguish placements; no analytics request is transmitted. Clicks are intent signals, never reported as confirmed bookings. No newsletter popup, discount timer, booking form or invented availability.

## 4. Creative direction

**Warm editorial hospitality, turned up in color.** Cream space, large serif typography, vermilion calls to action, blush-pink food postcards, a lime sticker and forest-green BBQ panel. Seven real Soy Yum photographs carry the experience. Asymmetric compositions alternate with quiet readable information. Rectangular images, small tilts and a restrained rounded-button system keep the page lively without becoming a game.

Hero: “Sushi. Sizzle. Something sweet.” Supporting copy is the sourced dining proposition. Use direct language, not superlatives or pseudo-Japanese decoration. Preserve the actual black-and-white logo and visible marks in photographs. No invented kanji, unrelated anime characters, stock interiors or simulated food.

## 5. Color system

| Token | Value | Use |
|---|---|---|
| Paper | `#fff8ee` | Main canvas |
| Ink | `#29201d` | Primary text |
| Muted | `#655b54` | Supporting text |
| Deep vermilion | `#b93227` | Buttons and readable emphasis |
| Tomato | `#e94633` | Large decorative accents only |
| Blush | `#f4bcc6` | Bakery/postcard surfaces |
| Lime | `#e4ee9b` | Sticker and location accents |
| Forest | `#263f32` | BBQ and top strip |
| Line | `#dacdbd` | Dividers |

These are proposed website tokens, not claimed official brand colors. Test rendered text, focus and hover contrast; a palette table alone is not accessibility certification.

## 6. Typography

DM Serif Display headlines and DM Sans body/interface, via Google Fonts with `display=swap`. Georgia/Arial fallbacks keep content usable when fonts fail. No font binaries are bundled in this repository. Only necessary styles/weights are requested. Body text is at least 16px; serif hero sizing scales to the viewport. Avoid fixed heights that truncate text or labels at zoom.

## 7. Image strategy

Seven real restaurant photographs: sushi close-up, sushi spread, tabletop BBQ, Japanese cheesecake, ramen, and two views of the actual room. The original brand-linked logo is used separately. Sources, alt text, dimensions and rights status are in `content/photos.json`; visible source credits are at `/credits/`.

Image variants are produced at build time in WebP with JPEG fallback; 480/800/1200 tiers do not enlarge originals. Hero loads eagerly; other photographs load lazily with reserved dimensions. Full photographs remain accessible through ordinary image links when the enhanced gallery is unavailable. Do not remove source brand marks or substitute another branch's space.

**All current photos are preview-only, with commercial reuse unconfirmed.** Owner-controlled publication does not itself grant reuse permission. A preview label is not a license. Official commercial release requires approved originals or replacement. No generated food is used.

## 8. Information architecture

Home `/`: hero → cuisine strip → three experience cards → BBQ → bakery → real space/gallery → visit information and FAQs → strong final CTA. Menu `/menu/`: intro and provenance notice → published highlights with optional search/category filters → current-menu enquiry. Supporting `/credits/` makes rights, sources and privacy explicit. `/404.html` provides recovery.

Two principal customer pages remain the scope; credits/404 are supporting requirements, not an expanded content program. No blog, checkout, account or speculative branch directory.

## 9. Section-by-section layout

**Header/hero:** existing logo, branch label, concise navigation, visible call button; large sushi photograph, editorial headline, primary/secondary actions and dated Zomato attribution. Mobile places text/actions before the photograph.

**Experience proposition:** sushi/Japanese dining, Korean BBQ, bakery as three photo-led cards. Each has a useful destination; avoid generic quality/service icon filler.

**BBQ:** forest split panel with actual grill photography and “Ask about BBQ tables.” No invented package price, group minimum, included sides or grill availability.

**Bakery:** blush background, cheesecake image and “Leave room for something sweet.” Published menu reference is not a promise of today's stock.

**Real space/gallery:** two room photographs and a food detail; an optional native dialog enlarges images. Do not invent chef credentials, team biographies or sourcing stories.

**Menu:** five sourced highlights, with source dates and named categories. No fabricated prices or dietary labels. Search, category buttons, result count, no-result state and reset enhance—not replace—the complete static list. A historical-reference notice appears before the list.

**Visit:** selectable exact address, telephone, directions, safe address-copy enhancement and explicit call-to-confirm hours wording. The typographic location panel is not a fabricated map. FAQs explain table enquiries, menu currency and access confirmation.

**Footer/closing:** repeat call/menu actions and social links; independent preview status and photo-source link remain visible. No unsupported email or newsletter.

## 10. Three.js / animation plan

No Three.js is included. Real food and room photographs are the strongest assets; a 3D scene would add weight without clarifying the restaurant. Small CSS hover lifts, image translations and navigation transitions supply polish. No scroll hijacking, autoplay, floating food, cursor effects, perpetual motion or hidden-until-animated content.

`prefers-reduced-motion: reduce` removes nonessential transitions/transforms and smooth scrolling. All content is present by default, including when JavaScript fails.

## 11. Responsive behavior

Mobile-first from 320px: single-column features, restrained padding, flexible hero, accessible disclosure navigation, two-action bottom bar. Tablet progressively introduces paired layouts. Desktop uses a bounded content width and asymmetric photo/text rhythm. Breakpoints follow content needs.

Reserve space for mobile safe areas and bottom actions; avoid covering focused elements. At constrained height or coarse-pointer/zoom conditions the bar must not obscure controls. No interaction requires hover. Test 320, 390, 768, 1024 and 1440px, both main pages, plus zoom/reflow and portrait/landscape crops.

## 12. Accessibility

Target WCAG 2.2 AA; do not claim certification from automated checks. Semantic header/nav/main/footer, one H1, meaningful headings, visible skip link and strong focus outline. Real links for destinations, buttons for UI state. Principal controls target at least 44px.

Navigation has expanded state and Escape focus return. Native dialog has an accessible name, close button, focus handling and normal-link fallback. Menu search has an accessible label and result status; selected category is not communicated by color alone. FAQs use native details/summary. Photographs have image-specific alt text, decorative elements are hidden from assistive technologies, and no menu is image-only.

Automated axe checks and keyboard/browser tests are release gates. Human VoiceOver/NVDA, text-enlargement and final owner testing remain separate commercial-launch acceptance steps.

## 13. Performance

Static HTML/CSS; roughly 7KB gzip CSS and 2KB gzip JS before final CI measurements. No client application framework, runtime package, WebGL, database, third-party embedded social feed, booking widget or automatic map load. Image decoding and dimensions avoid unnecessary layout shifts.

Budgets: JS ≤20KB gzip, CSS ≤35KB gzip, mobile hero ≤250KB target, no font-blocked text. The full asset directory includes alternate image sizes/formats and is not equal to initial transfer. Measure initial transfer and LCP using the actual browser build. Lighthouse mobile performance ≥90 is a target, not a fabricated score or a field guarantee. Desired field LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 require real-user data after an approved launch.

## 14. SEO / local discovery

Descriptive page titles, meta descriptions, canonical URLs, Open Graph metadata and a 1200×630 original text sharing card are implemented. Restaurant structured data uses only sourced facts and explicitly relates this independent preview to the business. Do not assert an official website URL, weekly schedule, price range, review stars or owner identity.

**Preview override:** all pages carry `noindex, nofollow`; the sitemap intentionally contains no discovery URLs. Robots permits crawlers to see the noindex directive. This requested public Pages preview is not intended to be search-indexed as an official restaurant website. An approved commercial release needs reviewed copy, indexing, sitemap and correct official canonical identity.

## 15. Rights / licensing notes

Actual food/room images are sourced from the branch listing; logo from the brand-linked profile. No commercial license is inferred. Record photographer/rightsholder, permission scope, expiry, credit and people/artwork clearances before official launch. Public preview status must not be confused with legal clearance.

Google Fonts DM families use the SIL Open Font License in their upstream source; no font files are distributed here. The simple bowl/chopsticks favicon and decorative graphics are original interface artwork, not a claimed replacement logo. Preserve all third-party rights. No testimonial quotation carousel or editorial award claim is used.

## 16. Implementation sequence

1. Inspect repository and recheck evidence/assets.
2. Record the approved vibrant interpretation, facts and unresolved gates in Markdown/JSON.
3. Implement semantic templates, shared CSS, sourced content and optimized-photo build.
4. Add progressively enhanced navigation, gallery, menu controls and clipboard feedback.
5. Run static/link/budget checks, JS syntax checks, browser/axe tests and responsive screenshots; fix failures.
6. Publish the labelled preview through GitHub Actions/Pages after tests pass.
7. Verify live HTTP responses and essential destinations; document actual test results.
8. Before an official commercial launch, obtain rights/operational/owner approval, update preview-specific copy and release guard, then repeat acceptance testing.

A push to main rebuilds and redeploys. No personal token, customer-data collection, payment processing or unconnected reservation form is added.

## 17. Acceptance criteria

- Actual branch identity and photographs dominate; vibrant but refined visual rhythm.
- No invented business claims, prices, hours, policies, dietary labels or booking confirmations.
- Call, menu and exact-branch directions work across mobile/desktop.
- Every menu highlight has a source/date; current-menu gap is visible.
- No horizontal overflow at tested widths; no broken local images/links/anchors.
- Keyboard navigation, Escape focus return, skip link, filters, FAQ and gallery work.
- No-JavaScript content and primary actions remain usable; reduced motion works.
- No unresolved automated WCAG A/AA violations; human checks are not falsely reported as completed.
- Image variants, CSS/JS budgets, metadata and JSON-LD validate.
- All uncleared assets and preview status remain clearly identified.
- CI and live Pages HTTP checks succeed before claiming deployment.

### Recorded deviations from the earlier plan

The user requested a more vibrant palette: pink/lime/vermilion augment warm cream and forest. No Three.js is needed. The unavailable approved menu is replaced by explicitly dated published highlights, not invented inventory. A credits page is added to make image status transparent. Publication is a **noindex independent preview**, while official commercial release remains blocked pending rights and business approvals. These are deliberate honesty and release-safety decisions, not silently completed owner-approval gates.
