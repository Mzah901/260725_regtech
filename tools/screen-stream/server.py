#!/usr/bin/env python3
"""ScreenStream: a tiny signaling server for Mac -> tablet screen viewing over WebRTC.

The video itself never passes through this server. The browsers send it to each
other directly (peer-to-peer) over the local Wi-Fi. This server only passes the
short "how to reach me" messages (SDP offer/answer) between the two browsers.

Pure Python standard library: no pip install needed. Works on Python 3.9+.

    python3 server.py            # then open http://127.0.0.1:8765/sender on the Mac
"""
import json
import os
import secrets
import socket
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("SCREENSTREAM_PORT", "8765"))
STATIC_DIR = Path(__file__).resolve().parent / "static"
TOKEN_FILE = Path.home() / ".screenstream-token"
LONG_POLL_SECONDS = 25  # how long a request waits for news before returning "nothing yet"
VIEWER_STALE_SECONDS = 30  # a viewer we haven't heard from for this long is gone


def load_or_create_token():
    """A secret key in the viewer URL, so random devices on the Wi-Fi can't watch.

    Saved to a file so the tablet's bookmark keeps working after a restart.
    """
    try:
        token = TOKEN_FILE.read_text().strip()
        if token:
            return token
    except OSError:
        pass
    token = secrets.token_urlsafe(8)
    try:
        TOKEN_FILE.write_text(token)
        TOKEN_FILE.chmod(0o600)
    except OSError:
        pass
    return token


def lan_ip():
    """Find this Mac's address on the local network (e.g. 192.168.1.23).

    Connecting a UDP socket sends no packets; it just asks the OS which
    network interface it would use, which tells us our own LAN address.
    """
    for probe in ("8.8.8.8", "10.255.255.255"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect((probe, 1))
                return s.getsockname()[0]
        except OSError:
            continue
    return "127.0.0.1"


class Hub:
    """Shared mailbox between the sender (Mac) page and the viewer (tablet) pages.

    A Condition lets a waiting request sleep until another request posts news,
    which is how "long polling" works without any extra libraries.
    """

    def __init__(self):
        self.cond = threading.Condition()
        self.pending = []  # viewer ids waiting for the Mac to call them
        self.last_seen = {}  # viewer id -> time we last heard from it
        self.offers = {}  # viewer id -> offer from the Mac
        self.answers = {}  # viewer id -> answer from the viewer

    def wait_for(self, predicate):
        with self.cond:
            self.cond.wait_for(predicate, timeout=LONG_POLL_SECONDS)
            return predicate()

    def viewer_join(self):
        viewer_id = secrets.token_hex(6)
        with self.cond:
            self.pending.append(viewer_id)
            self.last_seen[viewer_id] = time.time()
            self.cond.notify_all()
        return viewer_id

    def sender_next(self):
        """Return the viewers that want a stream (waits until there is at least one)."""
        def alive():
            now = time.time()
            return [v for v in self.pending if now - self.last_seen.get(v, 0) < VIEWER_STALE_SECONDS]

        with self.cond:
            self.cond.wait_for(lambda: alive(), timeout=LONG_POLL_SECONDS)
            ready = alive()
            self.pending = []
            return ready

    def put(self, box, viewer_id, sdp):
        with self.cond:
            box[viewer_id] = sdp
            self.cond.notify_all()

    def take(self, box, viewer_id):
        with self.cond:
            self.last_seen[viewer_id] = time.time()
            self.cond.wait_for(lambda: viewer_id in box, timeout=LONG_POLL_SECONDS)
            return box.pop(viewer_id, None)


HUB = Hub()
TOKEN = load_or_create_token()


class Handler(BaseHTTPRequestHandler):
    server_version = "ScreenStream/1.0"

    # ---- small helpers -------------------------------------------------
    def log_message(self, fmt, *args):  # keep the log quiet: long polls are noisy
        if os.environ.get("SCREENSTREAM_DEBUG"):
            super().log_message(fmt, *args)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_empty(self, status):
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_file(self, name):
        body = (STATIC_DIR / name).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def is_local(self):
        # Only the Mac itself may use the sender side.
        return self.client_address[0] in ("127.0.0.1", "::1")

    def parse(self):
        url = urllib.parse.urlparse(self.path)
        query = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
        return url.path, query

    def token_ok(self, query):
        return secrets.compare_digest(query.get("k", ""), TOKEN)

    def viewer_url(self):
        return "http://%s:%d/?k=%s" % (lan_ip(), PORT, TOKEN)

    # ---- routes --------------------------------------------------------
    def do_GET(self):
        path, q = self.parse()

        if path == "/healthz":
            return self.send_json({"ok": True})

        if path == "/":
            if not self.token_ok(q):
                return self.send_file("denied.html")
            return self.send_file("viewer.html")

        if path == "/api/viewer/offer":
            if not self.token_ok(q):
                return self.send_empty(403)
            offer = HUB.take(HUB.offers, q.get("id", ""))
            return self.send_json(offer) if offer else self.send_empty(204)

        # Everything below is for the Mac only.
        if not self.is_local():
            return self.send_empty(403)

        if path == "/sender":
            return self.send_file("sender.html")
        if path == "/api/sender/config":
            return self.send_json({"lanIp": lan_ip(), "viewerUrl": self.viewer_url()})
        if path == "/api/sender/next":
            return self.send_json({"ids": HUB.sender_next()})
        if path == "/api/sender/answer":
            answer = HUB.take(HUB.answers, q.get("id", ""))
            return self.send_json(answer) if answer else self.send_empty(204)

        return self.send_empty(404)

    def do_POST(self):
        path, q = self.parse()

        if path == "/api/viewer/join":
            if not self.token_ok(q):
                return self.send_empty(403)
            return self.send_json({"id": HUB.viewer_join()})
        if path == "/api/viewer/answer":
            if not self.token_ok(q):
                return self.send_empty(403)
            data = self.read_json()
            HUB.put(HUB.answers, data["id"], data["description"])
            return self.send_json({"ok": True})

        if not self.is_local():
            return self.send_empty(403)

        if path == "/api/sender/offer":
            data = self.read_json()
            HUB.put(HUB.offers, data["id"], data["description"])
            return self.send_json({"ok": True})
        if path == "/api/sender/quit":
            self.send_json({"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return None

        return self.send_empty(404)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    print("ScreenStream running.")
    print("  On this Mac open:     http://127.0.0.1:%d/sender" % PORT)
    print("  On the tablet open:   http://%s:%d/?k=%s" % (lan_ip(), PORT, TOKEN))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("ScreenStream stopped.")


if __name__ == "__main__":
    main()
