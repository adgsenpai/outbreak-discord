#!/usr/bin/env bash
# One-line installer for the Outbreak Discord Rich Presence companion (Linux x86_64).
#   curl -fsSL https://raw.githubusercontent.com/adgsenpai/outbreak-discord/main/scripts/install.sh | bash
# Downloads the latest release binary and installs it as a systemd user service
# (or a login autostart entry where systemd isn't available).
set -euo pipefail
URL="https://github.com/adgsenpai/outbreak-discord/releases/latest/download/outbreak-discord-companion-linux-x86_64"
here="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo .)"
if [ -x "$here/outbreak-discord-companion-linux-x86_64" ]; then
  bin="$here/outbreak-discord-companion-linux-x86_64"
else
  bin="$(mktemp)"
  trap 'rm -f "$bin"' EXIT
  echo "Downloading the companion..."
  curl -fsSL "$URL" -o "$bin"
  chmod +x "$bin"
fi
"$bin" --install
