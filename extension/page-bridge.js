// Runs in the page's own JS world (manifest "world": "MAIN") so it can see the
// site's tracker state, and forwards a few numbers to content.js.
// The site only refreshes window.trkLastState while its tracker panel/overlay is
// visible, so we call the site's own read-only trkRead() directly when possible.
(() => {
  const SOURCE = 'outbreak-discord-bridge';
  const read = () => {
    try {
      // trkRead / TRK_GAMES / game are top-level bindings of the site's script.
      // eslint-disable-next-line no-undef
      if (typeof trkRead === 'function' && typeof TRK_GAMES === 'object' && typeof game === 'object' && window.Module?.running) {
        // eslint-disable-next-line no-undef
        const cfg = TRK_GAMES[game && game.serial];
        // eslint-disable-next-line no-undef
        if (cfg) return trkRead(cfg);
      }
    } catch (_) { /* fall back below */ }
    return window.trkLastState;
  };
  setInterval(() => {
    const s = read();
    if (!s || s.state !== 'game') {
      window.postMessage({source: SOURCE, state: s ? String(s.state) : 'none'}, location.origin);
      return;
    }
    const players = Array.isArray(s.players) ? s.players : [];
    const me = players.find(p => p && p.slot === s.me) || players.find(p => p && p.inGame) || players[0];
    window.postMessage({
      source: SOURCE,
      state: 'game',
      file: Number(s.file) || null,
      scen: Number.isFinite(s.scen) ? s.scen : null,
      diff: Number.isFinite(s.diff) ? s.diff : null,
      room: me && Number.isFinite(me.room) ? me.room : null,
    }, location.origin);
  }, 2000);
})();
