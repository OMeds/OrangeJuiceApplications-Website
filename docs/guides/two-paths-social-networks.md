# Ways to get photos from social networks

FaceMatch gives you **three options** for Facebook, Instagram, LinkedIn, Google, and other networks. Use whichever fits — you can mix them.

| Option | Best for | Where in the app |
|--------|----------|------------------|
| **Account Sign-In** | Automated matching from official APIs when you connect an account | **Settings → Account Sign-In** |
| **Import from Files** | Exports you download yourself, or photos saved from Safari | **Settings → Import from Files** |
| **Share from Safari** | One-off profile photos when you do not have an export | Contact → **Share Photo from Browser** |

None of these are required. FaceMatch always matches from names, emails, phones, and profile URLs already saved on contact cards.

---

## Before you start

1. Open **Contacts** in FaceMatch and pick a person.
2. Tap **Edit Contact** and add profile URLs or @handles (Facebook, LinkedIn, Instagram, etc.).
3. Return to the contact and run **Find Photo for This Contact**, or use **Sync Social Photos** for bulk matching.
4. Open the **Review** tab to approve suggestions before they update Apple Contacts.

Adding profile links to contacts gives the best results on Facebook, Instagram, and LinkedIn.

---

## Account Sign-In

Use this when you want FaceMatch to call official APIs after you connect an account.

### Steps

1. Open the **Settings** tab.
2. Tap **Account Sign-In** (also under **Accounts & Activity**).
3. Choose a platform (Facebook, Instagram, LinkedIn, Google, Microsoft, Slack, X, Discord).
4. Tap **Sign In** and complete login in the browser sheet.
5. Return to FaceMatch — the platform should show **Connected**.
6. Go to **Settings** → **Sync Preferences** and ensure the platform is **enabled**.
7. Open **Contacts** → **Sync Social Photos**, or match one contact at a time.
8. Check the **Review** tab for suggestions.

### Platform limits

- **Settings → How to Get Photos** — requirements per network (Instagram Business/Creator, Meta testers, etc.).
- From **Account Sign-In**, open **Import from Files** if sign-in is not available for your account type.

See [Social sign-in](/contact-profile-picture-sync/guides/social-sign-in/) for per-platform details.

---

## Import from Files

Use this when you have a data export from a social network or a folder of named photos.

### Steps

1. Open the **Settings** tab.
2. Tap **Import from Files** (also under **Accounts & Activity** or **Help & Legal**).
3. Choose an **Import Type** (photo folder, LinkedIn CSV, Google Takeout, Facebook JSON, Instagram JSON).
4. Tap **Choose File…** and select the export ZIP, CSV, vCard, or folder.
5. FaceMatch parses the file **on your device** — nothing is uploaded to a server.
6. When import finishes, tap **Open Review Queue** if photos were queued.
7. Approve matches in the **Review** tab before they update Contacts.

See [Import from files](/contact-profile-picture-sync/guides/import-from-files/) for export download steps per network.

---

## Share from Safari

Use this when you do not have an export:

1. Open a contact in FaceMatch.
2. Under **Share Photo from Browser**, tap the platform row to open Safari.
3. Long-press the profile photo → **Share** → **FaceMatch**.
4. Return to FaceMatch — the photo is applied to that contact automatically.

**Fallback:** save to Photos, then use **Choose Photo from Library** on the contact screen.

---

## Which option for each network?

| Network | Account Sign-In | Import / manual |
|---------|-----------------|-----------------|
| **Facebook** | Graph API for profile links + app friends | Meta friends JSON; photo folder; Safari save |
| **Instagram** | Business Discovery for @handles (Business/Creator account) | Followers/following JSON; Safari save |
| **LinkedIn** | API for vanity URLs on contact cards | Connections.csv export; Safari save |
| **Google** | Google Contacts by email when signed in | Google Takeout vCard/CSV |
| **Microsoft / Slack** | Workplace directory when emails match | Outlook CSV; photo folder |
| **X / Discord** | @handles on cards when signed in | Photo folder; Safari save |
| **GitHub / Gravatar / Telegram / WhatsApp** | Public lookup from card (no sign-in) | Photo folder |

---

## Related guides

- [Social sign-in](/contact-profile-picture-sync/guides/social-sign-in/)
- [Import from files](/contact-profile-picture-sync/guides/import-from-files/)
- [Manage connections on a contact](/contact-profile-picture-sync/guides/manage-connections/)
- [Match photos](/contact-profile-picture-sync/guides/match-photos/)
- [Review queue](/contact-profile-picture-sync/guides/review-queue/)
