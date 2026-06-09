# Home page overrides

**Overrides MASTER.md for `/` (index.html) only.**

## Positioning

**Software studio first** — custom builds for studios, membership businesses, and privacy-conscious apps. YCDA and FaceMatch are proof of shipped work, not the primary identity.

## Pattern

Apple-style **scroll story** — one narrative path, not a dense marketing grid.

## Section order

1. **Intro** — full-viewport hero, primary + contact CTAs, scroll hint
2. **Chapter 1 · Studio** — custom software scope (4 scroll steps)
3. **Chapter 2 · YCDA** — interactive screenshot preview (4 tabs: home, classes, taster, portal)
4. **Chapter 3 · FaceMatch** — our Apple product in development (3 steps)
5. **Chapter 4 · Start** — “Got an idea we can build?” + pre-footer CTA band

## Chrome

- Fixed **story rail** — Studio / YCDA / FaceMatch / Start
- `data-ycda-preview` + `initYcdaPreview()` — tabbed screenshots from youcandanceacademy.co.uk
- Screenshots captured via `scripts/capture_ycda_screenshots.mjs` (cookie banners dismissed before capture)

## Removed from home

- Marquee, bento grid, trust strip, testimonial carousel/chapter, chip switcher, comparison table

## CTAs

- Intro: Start a project + Got an idea? Contact us
- Chapter 4 + `oja-idea-cta` band before footer

## Deep links

- Parent testimonials live on `/ycda/#testimonials` only — not duplicated on home
