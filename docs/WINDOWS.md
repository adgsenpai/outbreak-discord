# Windows setup guide

When you're done, your Discord profile shows **Playing Resident Evil Outbreak**, with the stage you're in, its artwork, your character and your room. Your friends see it in the member list and on your profile.

It takes about 5 minutes. You need three things:

1. **The Discord desktop app** (not Discord in a browser tab)
2. **The companion app** (`OutbreakDiscordCompanion.exe`)
3. **The Chrome extension** (`outbreak-discord-extension-v….zip`)

---

## Step 1: Install the Discord desktop app

The status only works with the **installed Discord app**. Discord opened in a browser tab (discord.com/app) can't show it.

- If Discord is already installed on your PC (it's in your Start menu or system tray), skip to Step 2.
- Otherwise go to <https://discord.com/download> and click **Download for Windows**. Don't click "Open Discord in your browser". Run the downloaded `DiscordSetup.exe` and sign in.

Then turn on activity sharing in Discord:

1. Click the ⚙️ **User Settings** gear, next to your name at the bottom left.
2. Go to **Activity Privacy**.
3. Turn on **Share your detected activities with others**.

## Step 2: Download the files

Open the **[latest release page](https://github.com/adgsenpai/outbreak-discord/releases/latest)** and scroll down to **Assets**. You only need two of the files:

| File | Do you need it? |
|---|---|
| **`OutbreakDiscordCompanion.exe`** | ✅ **Yes.** This is the Windows companion app. |
| **`outbreak-discord-extension-v….zip`** | ✅ **Yes.** This is the Chrome extension. |
| `outbreak-discord-companion-linux-x86_64` | ❌ No, this is for Linux. |
| `install-linux.sh` | ❌ No, this is for Linux. |
| `SHA256SUMS.txt` | ❌ No. It holds checksums for checking the downloads. |
| `Source code (zip)` / `Source code (tar.gz)` | ❌ No, this is the source code for developers. |

## Step 3: Install the companion app

1. Double-click **`OutbreakDiscordCompanion.exe`** in your Downloads folder.
2. Windows may show a blue **"Windows protected your PC"** box. It appears because the app isn't code-signed, which costs money for a free hobby project. Click **More info**, then **Run anyway**.
3. A box says **"Installed!"**. Click OK.

That's it. The companion now runs quietly in the background. It has no window and no tray icon, and it starts by itself every time you turn on your PC, so you only do this once.

> If Chrome or your antivirus deletes the `.exe` during download, choose **Keep** in the Chrome downloads list (Ctrl+J), or allow it in your antivirus. The source is public in this repo.

## Step 4: Install the Chrome extension

This extension isn't on the Chrome Web Store yet, so you load it yourself. It's a one-time setup.

1. **Unzip it.** Right-click `outbreak-discord-extension-v….zip`, choose **Extract All…**, then **Extract**. You get a folder with files like `manifest.json` inside.
   Move that folder somewhere it can stay, such as `Documents\outbreak-discord-extension`. Chrome loads the extension from this folder, so **don't delete it** afterwards.
2. In Chrome, type `chrome://extensions` in the address bar and press Enter.
3. Turn on **Developer mode** with the switch in the **top-right** corner.
4. Click **Load unpacked** at the top left.
5. Select the folder you unzipped: the one that has `manifest.json` directly inside it. Click **Select Folder**.
6. **Outbreak Discord Rich Presence** now appears in the list. To pin it, click the 🧩 puzzle icon in Chrome's toolbar and click the 📌 pin next to it.

> If Chrome says **"Manifest file is missing or unreadable"**, you picked the wrong folder level. Open the folder and select the one that contains `manifest.json`.

The extension also works in Edge, Brave and Opera. Use `edge://extensions` or `brave://extensions` instead.

## Step 5: Check it's connected

Click the extension's icon in the toolbar. The popup shows:

- 🟢 **Connected**: everything works. Make sure **Enable activity tracking** is ticked.
- 🔴 **Companion not running**: see [Troubleshooting](#troubleshooting) below.

## Step 6: Play

1. Make sure Discord desktop is open. It can be minimised to the tray.
2. In Chrome, go to <https://outbreakweb.com/file1/> or <https://outbreakweb.com/file2/>.
3. Start a game. Within about 30 seconds, your Discord status shows the game.

What people see:

- **In menus or the lobby:** the File #1 / File #2 cover.
- **In a stage:** the stage name, its artwork, your character and current room, and a **Play Outbreak** button.

Keep the game tab open. Your status stays even when Chrome is in the background, and it clears about a minute after you close the tab.

---

## Troubleshooting

**The popup says 🔴 Companion not running.**
Double-click `OutbreakDiscordCompanion.exe` again; it reinstalls and starts. If you deleted the download, it's also installed at `%LOCALAPPDATA%\OutbreakDiscord\OutbreakDiscordCompanion.exe`. Paste that into the Windows Run box (Win+R) to start it.

**The popup is 🟢, but nothing shows in Discord.**
- Check that you use the Discord **desktop app**, not Discord in a browser.
- Check that **User Settings → Activity Privacy → Share your detected activities** is on.
- Fully quit Discord (right-click its tray icon → **Quit Discord**) and open it again. Then wait 30 seconds.
- Don't run Discord "as administrator" unless the companion runs that way too. Windows won't let them talk to each other otherwise.

**Your friends can't see it, but you can.**
Discord only shows activity to people who share a server with you or are your friends, and your status must not be **Invisible**.

**It shows the cover, not the stage art.**
That's normal in menus, the lobby and loading screens. The stage art appears once the stage starts.

**I want to check the logs.**
Open `%USERPROFILE%\.config\outbreak-discord\companion.log` (paste it into Win+R). Lines like `Presence active: … | scen=28 …` mean it's working.

**I updated the extension.**
Replace the files in your extension folder with the new ones. Then click the ↻ reload icon on its card at `chrome://extensions` and reload the game tab.

## Uninstall

1. Press **Win+R**, paste the line below, and press Enter:
   ```
   %LOCALAPPDATA%\OutbreakDiscord\OutbreakDiscordCompanion.exe --uninstall
   ```
   This stops the companion, removes it from startup and deletes it.
2. At `chrome://extensions`, click **Remove** on the extension, then delete its folder.

## Is it safe?

- The companion only listens on your own computer (`127.0.0.1`), and it only accepts requests from the Chrome extension.
- The extension only runs on `outbreakweb.com/file1` and `/file2`. It reads the stage, room and character, and sends them only to the companion, which passes them to Discord.
- There's no tracking or analytics, and no account or Discord token is needed. All the code is in this repository. See [PRIVACY.md](../PRIVACY.md).
