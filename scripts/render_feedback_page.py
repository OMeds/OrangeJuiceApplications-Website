#!/usr/bin/env python3
"""Build the web feedback form page."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from website_chrome import wrap_page  # noqa: E402

BODY = """
<h1>Send feedback</h1>
<p class="guide-intro">
  Report a website bug, app issue, or share feedback. Your email app opens with a structured subject
  such as <strong>Web - Bug - Page not loading</strong> so we can sort messages quickly.
</p>

<form id="feedback-form" class="feedback-form" novalidate>
  <label class="feedback-label" for="feedback-category">Type</label>
  <select id="feedback-category" class="feedback-input" name="category" required>
    <option value="Feedback">Feedback</option>
    <option value="Bug">Bug</option>
    <option value="Issue">Issue</option>
    <option value="Feature Request">Feature Request</option>
  </select>

  <label class="feedback-label" for="feedback-summary">Short summary</label>
  <input id="feedback-summary" class="feedback-input" name="summary" type="text"
    maxlength="120" placeholder="e.g. Guides page link broken" required>

  <label class="feedback-label" for="feedback-detail">Description</label>
  <textarea id="feedback-detail" class="feedback-input feedback-textarea" name="detail"
    rows="6" placeholder="What happened? What did you expect?" required></textarea>

  <p class="feedback-label">Email subject preview</p>
  <p id="feedback-subject-preview" class="feedback-preview">Web - Feedback - …</p>

  <div class="feedback-actions">
    <button type="submit" class="btn btn-primary">Email feedback</button>
    <a class="btn btn-secondary" href="mailto:support@orangejuiceapplications.com">Email support directly</a>
  </div>

  <p class="feedback-error" hidden role="alert"></p>
  <p class="feedback-success" hidden role="status"></p>
</form>

<p class="guide-footer-links">
  Using the FaceMatch app? Open <strong>Settings → Support → Send Feedback</strong> — subjects start with
  <strong>Mobile -</strong> and include app version details automatically.
</p>
"""

EXTRA_SCRIPTS = '<script src="/assets/feedback.js" defer></script>'


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_feedback_page.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1]) / "contact-profile-picture-sync/feedback"
    out.mkdir(parents=True, exist_ok=True)

    html = wrap_page(
        "Send feedback about FaceMatch or this website. Structured email subjects help us route your message.",
        "Send Feedback — FaceMatch",
        BODY,
        "/contact-profile-picture-sync/feedback/",
    )
    html = html.replace("</body>", f"  {EXTRA_SCRIPTS}\n</body>")
    out.joinpath("index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {out / 'index.html'}")


if __name__ == "__main__":
    main()
