# Orange Juice Applications — Website

Static marketing site for [orangejuiceapplications.com](https://www.orangejuiceapplications.com): project hub, FaceMatch guides & legal pages, and You Can Dance Academy gateway.

This repository was split from the [FaceMatch](https://github.com/OMeds/FaceMatch) app repo so the website can be versioned and deployed independently.

## Layout

| Path | Purpose |
|------|---------|
| `src/` | Editable site source (HTML, CSS, JS, assets) |
| `dist/` | Build output — upload **contents** to your web host |
| `Brand/` | Logo SVG sources |
| `Brand/ycda/` | You Can Dance Academy logos (sourced from youcandanceacademy.co.uk) |
| `docs/legal/` | FaceMatch + website privacy (Markdown → HTML) |
| `docs/pages/` | About, work, contact (Markdown → HTML) |
| `docs/updates/` | News posts (Markdown → HTML) |
| `docs/guides/` | FaceMatch user guides (Markdown → HTML) |
| `scripts/` | Build and asset generation |
| `deploy/` | FileZilla site template and FTP notes |
| `.cursor/skills/ui-ux-pro-max/` | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) agent skill (design search DB) |
| `design-system/orange-juice-applications/` | Persisted OJA design tokens (from the skill workflow) |

### UI UX Pro Max

Installed with `npx -y uipro-cli init --ai cursor`. Regenerate recommendations:

```bash
python3 .cursor/skills/ui-ux-pro-max/scripts/search.py "studio portfolio Apple apps" --design-system -p "Orange Juice Applications" -f markdown
```

Site styling follows `design-system/orange-juice-applications/MASTER.md` (brand orange retained over generic palette suggestions).

## Build

Requirements: Python 3, Pillow, Node/npx (for `@resvg/resvg-js-cli` logo rasterization).

```bash
chmod +x scripts/build.sh
./scripts/build.sh
```

YCDA logos are pulled from the live studio site into `Brand/ycda/` (`logo.png` is used on-site; `logo-transparent.png` is kept as an optional alternate) and resized to `src/assets/ycda-logo-*.png` via `scripts/process_ycda_logos.py` (runs automatically during build).

Preview locally:

```bash
cd src && python3 -m http.server 8080
# or after build:
cd dist && python3 -m http.server 8080
```

## Deploy (Fasthosts / FileZilla)

See [deploy/DEPLOY.md](deploy/DEPLOY.md) for FileZilla setup and FTP upload steps.

## YCDA live URL

Edit `src/ycda/index.html` — `oja-ycda-app-url` meta and `#ycda-open` href — then rebuild.

## Integrations (`src/assets/site-config.js`)

| Key | Purpose |
|-----|---------|
| `formspreeIntakeId` | One-click submit on `/start-a-project/` (else mailto fallback) |
| `calendlyUrl` | Discovery call embed on `/contact/` and intake page |
| `plausibleDomain` | Privacy-friendly analytics |
| `facematchAppStoreUrl` / `ycdaAppStoreUrl` | App Store badges when live |

See `deploy/site-config.example.js` for a template.

Guides and legal HTML are **generated only in `dist/`** — do not edit copies under `src/contact-profile-picture-sync/guides/`.
