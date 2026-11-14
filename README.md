# Real game artwork edition — important

This edition **removes the ten AI-generated stage images**. The two original PlayStation 2 covers supplied by the user are still included as `assets/outbreak_file1.png` and `assets/outbreak_file2.png`.

**Actual stage screenshots are NOT bundled.** The environment could locate galleries, but could not retrieve and verify ten source image files. Rather than misrepresent generated artwork as authentic screenshots, this package includes an importer for genuine screenshots you save from the game or authorized galleries.

## Where to find real screenshots

- Resident Evil Wiki gallery: https://residentevil.fandom.com/wiki/Resident_Evil_Outbreak/gallery
- Scenario reference pages: https://outbreakweb.org/scenarios/
- File 1 full playthrough: https://www.youtube.com/watch?v=Iu3c1j7cyKc
- File 2 full playthrough: https://www.youtube.com/watch?v=f8B5E7lYfxY

For the cleanest real artwork, capture each scenario's in-game title card or a representative scene directly from your browser gameplay. Only use material you're allowed to redistribute.

## Install actual stage screenshots

1. Save your ten genuine screenshots to `assets/real_stage_images/`, naming them:

   `outbreak`, `below_freezing_point`, `the_hive`, `hellfire`, `decisions_decisions`, `wild_things`, `underbelly`, `flashback`, `desperate_times`, `end_of_the_road`.

   Use `.png`, `.jpg`, `.jpeg` or `.webp` extensions.

   Alternatively, if you have the 3/3/3/1 title-card grid image (774×754 layout), split it automatically:

   ```bash
   python3 crop_stage_grid.py assets/real_stage_images/stage_grid.jpeg
   ```
2. Run:

```bash
python3 -m pip install -r requirements-artwork.txt
python3 import_real_stage_art.py
```

3. Upload the resulting `assets/*.png` to Discord Developer Portal under matching asset keys. Until you add the stage screenshots, stage artwork will not render; the real game covers remain available.

## Companion and Chrome extension

# Outbreak Discord Presence v6 — Linux + Chrome

Supports Resident Evil Outbreak File #1 and File #2 with **10 original AI-generated stage illustrations** (one per scenario), plus two authentic game cover images supplied by the user. The 10 stage illustrations are atmospheric interpretations, NOT official game screenshots.

## Stage artwork keys (upload all PNG files in assets/)

| Game | Scenario | Discord asset key |
|---|---|---|
| file1 | Outbreak | `outbreak` |
| file1 | Below Freezing Point | `below_freezing_point` |
| file1 | The Hive | `the_hive` |
| file1 | Hellfire | `hellfire` |
| file1 | Decisions, Decisions | `decisions_decisions` |
| file2 | Wild Things | `wild_things` |
| file2 | Underbelly | `underbelly` |
| file2 | Flashback | `flashback` |
| file2 | Desperate Times | `desperate_times` |
| file2 | End of the Road | `end_of_the_road` |
| File 1 | Default cover | `outbreak_file1` |
| File 2 | Default cover | `outbreak_file2` |

**Cover artwork update (v6):** `assets/outbreak_file1.png` and `assets/outbreak_file2.png` are converted directly from the two real PlayStation 2 cover images supplied by the user. They are no longer duplicates of the Outbreak / Wild Things stage illustrations. The other 10 images remain generated stage artwork.

**Important:** Discord cannot use local PNG paths as Rich Presence artwork. Upload all 12 PNGs manually to the **same Discord Developer application**, under Rich Presence / Art Assets. If your application has an asset limit, upload only the stages you want or use a separate application. The title at the top of Discord is the Discord application's name; the details identify File 1 vs File 2.

## Setup

1. Create a Discord application at https://discord.com/developers/applications and copy its numeric Application ID.
2. In `outbreak-discord/companion`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py --app-id YOUR_APPLICATION_ID
```

3. Copy the pairing token printed by the server. Keep the terminal running and Discord Desktop open.
4. In Chrome go to `chrome://extensions`, enable Developer mode, **Load unpacked**, choose `outbreak-discord/extension`.
5. Click the extension icon, paste the token, and Save. Enable room sharing only if desired.
6. Open https://outbreakweb.com/file1/ or https://outbreakweb.com/file2/ and keep the tab active. Turn on the website's Tracker panel display so it populates `#trk-panel`.

## How live stage detection works

The extension reads `#trk-panel .trk-card .trk-room` (current in-game room), character, difficulty and timer, and optionally `#rooms` for lobby status. The companion uses conservative room-name hints in `companion/stages.py`. **Not every room in every scenario is mapped**: the 10 artworks are ready, but unrecognized room names show a default File 1/2 image rather than falsely identifying a stage. `In front of Elephant Restaurant` is recognized as Wild Things. Extend `HINTS` with verified tracker location strings to improve coverage.

The first tracker card is displayed as the character; it may be a teammate, not your controlled character. The match timer shown in the site is not used as Discord's elapsed timer; Discord displays the session start time. Browser updates run about every 30 seconds, with a 75-second stale timeout.

## Troubleshooting

- If Discord activity is missing, check Discord's Activity Privacy settings, confirm Discord Desktop is running, and look at Python logs. Flatpak/Snap Discord may not expose the IPC socket to the companion.
- If images are missing, check that the Discord asset keys exactly match the PNG filename stems and wait for Discord asset propagation.
- If you changed versions, reload the unpacked Chrome extension and restart the Python companion.
- If the stage is unknown, add its distinctive tracker room name to `companion/stages.py`. Do not map numeric `Area 01` to a scenario: that number is not sufficient evidence.
- Keep the pairing token private. The server listens only on `127.0.0.1:8766`.
- `assets/discord_upload/` holds the exact 1024×1024 files uploaded to Discord (covers padded to square, since Discord requires at least 512×512).
- To run the companion at login, copy `companion/outbreak-discord.service` to `~/.config/systemd/user/`, replace the path placeholder, then `systemctl --user enable --now outbreak-discord`.

## Privacy

All data stays between the Outbreak tab and the local companion, except what you explicitly publish through Discord Rich Presence. The extension never reads game memory, transfer codes, or inventory icons. Room sharing is opt-in and disabled by default. The code is provided as-is, without live integration verification.
