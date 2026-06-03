#!/usr/bin/env bash
# Build deploy/filezilla-sitemanager.xml from .deploy-credentials.env for FileZilla import.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/deploy/.deploy-credentials.env"
OUT="$ROOT/deploy/filezilla-sitemanager.xml"
TEMPLATE="$ROOT/deploy/filezilla-site.template.xml"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Create $ENV_FILE from deploy/.deploy-credentials.env.example first." >&2
  exit 1
fi

# shellcheck source=/dev/null
source "$ENV_FILE"

: "${FTP_HOST:?FTP_HOST required}"
: "${FTP_USER:?FTP_USER required}"
: "${FTP_PASSWORD:?FTP_PASSWORD required}"
FTP_PORT="${FTP_PORT:-21}"
PASS_B64=$(printf '%s' "$FTP_PASSWORD" | base64 | tr -d '\n')

sed \
  -e "s|FTP_HOST_PLACEHOLDER|${FTP_HOST}|g" \
  -e "s|FTP_PORT_PLACEHOLDER|${FTP_PORT}|g" \
  -e "s|FTP_USER_PLACEHOLDER|${FTP_USER}|g" \
  -e "s|FTP_PASS_B64_PLACEHOLDER|${PASS_B64}|g" \
  "$TEMPLATE" > "$OUT"

echo "Wrote $OUT"
echo "FileZilla → File → Import → select this file, or merge into Site Manager."
