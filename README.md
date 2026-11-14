# Outbreak Discord Rich Presence

Discord Rich Presence for **Resident Evil Outbreak File #1 and File #2** played in the browser at [outbreakweb.com](https://outbreakweb.com). A Chrome extension reads which stage you're in, and a small local companion sends it to your Discord desktop app, with stage artwork, your character and current room.

<p>
  <img src="docs/screenshots/decisions_decisions.png" alt="Discord status: Resident Evil Outbreak — Decisions, Decisions · Kevin, Waiting room" width="420">
  <img src="docs/screenshots/hellfire.png" alt="Discord status: Resident Evil Outbreak — Hellfire · Kevin, Apple Inn square" width="420">
</p>

When you're in the menus or between stages, it falls back to the game cover:

<img src="docs/screenshots/menu_fallback.png" alt="Discord status: Resident Evil Outbreak — Resident Evil Outbreak: File #1, Playing in Chrome" width="420">

## Features

- **Automatic stage detection** for all ten scenarios, read from the game's own scenario ID (no guessing from room names).
- **Stage artwork** for every scenario, plus File #1 / File #2 covers.
- Shows **character** and **current room**, and a "Play Outbreak File #N" button.
- Keeps your status while the game tab is open, even when Chrome isn't the focused window.
- Linux companion that can run as a **systemd user service** and start on login.
- Talks only to `127.0.0.1`, authenticated with a pairing token.

## How it works

```
outbreakweb.com tab ──► Chrome extension ──► local companion (127.0.0.1:8766) ──► Discord desktop (IPC)
   page-bridge.js         content.js /           companion/server.py
   (reads scen + room)    background.js          + stages.py (scen → stage)
```

1. `extension/page-bridge.js` runs in the page and calls the site's own read-only tracker reader (`trkRead()`) every 2 seconds. It gets the **scenario ID** and your **room**. This works whether or not the site's tracker panel is visible.
2. `extension/content.js` adds the character name and room label from the tracker cards. `extension/background.js` posts everything to the companion about every 30 seconds.
3. `companion/server.py` maps the scenario ID to a stage and updates your Discord presence through pypresence. If nothing arrives for 75 seconds, it clears the presence.

### Scenario IDs

The game's scenario ID is the stage's data-archive number on the disc (`rNNN.afs`). The table comes from the [Resident Evil Wiki scenario table](https://residentevil.fandom.com/wiki/Network_Biohazard). The ✓ rows were confirmed in-game.

| File | ID | Stage | Discord asset key |
|---|---|---|---|
| #1 | 1 | Outbreak | `outbreak_hd` |
| #1 | 2 | Hellfire ✓ | `hellfire_hd` |
| #1 | 28 | The Hive ✓ | `the_hive_hd` |
| #1 | 35 | Below Freezing Point | `below_freezing_point_hd` |
| #1 | 41 | Decisions, Decisions ✓ | `decisions_decisions_hd` |
| #2 | 10 | Underbelly | `underbelly_hd` |
| #2 | 15 | Desperate Times | `desperate_times_hd` |
| #2 | 26 | Flashback | `flashback_hd` |
| #2 | 40 | Wild Things ✓ | `wild_things_hd` |
| #2 | 6 | End of the Road ✓ | `end_of_the_road_hd` |
| #1 | not detected | File #1 cover | `outbreak_file1` |
| #2 | not detected | File #2 cover | `outbreak_file2` |

End of the Road (6) isn't in the wiki table; it was confirmed in-game. As a safety net, any other File #2 ID is also treated as End of the Road, since File #2 has only five scenarios. If a stage ever shows the wrong art, look for `scen=N` in the companion log and fix `SCENARIO_IDS` in `companion/stages.py`.

## Setup (Linux + Chrome)

### 1. Discord application

1. Create an application at <https://discord.com/developers/applications>. Its name is the title shown in Discord, e.g. "Resident Evil Outbreak". Copy the **Application ID**.
2. Under **Rich Presence → Art Assets**, upload every file in `assets/discord_upload_hd/` (stage art) and `outbreak_file1.png` / `outbreak_file2.png` from `assets/discord_upload/` (covers). Each filename (without extension) becomes the asset key. Upload a few files at a time; large batches can hang the portal.

### 2. Companion

```bash
cd companion
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python server.py --app-id YOUR_APPLICATION_ID
```

It prints a **pairing token**; the app ID and token are saved in `~/.config/outbreak-discord/config.json`. Keep Discord desktop running.

**Start on login (optional):**

```bash
mkdir -p ~/.config/systemd/user
sed "s#REPLACE_WITH_ABSOLUTE_PROJECT_PATH#$PWD/..#g" outbreak-discord.service > ~/.config/systemd/user/outbreak-discord.service
systemctl --user daemon-reload
systemctl --user enable --now outbreak-discord
```

View its log with `journalctl --user -u outbreak-discord -f`.

### 3. Chrome extension

1. Open `chrome://extensions`, enable **Developer mode**, click **Load unpacked**, and choose the `extension/` folder.
2. Click the extension icon, paste the pairing token, then click **Save & connect**. It should show 🟢 Connected.
3. Open <https://outbreakweb.com/file1/> or <https://outbreakweb.com/file2/> and play.

## Stage artwork

The ten stage images are cropped from a fan-made grid of the in-game scenario title cards.

- `crop_stage_grid.py` splits that 3/3/3/1 grid into `assets/real_stage_images/<stage>.png`.
- `import_real_stage_art.py` turns any screenshots in `assets/real_stage_images/` into 1024×1024 Discord art. Each image is scaled up to the full width and the empty space is filled with a blurred backdrop.

```bash
companion/.venv/bin/python crop_stage_grid.py assets/real_stage_images/stage_grid.jpeg
companion/.venv/bin/python import_real_stage_art.py
```

To use your own screenshots, save them as `assets/real_stage_images/<stage>.png` (or `.jpg`/`.webp`), using the stage keys from the table above without `_hd`. Then run the importer.

## Troubleshooting

- **No activity in Discord.** Check that Discord desktop is running, that **Settings → Activity Privacy → Share your activity** is on, and the companion log. Snap/Flatpak Discord is supported (the IPC socket under `$XDG_RUNTIME_DIR/snap.discord/` is found automatically).
- **Popup shows 🔴 Disconnected.** The companion isn't running or the token doesn't match. Run `systemctl --user status outbreak-discord` and re-paste the token.
- **Port 8766 is in use.** Change `PORT` in `companion/server.py` and the two `127.0.0.1:8766` URLs in `extension/background.js` and `extension/manifest.json`, then reload the extension.
- **Cover instead of stage art.** You're in a menu or lobby, or the scenario ID is unmapped. Check `scen=` in the log.
- **Art not updating after re-uploading.** Discord caches assets by key, so upload changed art under a new key rather than replacing an existing one.
- **After changing extension files.** Reload the extension at `chrome://extensions`, then reload the game tab.

## Privacy

- The extension only runs on `outbreakweb.com/file1` and `/file2`. It reads the scenario ID, room number, character name and room label through the site's own tracker, and sends them only to the companion on `127.0.0.1`.
- Showing your online lobby room name is opt-in in the popup and off by default.
- Only what appears in your Discord status leaves your machine.

## Credits

Resident Evil Outbreak and all game artwork © CAPCOM. This is an unofficial fan project; it isn't affiliated with Capcom, Discord or outbreakweb.com. Scenario IDs come from the [Resident Evil Wiki](https://residentevil.fandom.com/wiki/Network_Biohazard) (CC-BY-SA).
