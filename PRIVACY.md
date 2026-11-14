# Privacy policy — Outbreak Discord Rich Presence

_Last updated: 2026-11-15_

Outbreak Discord Rich Presence is a Chrome extension plus a companion app that runs on your own computer. Together they show the Resident Evil Outbreak stage you're playing on outbreakweb.com as your Discord status.

## What the extension reads

The extension only runs on `https://outbreakweb.com/file1/*` and `https://outbreakweb.com/file2/*`. On those pages it reads:

- the game's current scenario number and your room number, through the site's own tracker
- the character name and room label shown in the site's tracker
- your online lobby room name and player count, only if you turn on "Show my room in Discord" (off by default)

It doesn't read any other site, your browsing history, passwords, cookies, form data or game saves.

## Where the data goes

The extension sends this data only to the companion app at `http://127.0.0.1:8766`, which runs on your own computer. The companion passes it to the Discord desktop app over Discord's local connection, and Discord shows it as your status. Nothing is sent to the developer or to any other server, and there's no analytics or tracking.

## What's stored

The extension stores its settings (enabled/disabled, room-sharing choice, optional token) in Chrome's local extension storage. The companion stores a config file in `~/.config/outbreak-discord/` on your computer. Neither stores any game or personal data.

## Contact

Open an issue at https://github.com/adgsenpai/outbreak-discord/issues.
