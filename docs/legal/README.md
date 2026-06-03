# Legal documentation

Full, publishable legal documents for **FaceMatch** (version **3.3**, effective **29 May 2026**).

## Documents

| File | In-app title |
|------|----------------|
| [privacy-policy.md](./privacy-policy.md) | Privacy Policy |
| [terms-of-use.md](./terms-of-use.md) | Terms of Use (EULA) |
| [subscription-terms.md](./subscription-terms.md) | App Purchase & Pricing Terms |
| [data-retention.md](./data-retention.md) | Data Retention & Deletion |
| [acceptable-use.md](./acceptable-use.md) | Acceptable Use Policy |
| [support.md](./support.md) | Support Information |

## Source of truth workflow

1. **Edit** the markdown files in this folder (`docs/legal/`).
2. **Sync** into the app bundle:
   ```bash
   ./Scripts/sync_legal_docs.sh
   ```
3. **Bump** `LegalPublisherInfo.bundledLegalVersion` in the Xcode project when you change policy text (forces in-app refresh).
4. **Publish** the same markdown (or HTML rendered from it) at:
   - https://www.orangejuiceapplications.com/contact-profile-picture-sync/privacy
   - https://www.orangejuiceapplications.com/contact-profile-picture-sync/terms
5. **Verify** Security Disclosure, Privacy Dashboard, and README still match.

The iOS app loads `FaceMatch/Legal/*.md` at runtime and displays plain-text versions under **Settings → Help & Legal → Legal Documents**.

## Publisher

- **Operator:** Orange Juice Applications  
- **Bundle ID:** OrangeJuiceApplications.FaceMatch  
- **Privacy:** privacy@orangejuiceapplications.com  
- **Support:** support@orangejuiceapplications.com  

Update emails and URLs in `LegalPublisherInfo.swift` before App Store submission if production values differ.

## Disclaimer

These documents are drafted to match the app’s implemented behavior. They are not a substitute for advice from a qualified lawyer in your jurisdiction.
