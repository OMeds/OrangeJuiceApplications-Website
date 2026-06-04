# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/orange-juice-applications/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

**Project:** Orange Juice Applications  
**Generated:** 2026-06-04 (synthesized from UI UX Pro Max + existing brand)  
**Category:** Independent studio / SaaS portfolio (dance education + Apple apps)

---

## Pattern (UI UX Pro Max)

- **Layout:** Hero-Centric → Bento project grid → Social proof → Feature bands → CTA
- **Style:** Bento grids + warm glass surfaces (Apple-like cards on `#F5F5F7` page base)
- **Motion:** Scroll reveal, 200ms hovers; respect `prefers-reduced-motion` (no marquee/canvas when reduced)

---

## Color Palette (brand — do not replace with generic SaaS blue)

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary / ink | `#1A1A1A` | `--color-primary` / `--ink` |
| Secondary | `#3F3F46` | `--color-secondary` |
| CTA / accent | `#E85D04` | `--orange` |
| CTA hover | `#C44900` | `--orange-dark` |
| Page background | `#F5F5F7` | `--oja-page-bg` |
| Warm surface | `#F6F3EF` | `--oja-bg-warm` |
| Card | `#FFFFFF` | `--card` |
| Muted text | `#475569` | `--muted` (min contrast on light) |
| YCDA accent | `#61A4B8` | `--ycda-teal` |

---

## Typography

- **Heading:** Outfit (geometric, modern — existing brand)
- **Body:** DM Sans (readable, friendly)
- **Do not use:** Comic Neue, Baloo 2, or pure black `#000000` backgrounds

---

## Spacing & layout

| Token | Value |
|-------|-------|
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 32px |
| `--space-2xl` | 48px |
| `--space-3xl` | 64px |
| Max content | `--max-wide` (72rem) |
| Nav | Floating bar: `top: 1rem`, horizontal inset `1rem`, `border-radius: 16px` |

---

## Component rules

### Buttons
- Primary: orange fill, 200ms transition, `cursor: pointer`
- Focus: `outline: 3px solid var(--orange); outline-offset: 2px`
- No layout-shifting scale on hover (opacity/shadow only)

### Cards / bento
- `border-radius: 20–24px`, subtle shadow, hover: `translateY(-4px)` + shadow (no scale)
- All clickable cards: `cursor: pointer`

### Navigation
- Glass/frosted bar, sticky offset from viewport edges
- Skip link to `#main-content` required

---

## Anti-patterns (UI UX Pro Max + OJA)

- Emojis as UI icons
- `outline: none` without `:focus-visible` replacement
- Decorative infinite animation (marquee runs only when motion allowed)
- Scale transforms that shift layout on hover
- Muted text lighter than `#475569` on white
- Replacing orange brand with generic trust-blue `#2563EB`

---

## Implementation map

| Layer | Path |
|-------|------|
| Icons (SVG) | `scripts/website_components.py`, `src/assets/oja-icons.css` |
| Page shells | `scripts/marketing_shell.py`, `scripts/website_chrome.py` |
| Generated marketing | `scripts/render_company_pages.py`, `render_legal_hub.py`, `render_extra_pages.py` |
| Hand-built | `src/index.html`, `src/ycda/`, `src/facematch/`, `src/start-a-project/` |

## Pre-delivery checklist

- [x] 4.5:1 text contrast on light surfaces (`--muted: #475569`)
- [ ] `prefers-reduced-motion` disables marquee, canvas, tilt, autoplay carousel
- [ ] Responsive: 375, 768, 1024, 1440px
- [ ] All images have `alt`; logos decorative use `alt=""`
- [ ] Existing assets reused: `company-logo*.svg`, `app-icon.png`, `og-*.png`, guides, legal, build scripts
