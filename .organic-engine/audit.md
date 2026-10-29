# Audit, 2026-10-29

## Fixed in PR organic-engine/page-fixes
- Title was 79 chars; now 51. Added meta description, canonical, Open Graph, Twitter card, JSON-LD (WebApplication, Service £275 offer, Person).
- No order route for the £275 monograph: added "Commission Yours" header button, treatise CTA, chapter-10 link, all to Tally form.
- Ephemeris corrections (checked with IAU ERFA epv00/plan94 and IGRF): Earth 1.014 AU / 29.36 km/s (aphelion was 4 Jul 1973); Mars at perihelion 1.38 AU, -1.7° latitude (page said accelerating toward perihelion, +1.85°); Jupiter–Saturn heliocentric span 138° (page said 88.4° right angle); Minna dip -2.4° (page said ±0.8°). Chapter 4 rewritten around the real geometry.
- Calculator: Earth speed now vis-viva; Mars distance/latitude and Jupiter–Saturn span now computed per input from JPL approximate Keplerian elements (previously fixed values).
- Added method note separating calculated astronomy from FTA interpretation.
- Added sitemap.xml and llms.txt.

## Open (owner decision)
- Wave Collision modal returns fixed values (cos 0.892, 28%, 0.14) for every pair. Either compute or label as illustrative.
- The ten chapters are Bala's own monograph shown for any input name; visitors may read it as their result. Consider a "sample" label when name ≠ Bala.
- Remaining "verified physics" phrasing in chapters 1–3, 5–10 and README (e.g. "supersedes", "certifies ... rigorous").
- robots.txt only works at https://somersetnomad.github.io/robots.txt (user-site repo). Check it exists and doesn't block; reference this sitemap there.
- No Search Console property yet: add URL-prefix property for this path and submit sitemap.xml.
- Not indexed for brand name as of 2026-10-29 (spot check).
- H1 is the small header wordmark; acceptable but a descriptive H1 above the calculator would help.
- README: MIT badge vs "NO License" text conflict.
