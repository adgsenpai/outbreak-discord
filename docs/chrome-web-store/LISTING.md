# Chrome Web Store listing

Everything needed to submit the extension at <https://chrome.google.com/webstore/devconsole>.

**Package:** `outbreak-discord-extension-v<version>.zip` from the latest GitHub Release. It's the `extension/` folder zipped with `manifest.json` at the root.

## Store listing tab

**Name:** Outbreak Discord Rich Presence

**Summary (132 chars max):**
Show the Resident Evil Outbreak File #1/#2 stage you're playing on outbreakweb.com as your Discord status, with stage art.

**Category:** Entertainment (or Social & Communication)

**Language:** English

**Description:**

```
Show what you're playing in Resident Evil Outbreak (File #1 and File #2) on outbreakweb.com as your Discord status.

• Detects the stage automatically: Outbreak, Below Freezing Point, The Hive, Hellfire, Decisions Decisions, Wild Things, Underbelly, Flashback, Desperate Times and End of the Road
• Shows stage artwork, your character and your current room
• Adds a "Play Outbreak" button to your Discord status
• Keeps your status while the game tab is open, even when Chrome is in the background

REQUIRES the free companion app (Windows or Linux), which connects Chrome to the Discord desktop app:
https://github.com/adgsenpai/outbreak-discord/releases

Setup:
1. Install the companion. On Windows, double-click the .exe. On Linux, run the one-line installer.
2. Install this extension.
3. Play at outbreakweb.com with the Discord desktop app open.

Privacy: the extension only runs on outbreakweb.com/file1 and /file2 and sends data only to the companion on your own computer (127.0.0.1). There's no tracking or analytics.

Unofficial fan project. Not affiliated with Capcom, Discord or outbreakweb.com. Resident Evil Outbreak © CAPCOM.
```

**Graphics:**
- Store icon: `docs/chrome-web-store/icon-128.png`
- Screenshot: `docs/chrome-web-store/screenshot-1280x800.png`
- Small promo tile: `docs/chrome-web-store/promo-small-440x280.png`

**Homepage URL:** https://github.com/adgsenpai/outbreak-discord
**Support URL:** https://github.com/adgsenpai/outbreak-discord/issues

## Privacy practices tab

**Single purpose:**
Shows the Resident Evil Outbreak stage the user is playing on outbreakweb.com as their Discord Rich Presence status, using a local companion app.

**Permission justifications:**
- `storage`: saves the user's settings (on/off and the room-sharing opt-in).
- `alarms`: refreshes the Discord status about every 30 seconds while the game is open.
- Host permission `https://outbreakweb.com/file1/*`, `/file2/*`: reads the current stage, room and character from the game page.
- Host permission `http://127.0.0.1:8766/*`: sends that status to the companion app running on the user's own computer.

**Remote code:** No. All code ships in the package.

**Data usage:** Check **Website content** (the stage, room and character from the game page), used only for the extension's single purpose. Certify that data isn't sold, isn't used for unrelated purposes, and isn't used for creditworthiness.

**Privacy policy URL:** https://github.com/adgsenpai/outbreak-discord/blob/main/PRIVACY.md

## Notes

- Registering a Chrome Web Store developer account has a one-time US$5 fee. The account holder must pay it and submit.
- After the extension is published, it gets a permanent ID. Nothing in the companion needs changing, because it accepts any `chrome-extension://` origin.
- Expect review to take a few days. The name avoids "Resident Evil", and the description says it's an unofficial fan project, to reduce trademark flags.
