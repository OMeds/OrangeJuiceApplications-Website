# Data Retention & Deletion Schedule

**Effective date:** 29 May 2026  
**Version:** 3.2  
**Application:** FaceMatch  
**Operator:** Orange Juice Applications

This document describes how long categories of data are kept and how you can delete them. It implements practices stated in our **Privacy Policy** and matches behavior of the in-app **Privacy Dashboard** and **DataWipeService**.

We do **not** operate a server-side copy of your address book.

---

## 1. How to delete data quickly

| Goal | Action |
|------|--------|
| Erase all local app data | Settings → Privacy Dashboard → **Delete All App Data** |
| Disconnect social logins only | Privacy Dashboard → **Disconnect All Providers** |
| Remove one platform link for a contact | Contact → **Manage Connections** → delete / swipe |
| Remove a photo from a contact | iOS Contacts app or revert via **Photo History** in the App |
| Export your data | Privacy Dashboard → **GDPR Data Export** (encrypted file) |

**Delete All App Data** removes items in Section 3 below except Apple Contacts entries themselves. Photos you already wrote to Contacts **remain** until you change them in Contacts or the App.

---

## 2. Retention principles

1. **On-device by default** — Processing data stays on your iPhone/iPad unless you export it.  
2. **Until you delete** — Most categories persist until you wipe, disconnect, or uninstall.  
3. **No fixed maximum period** — We do not archive your contacts on our servers.  
4. **Legal holds** — We may retain minimal records if required by law (e.g. response to lawful process); this App design minimizes server-held data.

---

## 3. Category schedule

### 3.1 Apple Contacts

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Names, emails, phones, org fields | iOS Contacts database | Until you edit/delete in Contacts | Apple Contacts app |
| Profile photos you applied | Same contact record | Until you replace/remove | Contacts app or App photo history revert |

**Not deleted** by “Delete All App Data”.

---

### 3.2 Linked profiles & saved social connections

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Platform type, handle/reference, sync flags | App local storage (`linked_profiles`) | Until removed or wipe | Manage Connections; Delete All App Data |

---

### 3.3 Approved match preferences

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Per-contact, per-platform approved references | `approved_match_records` | Until removed or wipe | Delete All App Data; update connection |

---

### 3.4 OAuth tokens & platform sessions

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Access/refresh tokens, session metadata | iOS Keychain + local session store | Until disconnect or wipe | Disconnect All Providers; Delete All App Data |

---

### 3.5 Uploaded photos

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Library uploads you saved | Application Support / ContactPhotoUploads | Until wipe | Delete All App Data |

---

### 3.6 Photo history snapshots

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Prior images before changes | App photo history storage | Until wipe | Delete All App Data |

---

### 3.7 Photo change audit log

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Who changed what, source description, timestamp | Local audit log | Until wipe | Delete All App Data |

---

### 3.8 Review queue

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Pending suggested photos | `review_queue_items` | Until apply/dismiss or wipe | Review tab; Delete All App Data |

---

### 3.9 Remote profile & image asset cache

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Cached URLs, fetch status, account references | `remote_profiles`, `remote_image_assets` | Until wipe | Delete All App Data |

---

### 3.10 Discovery diagnostics

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Self-test results, scoring logs | `photo_discovery_diagnostics_log` | Until clear/export/wipe | Diagnostics screen; Delete All App Data |

---

### 3.11 Sync preferences & favorites

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Enabled platforms, favorites, automation prefs | `sync_preferences`, related keys | Until wipe (favorites reset) | Delete All App Data |

---

### 3.12 Contact groups & platform accounts metadata

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Groups, linked platform account summaries | `contact_groups`, `linked_platform_accounts` | Until wipe | Delete All App Data |

---

### 3.13 Security & onboarding state

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Biometric lock prefs, URL policy, onboarding flags | `app_security_settings`, `onboarding_state` | Security reset on wipe; onboarding may reset | Delete All App Data |

---

### 3.14 Widget & App Group state

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Pending review count for widget | App Group UserDefaults | Until wipe / update | Delete All App Data |

---

### 3.15 Support tickets (local)

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Tickets you create in Settings → Support | Local only (not auto-sent) | Until you tap Clear Tickets | Support view |

---

### 3.16 GDPR export files

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Encrypted `.cpsenc` export | iOS temporary directory | Until you delete the file | Files app / delete export |

---

### 3.17 Legal documents (in-app text)

| Element | Location | Retention | Deletion |
|---------|----------|-----------|----------|
| Bundled Privacy Policy, Terms, etc. | App binary + cached copy | Updated when **bundled legal version** changes on app update | Not user-deletable; read in Settings → Legal Documents |

---

## 4. Uninstalling the app

Removing the App from your device deletes the app container and most local files subject to iOS behavior. **Keychain** entries may persist until explicitly cleared via wipe before uninstall or by iOS. Reinstalling starts with fresh local state unless iCloud Keychain restores items (provider-dependent).

---

## 5. Backups

Device **iCloud** or **iTunes/Finder** backups may include Contacts and app data per Apple’s backup rules. We do not control backup retention. Manage backups in iOS settings.

---

## 6. Questions

privacy@orangejuiceapplications.com

---

*End of Data Retention & Deletion Schedule*
