#!/usr/bin/env python3
"""Loopback-only Chrome -> Discord desktop Rich Presence bridge."""
import argparse
import json
import os
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from pypresence import Presence
from stages import identify, STAGES

PORT = 8766
TIMEOUT = 75
GAME_URLS = {'file1': 'https://outbreakweb.com/file1/', 'file2': 'https://outbreakweb.com/file2/'}
CONFIG = Path.home() / '.config' / 'outbreak-discord' / 'config.json'

class State:
    def __init__(self, app_id, token, image):
        self.app_id, self.token, self.image = app_id, token, image
        self.lock = threading.Lock()
        self.playing = False
        self.game = None
        self.room = None
        self.tracker = None
        self.updated = 0.0
        self.started = None
        self.rpc = None
        self.last_sent = None

    def update(self, playing, game=None, room=None, tracker=None):
        with self.lock:
            now = time.time()
            if playing and not self.playing:
                self.started = int(now)
            self.playing = playing
            self.game = game if playing else None
            self.room = room if playing else None
            self.tracker = tracker if playing else None
            self.updated = now

    def run(self):
        while True:
            try:
                with self.lock:
                    active = self.playing and (time.time() - self.updated < TIMEOUT)
                    if not active and self.playing:
                        self.playing = False
                    started = self.started
                    game = self.game
                    room = self.room
                    tracker = self.tracker
                if not self.rpc:
                    if active:
                        self.rpc = Presence(self.app_id)
                        self.rpc.connect()
                        print('Connected to Discord desktop RPC', flush=True)
                        self.last_sent = None
                if self.rpc:
                    desired = (active, started if active else None, game, json.dumps(room, sort_keys=True), json.dumps(tracker, sort_keys=True))
                    if desired != self.last_sent:
                        if active:
                            which = 'File #1' if game == 'file1' else 'File #2'
                            title = f'Resident Evil Outbreak: {which}'
                            chars = (tracker or {}).get('characters') or []
                            location = chars[0].get('location','') if chars else ''
                            character = chars[0].get('name','') if chars else ''
                            # Confirmed mapping: File 2's Elephant Restaurant belongs to Wild Things.
                            stage_key = identify(game, location)
                            stage = STAGES.get(game, {}).get(stage_key)
                            details = f'{stage} · {character}' if stage and character else (f'Playing as {character}' if character else title)
                            state_text = location or 'Playing in Chrome'
                            if room and not location:
                                details = f'{which} · {room.get("name", "Room")}'
                                state_text = f'{room.get("status", "In room")} · {room.get("players", "?")} players'
                            payload = dict(details=details[:128], state=state_text[:128],start=started,
                                buttons=[{'label':f'Play Outbreak {which}','url':GAME_URLS.get(game,GAME_URLS['file2'])}])
                            image_key = stage_key if stage_key else ('outbreak_file1' if game=='file1' else 'outbreak_file2')
                            payload['large_image'] = image_key
                            payload['large_text'] = (stage or title)[:128]
                            if tracker and tracker.get('difficulty'):
                                payload['state'] = (state_text + ' · ' + str(tracker['difficulty']))[:128]
                            # Optional override for users with a custom cover asset.
                            if self.image and not stage: payload['large_image'] = self.image
                            self.rpc.update(**payload)
                            print(f"Presence active: {title} | {stage or location or 'unknown stage'}", flush=True)
                        else:
                            self.rpc.clear()
                            print('Presence cleared', flush=True)
                        self.last_sent = desired
            except Exception as exc:
                print(f'Discord unavailable: {exc}; retrying...', flush=True)
                if self.rpc:
                    try: self.rpc.close()
                    except Exception: pass
                self.rpc = None
                self.last_sent = None
            time.sleep(3)

def make_handler(state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass
        def do_GET(self):
            if self.path != '/health':
                self.send_error(404); return
            self.send_json(200, {'ok': True, 'service': 'outbreak-discord'})
        def do_POST(self):
            if self.path != '/status':
                self.send_error(404); return
            supplied = self.headers.get('X-Outbreak-Token', '')
            if not secrets.compare_digest(supplied, state.token):
                self.send_json(403, {'error':'Invalid pairing token'}); return
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 8192:
                self.send_json(400, {'error':'Invalid body length'}); return
            try:
                body = json.loads(self.rfile.read(length))
                if type(body.get('playing')) is not bool:
                    raise ValueError('playing must be a boolean')
                game = body.get('game')
                if game not in (None, 'file1', 'file2'):
                    raise ValueError('invalid game')
                room = body.get('room')
                tracker = body.get('tracker')
                if tracker is not None:
                    if not isinstance(tracker, dict): raise ValueError("invalid tracker")
                    chars = tracker.get("characters", [])
                    if not isinstance(chars, list): raise ValueError("invalid characters")
                    tracker = {"characters": [{k: str(c.get(k,""))[:100] for k in ("name","location","health","virus")} for c in chars[:4] if isinstance(c,dict)],"difficulty":str(tracker.get("difficulty",""))[:24],"matchTime":str(tracker.get("matchTime",""))[:30]}
                if room is not None:
                    if not isinstance(room, dict):
                        raise ValueError('invalid room')
                    allowed = ('name','status','area','players','visibility')
                    room = {k: str(room[k])[:80] for k in allowed if isinstance(room.get(k), str)}
                if not body['playing']:
                    game, room, tracker = None, None, None
            except (ValueError, json.JSONDecodeError, AttributeError):
                self.send_json(400, {'error':'Expected JSON {"playing": boolean}'}); return
            state.update(body['playing'], game, room, tracker)
            self.send_json(200, {'ok':True, 'playing':body['playing']})
        def send_json(self, status, data):
            payload = json.dumps(data).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
    return Handler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', help='Discord Developer Portal Application ID')
    parser.add_argument('--image', default=None, help='Optional Discord Rich Presence asset key, e.g. outbreak_cover')
    args = parser.parse_args()
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text())
    else:
        cfg = {'token': secrets.token_urlsafe(32)}
    if args.app_id: cfg['app_id'] = args.app_id
    if args.image is not None: cfg['image'] = args.image
    app_id = str(cfg.get('app_id', ''))
    if not app_id.isdigit() or len(app_id) < 15:
        parser.error('Provide --app-id YOUR_DISCORD_APPLICATION_ID on first run')
    CONFIG.write_text(json.dumps(cfg, indent=2) + '\n')
    os.chmod(CONFIG, 0o600)
    state = State(app_id, cfg['token'], cfg.get('image'))
    threading.Thread(target=state.run, daemon=True).start()
    print(f'Listening on http://127.0.0.1:{PORT}', flush=True)
    print(f'Pairing token (keep private): {cfg["token"]}', flush=True)
    print('Keep this process running. Ctrl+C to stop.', flush=True)
    server = ThreadingHTTPServer(('127.0.0.1', PORT), make_handler(state))
    try: server.serve_forever()
    except KeyboardInterrupt: print('\nStopping...')
    finally:
        server.server_close()
        if state.rpc:
            try: state.rpc.clear(); state.rpc.close()
            except Exception: pass

if __name__ == '__main__': main()
