# Troubleshooting

Common issues and how to fix them.

---

## No contacts appear

1. Open **iOS Settings → FaceMatch → Contacts** and set to **Full Access** (or allow access).
2. Force-quit and reopen FaceMatch.
3. Confirm you have contacts in Apple’s **Contacts** app.

---

## No photos found for a contact

1. Add **email**, **phone**, or a **social URL** to the contact in Apple Contacts.
2. Check **Settings → Photo Sources** — ensure relevant platforms are enabled.
3. **Account Sign-In:** try **Settings → Account Sign-In** and connect the relevant platform.
4. **Import from Files:** try **Settings → Import from Files** (LinkedIn CSV, Google Takeout, photo folder) or share a photo from Safari (contact → **Share Photo from Browser** → Share → FaceMatch).
5. Run matching again from the contact detail screen.

See [Ways to get photos](/contact-profile-picture-sync/guides/two-paths-social-networks/).

---

## LinkedIn sign-in fails

1. Confirm the redirect URL is registered in LinkedIn Developer Portal:
   `https://www.orangejuiceapplications.com/facematch/oauth/linkedin`
2. Complete sign-in in one session — don’t close the browser early.
3. If you see “authentication state mismatch”, tap **Sign In** again.

LinkedIn profile **lookups for other people** may return no results if API access is restricted — add a LinkedIn URL on the contact card.

---

## Suggestions never apply

1. Open the **Review** tab and approve manually.
2. Check auto-apply settings under **Settings → Sync & Automation**.
3. Confirm Contacts permission is still granted.

---

## Wrong photo suggested

1. **Reject** the match in Review — it won’t be applied.
2. If the contact already had a photo, on-device comparison should reduce wrong matches; adjust sources or add a clearer handle on the card.
3. Report persistent issues to [support@orangejuiceapplications.com](mailto:support@orangejuiceapplications.com) with the platform and contact type (no need to send personal contact details).

---

## Run diagnostics

1. **Settings → Privacy & Security → Photo Discovery Diagnostics**
2. Tap **Run All Discovery Tests**
3. Note any failures and include them in a support email if needed.

---

## Refunds & billing

FaceMatch is a **one-time paid App Store download**, not a subscription. For full refund steps, see the [Refunds & billing guide](/contact-profile-picture-sync/guides/refunds/). To request a refund, use Apple’s [Report a Problem](https://reportaproblem.apple.com) flow.

---

## Delete app data

**Settings → Privacy & Security → Privacy Dashboard → Delete All App Data**

This removes local app preferences and history. It does **not** delete your Apple Contacts.

---

## Still stuck?

Email [support@orangejuiceapplications.com](mailto:support@orangejuiceapplications.com) with:

- Device model and iOS version
- What you tried to do
- Screenshots if possible
- Diagnostics results (if any)

We aim to respond within **5 business days**.
