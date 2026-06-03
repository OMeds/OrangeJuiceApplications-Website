# Deploy to Fasthosts (FileZilla)

## 1. Build

```bash
./scripts/build.sh
```

Upload everything **inside** `dist/` to your web root (`htdocs` on Fasthosts), not the `dist` folder itself.

## 2. Connect FileZilla

### Option A — Import site profile (recommended)

1. Copy credentials template:
   ```bash
   cp deploy/.deploy-credentials.env.example deploy/.deploy-credentials.env
   ```
2. Edit `deploy/.deploy-credentials.env` with your Fasthosts FTP host, username, password, and remote directory (usually `/htdocs` or `/public_html`).
3. Generate a FileZilla site entry (macOS/Linux):
   ```bash
   ./deploy/generate-filezilla-site.sh
   ```
4. In **FileZilla → File → Import**, choose `deploy/filezilla-sitemanager.xml` (or merge manually — see below).
5. Open **Site Manager** (⌘U / Ctrl+S), select **Orange Juice Applications — Fasthosts**, click **Connect**.

### Option B — Manual site entry

| Field | Typical Fasthosts value |
|-------|-------------------------|
| Protocol | FTP — File Transfer Protocol |
| Host | From Fasthosts control panel (e.g. `ftp.yourdomain.com` or server hostname) |
| Port | `21` (or `22` for SFTP if enabled) |
| Logon Type | Normal |
| User / Password | FTP account from hosting panel |
| Default remote directory | `/htdocs` |

**Transfer settings:** Binary for images; allow overwrite when updating.

**Local directory:** `<repo>/dist`  
**Remote directory:** `/htdocs` (or your document root)

## 3. Upload workflow

1. Connect via FileZilla.
2. Left pane: local `dist/`.
3. Right pane: remote `htdocs/`.
4. Select all files and folders in `dist/`, upload (drag or right-click → Upload).
5. Confirm `index.html`, `.htaccess`, `assets/`, `facematch/`, `ycda/`, `contact-profile-picture-sync/` exist on the server.
6. Test: `https://www.orangejuiceapplications.com/`

## 4. Merge into existing FileZilla Site Manager (macOS)

FileZilla stores sites at:

`~/Library/Application Support/FileZilla/sitemanager.xml`

Back up that file, then either import `deploy/filezilla-sitemanager.xml` or copy the `<Server>` block from the generated XML into your existing `<Servers>` section.

## Security

- Never commit `deploy/.deploy-credentials.env` or `deploy/filezilla-sitemanager.xml` (both are gitignored).
- Use SFTP if Fasthosts provides it.
