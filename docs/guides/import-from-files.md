# Import from files

Use **Import from Files** when you have a social network export, a folder of named photos, or images saved from Safari — no account sign-in required.

---

## Open Import from Files

1. Open the **Settings** tab in FaceMatch.
2. Tap **Import from Files**.
   - Also available from **Settings → Help & Legal → Import from Files**
   - Or **Settings → Account Sign-In → Import from Files (exports & photo folders)**
3. Pick an **Import Type** below.
4. Tap **Choose File…** and select your export.
5. Review the import summary, then open **Review Queue** if photos were found.
6. Approve suggestions in the **Review** tab before they update Apple Contacts.

All parsing happens **on your device**. FaceMatch does not upload your export to a server.

---

## Import types

### Photo folder or ZIP

**Use when:** You have images named like `Jane Smith.jpg` or saved profile photos.

1. **Settings → Import from Files**
2. Import Type: **Photo Folder or ZIP**
3. Choose a folder or ZIP of `.jpg`, `.png`, or `.heic` files.
4. FaceMatch matches filenames to contact names and queues photos for review.

### LinkedIn Connections export

**Use when:** You want to add LinkedIn profile URLs to contacts by name.

1. On **desktop LinkedIn**: Me → **Settings & Privacy** → **Data privacy** → **Get a copy of your data** → check **Connections** → Request archive.
2. Download the ZIP when LinkedIn emails you (contains `Connections.csv`).
3. In FaceMatch: **Settings → Import from Files** → **LinkedIn Connections Export** → choose the ZIP or CSV.
4. FaceMatch adds profile URLs to matching contacts and queues photos when possible.

### Google Takeout (vCard or CSV)

**Use when:** You want to match iOS contacts to your Google address book without signing in.

1. Visit [Google Takeout](https://takeout.google.com) → select **Contacts** only → **vCard** or **CSV** format → create export.
2. Download the ZIP when ready.
3. In FaceMatch: **Settings → Import from Files** → **Google Contacts (vCard)** or **Google Contacts (CSV)** → choose the file.
4. FaceMatch matches by name or email and fetches photo URLs when present in the export.

### Facebook friends JSON

**Use when:** You want name hints from your Facebook friend list (photos are not included in the export).

1. **Meta Accounts Center** → **Your information and permissions** → **Download your information**.
2. Select **Some of your information** → **Friends and followers** → **JSON** format → create files.
3. Download the ZIP when Meta notifies you.
4. In FaceMatch: **Settings → Import from Files** → **Facebook Friends Export** → choose the ZIP or `friends.json`.

For photos, add Facebook profile URLs to contacts and use **Account Sign-In**, or save photos manually from Safari.

### Instagram followers JSON

**Use when:** You want to add @handles to contacts from your followers/following list.

1. **Meta Accounts Center** → **Download your information** → **Followers and following** → **JSON**.
2. Download the ZIP (files like `followers_1.json`, `following.json`).
3. In FaceMatch: **Settings → Import from Files** → **Instagram Followers Export** → choose the ZIP or JSON.

Then run sync or sign in with a Business/Creator account to resolve photos for those handles.

---

## Share a photo from Safari

When you do not have an export:

1. Open a contact in FaceMatch.
2. Tap a row under **Share Photo from Browser** (Facebook, LinkedIn, Instagram, etc.).
3. In Safari, long-press the profile photo → **Share** → **FaceMatch**.
4. Return to FaceMatch — the photo is applied automatically.

**Fallback:** save to Photos, then **Choose Photo from Library** on the same contact.

---

## After import

- **Review tab** — approve or reject queued photo suggestions.
- **Contacts → Sync Social Photos** — run again after URLs were added to contact cards.
- **Account Sign-In** — connect accounts under **Settings → Account Sign-In** for automated API lookups.

---

## Related guides

- [Ways to get photos](/contact-profile-picture-sync/guides/two-paths-social-networks/)
- [Social sign-in](/contact-profile-picture-sync/guides/social-sign-in/)
- [Manage connections on a contact](/contact-profile-picture-sync/guides/manage-connections/)
