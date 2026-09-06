# Evidence and asset ledger

Research checked **6 September 2026**. This repository is an independent website design preview. Publicly available material is not automatically commercially licensed.

## Business facts

| Fact | Source | Treatment |
|---|---|---|
| Soy Yum, Hindustan Park; P353B Keyatala Road, Kolkata 700029 | https://linktr.ee/soyyumkol | Visible address; branch-specific |
| Japanese dining, sushi, Korean BBQ, Asian bakery | Brand-linked profile above | Visible proposition; no exclusivity claims |
| +91 81005 81884 | https://www.zomato.com/kolkata/soy-yum-hindustan-park | Call-for-a-table action; no booking guarantee |
| 4.7 / 1,980 dining ratings | Same listing, research snapshot | Attributed, dated, not live; no aggregateRating JSON-LD |
| Exact map destination | User-provided place URL in content/site.json | Not a guessed place ID |
| Brand social profiles | Links from brand profile | External links, no tracking embed |

## Menu evidence

Indulge published its restaurant visit on **9 May 2024**: https://www.indulgexpress.com/food/food-calcutta/2024/May/09/this-japanese-korean-modern-caf%C3%A9-in-kolkata-offers-lavish-meal

Named historical highlights: spicy salmon maki, buta negima, spicy chicken miso ramen and Japanese cheesecake. Korean BBQ is also supported as a category by the brand profile. These are not a current full menu. Prices and current availability are deliberately not invented. Each item in `content/menu.json` has a source key and date.

The brand-linked digital menu could not be fetched during research. Today's listing hours do not establish a weekly schedule. Conflicting cost, alcohol and branch entries were not used to invent an operational answer. No WhatsApp number, parking guarantee, step-free claim or third-party booking provider is assumed.

## Actual photographs and logo

The complete machine-readable asset register is [`content/photos.json`](../content/photos.json). It records each exact source-image URL, published-source page, descriptive alt text, reference identifier and `production_approved: false`. Visitors can inspect the same provenance at `/credits/`.

| Key | Subject | Provenance |
|---|---|---|
| logo | Brand-linked black-and-white logo | Soy Yum's Linktree profile |
| sushi | Sushi plate, wooden table | Hindustan Park Zomato gallery |
| sushi-table | Sushi platter | Same branch gallery |
| bbq | Tabletop Korean BBQ and accompaniments | Same branch gallery |
| cheesecake | Japanese-style cheesecake | Same branch gallery |
| room | Table, cane chairs, copper-toned hood | Same branch gallery |
| space | Wider room and display counter | Same branch gallery |
| ramen | Noodle bowl | Same branch gallery |

**Commercial reuse is not established for any entry.** Confirm rights or replace before official commercial launch. A brand mark or listing publication does not prove ownership or grant reuse permission. A preview label is not a license. No watermark is removed. Food photos are illustrative, not a promise of current inventory. Images are downloaded at build time and optimized for static deployment; no generic stock or generated food is used.

## Release checklist

Obtain owner representation approval, photograph/logo licenses, current menu/prices and dietary language, weekly/holiday hours, branch booking destination and operational accessibility information. Record a named content maintainer and recheck every external destination. The `--production` build guard cannot be removed by merely switching a flag. Human screen-reader and commercial owner acceptance have not been claimed.

## Maintenance

Recheck published contact and destinations before each release. Recheck the displayed rating monthly; remove the statistic when stale instead of implying a live feed. Historical highlights retain their source dates until replaced by an approved menu. Review dependencies and source-host availability before rebuilding.
