#!/usr/bin/env python3
"""Upload dist/ to Fasthosts via FTP using deploy/.deploy-credentials.env (gitignored)."""
from __future__ import annotations

import sys
from ftplib import FTP, FTP_TLS
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / "deploy" / ".deploy-credentials.env"
DIST = ROOT / "dist"


def load_env(path: Path) -> dict[str, str]:
    if not path.exists():
        print(f"Missing {path} — copy from deploy/.deploy-credentials.env.example", file=sys.stderr)
        sys.exit(1)
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()
    return values


def connect(cfg: dict[str, str]) -> FTP:
    host = cfg["FTP_HOST"]
    port = int(cfg.get("FTP_PORT", "21"))
    user = cfg["FTP_USER"]
    password = cfg["FTP_PASSWORD"]
    use_tls = cfg.get("FTP_PROTOCOL", "ftp").lower() in {"ftps", "ftpes", "tls"}

    if use_tls:
        ftp: FTP = FTP_TLS()
        ftp.connect(host, port, timeout=120)
        ftp.login(user, password)
        ftp.prot_p()
    else:
        ftp = FTP()
        ftp.connect(host, port, timeout=120)
        ftp.login(user, password)
    ftp.set_pasv(True)
    return ftp


def cwd_or_mkd(ftp: FTP, name: str) -> None:
    try:
        ftp.cwd(name)
    except Exception:
        ftp.mkd(name)
        ftp.cwd(name)


def ensure_remote_path(ftp: FTP, remote_dir: str) -> None:
    for part in [p for p in remote_dir.split("/") if p]:
        cwd_or_mkd(ftp, part)


def upload_dir(ftp: FTP, local: Path, prefix: str = "") -> int:
    count = 0
    for entry in sorted(local.iterdir()):
        if entry.name in {".", ".."}:
            continue
        if entry.name.startswith(".") and entry.name not in {".htaccess", ".well-known"}:
            continue
        rel = f"{prefix}/{entry.name}" if prefix else entry.name
        if entry.is_dir():
            cwd_or_mkd(ftp, entry.name)
            count += upload_dir(ftp, entry, rel)
            ftp.cwd("..")
        else:
            with entry.open("rb") as fh:
                print(f"  UP {rel}")
                ftp.storbinary(f"STOR {entry.name}", fh)
                count += 1
    return count


def main() -> None:
    if not DIST.is_dir() or not any(DIST.iterdir()):
        print("Run ./scripts/build.sh first — dist/ is empty or missing.", file=sys.stderr)
        sys.exit(1)

    cfg = load_env(ENV_FILE)
    remote_dir = cfg.get("FTP_REMOTE_DIR", "htdocs").strip("/")

    print(f"Connecting to {cfg['FTP_HOST']}…")
    ftp = connect(cfg)
    try:
        if remote_dir:
            ensure_remote_path(ftp, remote_dir)
        print(f"Remote directory: {ftp.pwd()}")
        print(f"Uploading {DIST} …")
        n = upload_dir(ftp, DIST)
        print(f"Done — {n} files uploaded.")
    finally:
        try:
            ftp.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
