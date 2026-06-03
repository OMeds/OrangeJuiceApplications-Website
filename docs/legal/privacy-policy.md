# Privacy Policy

**Effective date:** 29 May 2026  
**Version:** 3.2  
**Last reviewed:** 29 May 2026

**Application:** FaceMatch  
**Data controller / operator:** Orange Juice Applications (“Orange Juice Applications”, “we”, “us”, “our”)  
**Apple bundle identifier:** OrangeJuiceApplications.FaceMatch  
**Privacy contact:** privacy@orangejuiceapplications.com  
**Support contact:** support@orangejuiceapplications.com  
**Policy URL:** https://www.orangejuiceapplications.com/contact-profile-picture-sync/privacy

---

## 1. Introduction and scope

This Privacy Policy explains how Orange Juice Applications processes personal information when you download, install, or use the FaceMatch mobile application for Apple iOS, iPadOS, and related platforms distributed through the Apple App Store (the “App”).

This policy applies to:

- processing performed **on your device** to display contacts, suggest profile photos, store preferences, and write photos you approve to Apple Contacts; and  
- processing performed **when you optionally connect** third-party social or workplace accounts, which causes API requests from your device to those providers.

This policy does **not** apply to:

- Apple Inc.’s processing as platform operator (Contacts, iCloud, App Store, StoreKit, Keychain, background tasks);  
- third-party websites, APIs, or social networks you choose to connect; or  
- any future web dashboard or support portal we operate outside the App (those will publish their own notices).

If you do not agree with this policy, do not use the App.

---

## 2. Plain-language summary

| Topic | What we do |
|--------|------------|
| Address book | Read Apple Contacts on your device; write photos only when you confirm. |
| Cloud import | We **do not** import contact lists from Google Contacts or other cloud address books. |
| Matching | Use names; emails/phones when on the card; on-device Vision comparison when a contact photo exists. |
| Saved connections | Store platform + handle per contact on-device for faster re-matching. |
| Sign-in | Optional OAuth; tokens in Keychain; not required for basic use. |
| Servers | We do **not** upload your address book to our servers. |
| Sale of data | We do **not** sell your personal information. |
| Your controls | Privacy Dashboard: export (encrypted), disconnect providers, delete local app data. |

---

## 3. Definitions

- **“Personal information”** / **“personal data”** means information relating to an identified or identifiable natural person.  
- **“Contacts data”** means information from Apple Contacts (names, emails, phones, photos, identifiers, organization fields).  
- **“Processing”** means any operation on personal data (collection, storage, use, disclosure, erasure).  
- **“You”** means the individual user of the App.  
- **“App purchase”** means the one-time fee you pay Apple to download the App on the App Store (all features are included; no separate subscription is required in current versions).

---

## 4. Categories of information we process

### 4.1 Apple Contacts (core functionality)

**What:** Contact identifiers, display names, given/family names, nicknames, organization name and job title, email addresses, phone numbers, existing contact photos and thumbnails.

**Why:** To list contacts, filter and search, suggest profile photos, compare candidates on-device, and write the image you select to the contact record.

**Legal basis (EEA/UK):** Performance of a contract with you (providing the App) and/or steps at your request before entering a contract.

**Storage:** Primarily in the iOS Contacts database (controlled by Apple and you). The App reads via Apple’s Contacts framework.

**Upload to us:** None. We do not maintain a server-side copy of your address book.

### 4.2 Saved social connections and linked sources

**What:** Platform identifier (e.g. GitHub, LinkedIn), account reference (username, vanity name, email for Gravatar), sync metadata, timestamps, auto-sync preferences.

**Why:** To remember your choices, speed up later matching, and drive optional automated sync for linked contacts.

**Legal basis:** Your instructions when you save or approve a connection; legitimate interest in providing a consistent experience.

**Storage:** On-device (UserDefaults / local app storage).

### 4.3 Approved match preferences

**What:** Per-contact, per-platform records of photos you approved, including display name matched, reference string, optional image URL, approval timestamp.

**Why:** To auto-prefer your prior choices and reduce repeated review.

**Storage:** On-device.

### 4.4 Optional OAuth and platform sessions

**What:** OAuth access tokens, refresh tokens where applicable, session state, connected account identifiers permitted by each provider’s API.

**Why:** To discover or fetch profile information and images when you sign in to Facebook, LinkedIn, Instagram, Microsoft, X, Discord, Slack, or other supported providers.

**Storage:** iOS Keychain and local session records.

**Providers’ policies:** Each platform’s terms and privacy policy govern their processing when their API is called from your device.

### 4.5 Network and image data

**What:** HTTPS requests to approved hosts to download public profile image URLs; response bytes temporarily in memory; optional cached references (URL, platform, account reference, fetch status).

**Why:** To preview and apply images you request.

**On-device processing:** When a contact already has a photo, the App may compare candidate images using Apple’s Vision framework **on your device**. We do not upload your contact photos to our servers for reverse-image search.

**Security:** Remote image URLs must pass in-app URL policy (HTTPS, allowed hosts). A stricter on-device mode can disable third-party avatar resolvers.

### 4.6 Photos you upload

**What:** Image data you pick from the photo library; file references in app storage.

**Why:** To apply a library photo as a contact profile picture.

**Permission:** Photo library access only when you initiate an upload.

### 4.7 Diagnostics, audit, and history

**What:**  
- Photo change audit log (what changed, when, source description);  
- Optional photo history snapshots before changes;  
- Review queue entries for suggested photos;  
- Photo discovery self-test results and error diagnostics;  
- Local support tickets you create in Settings.

**Why:** Troubleshooting, App Review demonstration, your ability to revert photos, and QA.

**Transmission:** Not sent automatically to us. You may export diagnostics locally.

### 4.8 Biometric lock (optional)

**What:** No biometric data is stored by us. iOS LocalAuthentication verifies Face ID / Touch ID.

**Why:** Optional gate before showing contacts or applying changes.

### 4.9 Purchases

**What:** We do not receive your payment card number. Apple processes the one-time App Store purchase. The App does not use recurring subscription entitlements in current versions.

**Why:** Apple confirms you acquired the App; we do not maintain a separate billing profile.

**Processor:** Apple is merchant of record.

### 4.10 Widget and Siri / Shortcuts

**What:** Limited app state (e.g. pending review count) in App Group shared preferences for widget display; shortcut intents you run.

**Why:** Home screen widget and system shortcuts described in the App.

**Storage:** App Group container on-device.

---

## 5. Purposes of processing

We process personal information to:

1. Provide contact browsing, search, favorites, and filters;  
2. Discover and suggest profile photos from public sources and connected accounts;  
3. Let you review, approve, dismiss, or revert photo changes;  
4. Save per-platform connections you specify;  
5. Operate automation, background sync, bulk review, sync engine, conflict center, and dashboard;  
6. Maintain security (URL policy, audit trail, error mapping);  
7. Comply with law and respond to lawful requests;  
8. Improve the App using aggregated, non-identifying technical feedback where applicable.

We do **not** use Contacts data to build cross-app advertising profiles or to sell contact lists.

---

## 6. Legal bases (EEA, UK, and similar regimes)

Where the GDPR or UK GDPR applies:

| Processing | Typical legal basis |
|------------|---------------------|
| Core contact features | Contract / pre-contract steps |
| Optional sign-in & automation | Consent and/or legitimate interest (you can disconnect) |
| Security & abuse prevention | Legitimate interest |
| Legal obligations | Legal obligation |
| App purchase via Apple | Contract |

You may withdraw consent for optional features by disconnecting providers and disabling automation without affecting free-tier manual matching, subject to technical limitations.

---

## 7. Sharing and recipients

We do **not** sell personal information.

We disclose information only as follows:

1. **Apple** — as part of operating iOS, Contacts, StoreKit, Keychain, background tasks, and App Store distribution.  
2. **Third-party platforms you connect** — when your device calls their APIs under their policies.  
3. **Content delivery networks** — when fetching public image URLs you triggered (e.g. Slack CDN, platform avatar hosts allowed by security settings).  
4. **Professional advisers or authorities** — where required by law, court order, or to protect rights, safety, and security.  
5. **Business transfers** — if we merge or sell assets, subject to confidentiality and notice where required by law.

We do not share Contacts data with data brokers.

---

## 8. International transfers

Most processing occurs **on your device** in your country.

When you connect a provider headquartered outside your country (e.g. United States), that provider may process data under its own transfer tools (Standard Contractual Clauses, UK IDTA, etc.) when their API is invoked from your device.

We do not operate a central database of your contacts in a fixed country.

---

## 9. Retention

We retain data only as long as needed for the purposes above or as required by law.

| Category | Retention | Erasure |
|----------|-----------|---------|
| Contacts on device | Until you change/delete in Contacts | iOS Contacts app |
| App-local data | Until you delete or uninstall | Privacy Dashboard → Delete All App Data |
| Keychain tokens | Until disconnect/wipe | Disconnect All Providers / wipe |
| GDPR export file | Until you delete the file | Files app |

See **Data Retention & Deletion** in Legal Documents for the full schedule.

---

## 10. Security measures

We implement measures appropriate to a consumer iOS app, including:

- HTTPS-only remote image fetching with host allow lists;  
- Keychain storage for OAuth secrets;  
- Optional biometric app lock;  
- On-device Vision comparison without server upload of contact photos;  
- No centralized storage of your address book.

No system is perfectly secure. You are responsible for device passcode, Apple ID security, and physical access to your device.

---

## 11. Automated processing

The App may rank matches and auto-apply high-confidence suggestions when you enable automation or thresholds. You can:

- require manual review for close matches;  
- use the review queue;  
- revert via photo history;  
- override saved connections per platform.

You are not subject to solely automated decisions with legal or similarly significant effects outside photo suggestions for contacts you manage.

---

## 12. Your rights

Depending on your location, you may have rights to **access**, **rectify**, **erase**, **restrict**, **object**, **port**, and **withdraw consent**, and to lodge a complaint with a supervisory authority.

**In the App:**  
- **GDPR Data Export** — encrypted export of local app data you control;  
- **Delete All App Data** — erases local app processing data (not entire Contacts database);  
- **Disconnect All Providers** — removes OAuth sessions.

**By email:** privacy@orangejuiceapplications.com — we will respond within timeframes required by applicable law (e.g. one month under GDPR, subject to extension where permitted).

We may need to verify your identity before fulfilling requests.

---

## 13. United States state notices

### 13.1 California (CCPA/CPRA)

**Categories collected (last 12 months, via App):** identifiers (contact IDs, handles); personal information (names, emails, phones, photos); internet activity (image fetch URLs locally processed).

**Sources:** You, your device, Apple Contacts, optional connected platforms, public profile endpoints.

**Business purposes:** Provide the App, security, debugging, compliance.

**Sale / sharing for cross-context behavioral advertising:** None.

**Sensitive personal information:** Contact photos — used only to provide the App as you direct; we do not use for inferring characteristics unrelated to the service.

**Rights:** Know, delete, correct, opt out of sale (N/A), limit use of sensitive PI (N/A for our use), non-discrimination. Use in-app tools or email privacy@orangejuiceapplications.com.

### 13.2 Other US states

Residents of states with comprehensive privacy laws (e.g. Virginia, Colorado, Connecticut, Utah) may have similar rights. Contact us at the privacy email above.

---

## 14. Children

The App is not directed to children under **16** (or the minimum age in your jurisdiction). We do not knowingly collect personal information from children. If you believe a child provided information, contact us and we will take appropriate steps to delete local data where feasible.

---

## 15. Third-party links and services

The App may reference or connect to third-party services. Their privacy practices are their own. Review each provider’s policy before signing in.

---

## 16. Changes to this policy

We may update this Privacy Policy. When we do, we will change the effective date and bundled legal version in the App. Material changes may be highlighted in release notes or in-app notice where appropriate.

Continued use after the effective date constitutes acceptance where permitted by law. If you disagree, stop using the App and contact Apple regarding refund eligibility.

---

## 17. Contact and complaints

**Privacy inquiries:** privacy@orangejuiceapplications.com  
**General support:** support@orangejuiceapplications.com  

**UK/EEA users** may complain to your local data protection authority. UK ICO: https://ico.org.uk/

---

*End of Privacy Policy*
