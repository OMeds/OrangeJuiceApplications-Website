#!/usr/bin/env python3
"""Build FAQ and Security summary pages for website-deploy."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from website_chrome import wrap_page  # noqa: E402

FAQ_BODY = """
<h1>Frequently asked questions</h1>
<p>Quick answers about FaceMatch. For step-by-step help, see the <a href="/contact-profile-picture-sync/guides/">user guides</a>, <a href="/contact-profile-picture-sync/privacy/">Privacy Policy</a>, and <a href="/contact-profile-picture-sync/security/">Security summary</a>.</p>

<h2>Is my contact data uploaded to your servers?</h2>
<p><strong>No.</strong> FaceMatch reads and updates contacts on your device through Apple Contacts. We do not operate a central cloud database of your address book.</p>

<h2>Do I need to sign in to LinkedIn, Google, or Facebook?</h2>
<p><strong>No.</strong> Sign-in is optional. The app can still suggest photos from names, emails, and phone numbers on each contact card. Connecting accounts unlocks additional networks.</p>

<h2>How does photo matching work?</h2>
<p>FaceMatch discovers candidate profile photos from public sources and connected accounts, then compares them on your device. When a contact already has a photo, Apple’s on-device Vision tools help reduce wrong matches.</p>

<h2>Are changes applied automatically?</h2>
<p>You stay in control. Strong matches may auto-apply only if you enable that in settings. Otherwise suggestions go to a review queue and you choose what to apply.</p>

<h2>Is FaceMatch a subscription?</h2>
<p><strong>No.</strong> FaceMatch is a one-time paid download on the Apple App Store. There is no monthly subscription for core features.</p>

<h2>How do I send feedback or report a bug?</h2>
<p>On the website, use the <a href="/contact-profile-picture-sync/feedback/">feedback form</a> (subjects start with <strong>Web -</strong>). In the app, open <strong>Settings → Support → Send Feedback</strong> (subjects start with <strong>Mobile -</strong>).</p>

<h2>How do I get a refund?</h2>
<p>Refunds are handled by <strong>Apple</strong>, not Orange Juice Applications. Use Apple’s <a href="https://reportaproblem.apple.com" rel="noopener">Report a Problem</a> page or contact Apple Support. See our full <a href="/contact-profile-picture-sync/guides/refunds/">Refunds &amp; billing guide</a>.</p>

<h2>How do I delete my data?</h2>
<p>Remove photos or contacts in Apple Contacts, disconnect social accounts in the app, or use in-app wipe tools under Settings. Email <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a> for data-rights requests.</p>

<h2>Who makes FaceMatch?</h2>
<p>FaceMatch is published by <strong>Orange Juice Applications</strong>, an independent app studio. Support: <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a>.</p>
"""

SECURITY_BODY = """
<h1>Security &amp; privacy summary</h1>
<p>A plain-language overview of how FaceMatch handles your information. This is a summary — the full <a href="/contact-profile-picture-sync/privacy/">Privacy Policy</a> controls if anything differs.</p>

<h2>On your device first</h2>
<ul>
  <li>Contacts are read and updated through Apple Contacts on your iPhone or iPad.</li>
  <li>Matching preferences, saved social links, and review history are stored locally on your device.</li>
  <li>Photo comparison for existing contact photos uses Apple’s on-device Vision framework — not a server-side face database.</li>
</ul>

<h2>Optional sign-in</h2>
<ul>
  <li>Social and workplace sign-in is optional and only activated when you choose to connect an account.</li>
  <li>OAuth tokens are stored in the iOS Keychain on your device.</li>
  <li>When connected, the app requests profile information from the provider you signed into (for example LinkedIn or Google) to suggest photos.</li>
</ul>

<h2>What we don’t do</h2>
<ul>
  <li>We don’t sell contact lists or build advertising profiles from your address book.</li>
  <li>We don’t upload your full contact database to Orange Juice Applications servers.</li>
  <li>We don’t apply profile photo changes without your approval (unless you explicitly enable automatic apply for high-confidence matches).</li>
</ul>

<h2>Network requests</h2>
<p>The app may fetch public profile images or provider APIs over HTTPS when you run a sync or sign in. Those requests originate from your device to the relevant service — not through a contact-upload pipeline we operate.</p>

<h2>Your controls</h2>
<ul>
  <li>Disconnect any linked account at any time.</li>
  <li>Revoke Contacts permission in iOS Settings.</li>
  <li>Use in-app data wipe tools to remove local app data.</li>
  <li>Contact <a href="mailto:privacy@orangejuiceapplications.com">privacy@orangejuiceapplications.com</a> for privacy questions or data-rights requests.</li>
</ul>

<h2>Reporting issues</h2>
<p>If you discover a security concern, email <a href="mailto:support@orangejuiceapplications.com">support@orangejuiceapplications.com</a> with enough detail for us to reproduce the issue.</p>
"""


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_static_pages.py output_dir", file=sys.stderr)
        sys.exit(1)
    out = Path(sys.argv[1])
    faq_dir = out / "contact-profile-picture-sync/faq"
    security_dir = out / "contact-profile-picture-sync/security"
    faq_dir.mkdir(parents=True, exist_ok=True)
    security_dir.mkdir(parents=True, exist_ok=True)

    faq_dir.joinpath("index.html").write_text(
        wrap_page(
            "FaceMatch FAQ",
            "Frequently asked questions about FaceMatch — privacy, sign-in, matching, and pricing.",
            FAQ_BODY,
            "/contact-profile-picture-sync/faq/",
        ),
        encoding="utf-8",
    )
    security_dir.joinpath("index.html").write_text(
        wrap_page(
            "FaceMatch Security & Privacy",
            "How FaceMatch protects your contacts — on-device processing, optional sign-in, and your controls.",
            SECURITY_BODY,
            "/contact-profile-picture-sync/security/",
        ),
        encoding="utf-8",
    )
    print(f"Wrote FAQ and Security pages under {out}")


if __name__ == "__main__":
    main()
