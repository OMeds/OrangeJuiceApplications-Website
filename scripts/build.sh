#!/usr/bin/env bash
# Build static site into dist/ — upload dist/ contents to Fasthosts htdocs (see deploy/DEPLOY.md).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/src"
OUT="$ROOT/dist"
LEGAL="$ROOT/docs/legal"
GUIDES="$ROOT/docs/guides"
OAUTH_PLATFORMS=(linkedin facebook instagram microsoft slack discord x)

export PYTHONPATH="$ROOT/scripts${PYTHONPATH:+:$PYTHONPATH}"

python3 "$ROOT/scripts/process_brand_logo.py"
python3 "$ROOT/scripts/process_app_icon.py"
python3 "$ROOT/scripts/process_og_images.py"
python3 "$ROOT/scripts/process_ycda_logos.py"
if command -v node >/dev/null 2>&1 && [[ -f "$ROOT/scripts/capture_ycda_screenshots.mjs" ]]; then
  if [[ ! -f "$SRC/assets/ycda-screenshots/home.png" ]] && [[ -f "$ROOT/node_modules/playwright/package.json" || -f "$ROOT/package.json" ]]; then
    node "$ROOT/scripts/capture_ycda_screenshots.mjs" 2>/dev/null || true
  fi
fi

rm -rf "$OUT"
mkdir -p "$OUT/assets" "$OUT/facematch/beta" "$OUT/ycda" "$OUT/start-a-project" "$OUT/legal" \
  "$OUT/about" "$OUT/work" "$OUT/contact" "$OUT/updates" "$OUT/press" "$OUT/company/privacy" \
  "$OUT/company/services" \
  "$OUT/contact-profile-picture-sync/privacy" \
  "$OUT/contact-profile-picture-sync/terms" \
  "$OUT/contact-profile-picture-sync/support" \
  "$OUT/contact-profile-picture-sync/subscription-terms" \
  "$OUT/contact-profile-picture-sync/data-retention" \
  "$OUT/contact-profile-picture-sync/acceptable-use"

for platform in "${OAUTH_PLATFORMS[@]}"; do
  mkdir -p "$OUT/facematch/oauth/$platform"
done

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/privacy-policy.md" "$OUT/contact-profile-picture-sync/privacy/index.html" \
  "Privacy Policy for FaceMatch by Orange Juice Applications." \
  "FaceMatch Privacy Policy" "/contact-profile-picture-sync/privacy/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/terms-of-use.md" "$OUT/contact-profile-picture-sync/terms/index.html" \
  "Terms of Use for FaceMatch by Orange Juice Applications." \
  "FaceMatch Terms of Use" "/contact-profile-picture-sync/terms/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/support.md" "$OUT/contact-profile-picture-sync/support/index.html" \
  "Support information for FaceMatch." \
  "FaceMatch Support" "/contact-profile-picture-sync/support/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/subscription-terms.md" "$OUT/contact-profile-picture-sync/subscription-terms/index.html" \
  "App Purchase and Pricing Terms for FaceMatch." \
  "FaceMatch App Purchase & Pricing Terms" "/contact-profile-picture-sync/subscription-terms/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/data-retention.md" "$OUT/contact-profile-picture-sync/data-retention/index.html" \
  "Data retention and deletion for FaceMatch." \
  "FaceMatch Data Retention & Deletion" "/contact-profile-picture-sync/data-retention/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/acceptable-use.md" "$OUT/contact-profile-picture-sync/acceptable-use/index.html" \
  "Acceptable Use Policy for FaceMatch." \
  "FaceMatch Acceptable Use Policy" "/contact-profile-picture-sync/acceptable-use/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/company-privacy-policy.md" "$OUT/company/privacy/index.html" \
  "Privacy policy for orangejuiceapplications.com and marketing forms." \
  "Website Privacy Policy" "/company/privacy/"

python3 "$ROOT/scripts/render_legal_html.py" \
  "$LEGAL/services-inquiry-terms.md" "$OUT/company/services/index.html" \
  "Terms for custom project inquiries with Orange Juice Applications." \
  "Custom Project Inquiry Terms" "/company/services/"

python3 "$ROOT/scripts/render_legal_hub.py" "$OUT"
python3 "$ROOT/scripts/render_company_pages.py" "$OUT"
python3 "$ROOT/scripts/render_extra_pages.py" "$OUT"
python3 "$ROOT/scripts/render_static_pages.py" "$OUT"
GUIDES_DIR="$GUIDES" python3 "$ROOT/scripts/render_guides.py" "$OUT"
python3 "$ROOT/scripts/render_feedback_page.py" "$OUT"
python3 "$ROOT/scripts/render_error_pages.py" "$OUT"
python3 "$ROOT/scripts/render_rss.py" "$OUT"
python3 "$ROOT/scripts/render_sitemap.py" "$OUT"

cp "$SRC/index.html" "$OUT/index.html"
cp "$SRC/facematch/index.html" "$OUT/facematch/index.html"
cp "$SRC/ycda/index.html" "$OUT/ycda/index.html"
cp "$SRC/start-a-project/index.html" "$OUT/start-a-project/index.html"
cp "$SRC/assets/style.css" "$OUT/assets/style.css"
cp "$SRC/assets/oja-premium.css" "$OUT/assets/oja-premium.css"
cp "$SRC/assets/oja-icons.css" "$OUT/assets/oja-icons.css"
cp "$SRC/assets/site.js" "$OUT/assets/site.js"
cp "$SRC/assets/site-config.js" "$OUT/assets/site-config.js"
cp "$SRC/assets/oja-interactive.js" "$OUT/assets/oja-interactive.js"
cp "$SRC/assets/oja-intake.js" "$OUT/assets/oja-intake.js"
cp "$SRC/assets/ycda-launch.js" "$OUT/assets/ycda-launch.js"
cp "$SRC/assets/feedback.js" "$OUT/assets/feedback.js"
cp "$SRC/assets/oauth-bridge.js" "$OUT/assets/oauth-bridge.js"
for asset in company-logo.png company-logo-header.png company-logo.svg company-logo-header.svg \
  company-logo-mark.svg favicon.svg favicon.png app-icon.png apple-touch-icon.png \
  og-image.png og-facematch.png og-ycda.png \
  ycda-logo.png ycda-logo-transparent.png ycda-logo-header.png ycda-logo-header-nav.png ycda-logo-card.png ycda-logo-hero.png; do
  cp "$SRC/assets/$asset" "$OUT/assets/$asset"
done
mkdir -p "$OUT/assets/ycda-screenshots"
for shot in home.png classes.png tasters.png portal.png; do
  if [[ -f "$SRC/assets/ycda-screenshots/$shot" ]]; then
    cp "$SRC/assets/ycda-screenshots/$shot" "$OUT/assets/ycda-screenshots/$shot"
  fi
done
cp "$SRC/.htaccess" "$OUT/.htaccess"
cp "$SRC/robots.txt" "$OUT/robots.txt"
mkdir -p "$OUT/.well-known"
cp "$SRC/.well-known/security.txt" "$OUT/.well-known/security.txt"
cp "$SRC/README-UPLOAD.txt" "$OUT/README-UPLOAD.txt"

for platform in "${OAUTH_PLATFORMS[@]}"; do
  python3 "$ROOT/scripts/render_oauth_bridge.py" \
    "$OUT/facematch/oauth/$platform/index.html" "$platform"
done

echo "Built $OUT — upload all contents inside dist/ to your web host (see deploy/DEPLOY.md)."
