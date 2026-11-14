Show the Resident Evil Outbreak stage you're playing on [outbreakweb.com](https://outbreakweb.com) as your Discord status, with stage art, character and room.

## Install (2 steps)

**1. Companion app** (connects Chrome to the Discord desktop app)

- **Windows:** download **`OutbreakDiscordCompanion.exe`** and double-click it. It installs itself, starts in the background, and starts with Windows from then on.
  - Windows SmartScreen may warn because the app isn't code-signed. Click **More info → Run anyway**.
  - To uninstall, run `%LOCALAPPDATA%\OutbreakDiscord\OutbreakDiscordCompanion.exe --uninstall`.
- **Linux (x86_64):** run
  ```bash
  curl -fsSL https://raw.githubusercontent.com/adgsenpai/outbreak-discord/main/scripts/install.sh | bash
  ```
  It installs a systemd user service that starts at login. To uninstall, run `~/.local/bin/outbreak-discord-companion --uninstall`.

**2. Chrome extension**

Download **`outbreak-discord-extension-v*.zip`** and unzip it. Open `chrome://extensions`, turn on **Developer mode**, click **Load unpacked**, and pick the unzipped folder.

Then play at https://outbreakweb.com/file1/ or /file2/. There's no account and no token to paste. Make sure the Discord **desktop** app is running and **Settings → Activity Privacy → Share your activity** is on.

## Files

| File | What it is |
|---|---|
| `OutbreakDiscordCompanion.exe` | Windows companion (self-installing) |
| `outbreak-discord-companion-linux-x86_64` | Linux companion binary (`--install` to set up autostart) |
| `install-linux.sh` | The Linux one-line installer |
| `outbreak-discord-extension-v*.zip` | Chrome extension |
| `SHA256SUMS.txt` | Checksums |
