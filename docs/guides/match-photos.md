# How to match photos for contacts

FaceMatch finds candidate profile pictures using each contact’s **name**, **email**, **phone**, and any **social profile links** already saved on the card.

---

## Match one contact

1. Open the **Contacts** tab.
2. Search or scroll to the person.
3. Tap the contact to open their detail screen.
4. Tap **Find Photo for This Contact**.
5. Wait while the app searches enabled sources on your device.
6. If a match is found, it appears in **Review** (or auto-applies if you enabled that in Settings).

**Tip:** Add an email, phone number, or LinkedIn/GitHub URL to the contact in Apple Contacts first — matching works best when the card has real identifiers.

---

## Sync many contacts at once

1. Open the **Contacts** tab.
2. Tap **Sync Social Photos** (toolbar or sync action).
3. Optionally filter to **Favorites** or contacts **missing photos** before syncing.
4. When finished, open the **Review** tab to approve suggestions.

Large address books may take several minutes. Keep the app open while sync runs.

---

## What sources are used?

**Without signing in:**

- Gravatar (from email on the contact)
- GitHub (from username or name search)
- Public profile URLs saved on the contact (Instagram, X, LinkedIn, etc.)
- WhatsApp and Telegram when phone or handle is present

**With optional sign-in:**

- LinkedIn, Google, Facebook, Microsoft, Slack, and others — see [Social sign-in guide](/contact-profile-picture-sync/guides/social-sign-in/)

Enable or disable sources under **Settings → Photo Sources**.

---

## On-device photo comparison

If the contact **already has a photo**, FaceMatch compares candidates on your device using Apple’s Vision framework. This helps avoid applying the wrong person’s image.

---

## Related guides

- [Review queue](/contact-profile-picture-sync/guides/review-queue/)
- [Manage connections per contact](/contact-profile-picture-sync/guides/manage-connections/)
- [Settings & sync options](/contact-profile-picture-sync/guides/settings-and-sync/)
