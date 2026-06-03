#!/usr/bin/env python3
"""OAuth HTTPS bridge — external JS only, no inline scripts (CSP-friendly)."""
import html
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: render_oauth_bridge.py output.html platform", file=sys.stderr)
        sys.exit(1)
    dest, platform = sys.argv[1], sys.argv[2]
    if platform not in {"linkedin"}:
        print(f"unsupported oauth platform: {platform}", file=sys.stderr)
        sys.exit(1)

    platform = html.escape(platform)
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <meta name="referrer" content="no-referrer">
  <title>FaceMatch sign-in</title>
  <link rel="icon" href="/assets/favicon.png" type="image/png" sizes="32x32">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/oauth-bridge.js" defer></script>
</head>
<body data-oauth-platform="{platform}">
  <main class="oauth-bridge">
    <section id="panel-loading" class="oauth-panel is-visible" aria-live="polite">
      <div class="oauth-status" aria-hidden="true"></div>
      <h1>Returning to FaceMatch…</h1>
      <p class="oauth-detail">Completing sign-in. The app should open automatically.</p>
    </section>

    <section id="panel-error" class="oauth-panel" aria-live="assertive">
      <h1 class="oauth-error-title" id="error-title">Sign-in could not be completed</h1>
      <p class="oauth-detail" id="error-detail"></p>
      <div class="oauth-actions">
        <a class="btn btn-primary" id="retry-link" href="facematch://oauth/{platform}">Open FaceMatch</a>
        <a class="btn btn-secondary" href="/contact-profile-picture-sync/guides/social-sign-in/">Sign-in help</a>
      </div>
    </section>

    <section id="panel-fallback" class="oauth-panel" aria-live="polite">
      <h1>App didn’t open?</h1>
      <p class="oauth-detail">Tap below to return to FaceMatch and finish connecting your account.</p>
      <div class="oauth-actions">
        <a class="btn btn-primary" id="open-app-link" href="facematch://oauth/{platform}">Open FaceMatch</a>
        <a class="btn btn-secondary" href="/contact-profile-picture-sync/guides/troubleshooting/">Troubleshooting</a>
      </div>
    </section>
  </main>
</body>
</html>
"""
    Path(dest).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
