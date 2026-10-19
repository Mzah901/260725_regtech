# ScreenStream

View-only screen mirror from a Mac to a browser on an Android tablet over the
local Wi-Fi, using WebRTC. Full screen on the tablet, low latency, no installs
on the tablet and no Python packages.

> Independent personal research. Not affiliated with or endorsed by any employer.

## How it works

```
 Mac                                               Android tablet
 ┌───────────────────────────┐                     ┌──────────────────────┐
 │ Chrome tab /sender        │ ── video (WebRTC, ──▶ Chrome  /?k=KEY     │
 │  captures the screen,     │    peer-to-peer     │  plays it full screen│
 │  encodes H.264            │    over Wi-Fi)      │  with ~0 buffering   │
 └────────────┬──────────────┘                     └──────────┬───────────┘
              │ tiny "how to reach me" messages (SDP)         │
              └────────────▶ server.py (port 8765) ◀──────────┘
```

`server.py` only relays the connection setup. The video goes straight from
the Mac's browser to the tablet's browser.

## Use it

1. On the Mac, build the app once:
   ```bash
   cd tools/screen-stream
   ./build_app.sh
   ```
   (Or skip the app and just run `python3 server.py`, then open
   http://127.0.0.1:8765/sender.)
2. Double-click **ScreenStream.app**. It opens the sharing page in Chrome.
3. On the tablet, open the address shown on that page (looks like
   `http://192.168.1.23:8765/?k=…`) in Chrome and bookmark it.
4. On the Mac, click **Start sharing** and pick a screen or window.
5. Tap the tablet screen once for full screen. Double-tap to show stats.

**First run on macOS** you will get two prompts. Allow both:
- *Screen Recording* for Chrome (System Settings → Privacy & Security →
  Screen Recording). Chrome must be restarted after you enable it.
- *Firewall: allow python3 incoming connections*, so the tablet can reach the
  server.

To stop: click **Quit ScreenStream** on the sharing page.

## Settings

| Setting | Options | When to use |
|---|---|---|
| Mode | Sharp text / Smooth motion | Text: documents, code (30 fps, keeps resolution). Motion: video, fast scrolling (60 fps, drops resolution first). |
| Max width | 1280 / 1920 / 2560 / Native | Lower = less latency. Retina Macs capture ~3000 px wide; 1920 is a good default. |

## What makes it low-latency

- **Peer-to-peer on the LAN**: no server in the video path, no STUN/TURN.
- **H.264 preferred**: hardware-decoded on nearly every Android tablet.
- **Jitter buffer target 0** on the tablet: frames are shown as soon as they
  arrive instead of being held "just in case".
- **Fast start**: Chrome is told to start at 4 Mbps instead of ramping up
  slowly from a blurry low bitrate.
- **Down-scaling** retina captures before encoding.

## Tested

Automated end-to-end test in headless Chromium on Linux (fake screen source):
video arrives, jitter buffer ~2 ms, network RTT ~1 ms, wrong access key gets
403, stop → viewer notices → restart → viewer reconnects automatically, Quit
stops the server.

**Not yet tested on a real Mac + Android tablet.** The headless browser has no
H.264, so it fell back to VP8; real Chrome on Mac/Android has H.264. Glass-to-
glass latency on real hardware (target: under ~150 ms on a decent 5 GHz Wi-Fi)
still needs measuring: show a stopwatch on the Mac, photograph both screens
together, subtract.

## Limitations (honest)

- **It's a "browser app", not a native Swift app.** The `.app` is a launcher
  that starts the server and opens Chrome; capture happens in the browser.
  This avoids Xcode and Google's WebRTC framework, at the cost of needing the
  Chrome tab to stay open.
- **Plain http on the LAN.** The video itself is encrypted (WebRTC always
  uses DTLS-SRTP), but the setup page is plain http. Anyone on the same Wi-Fi
  who learns the key could watch. Don't use it on public/shared Wi-Fi. Delete
  `~/.screenstream-token` to get a new key.
- **Tablet screen may sleep.** The Wake Lock API needs https. Either raise the
  tablet's screen timeout, or in tablet Chrome open
  `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, add
  `http://<mac-ip>:8765`, and relaunch.
- **No audio** (view only, by design).
- If the Mac's IP changes (new DHCP lease), the bookmark changes too. Give the
  Mac a fixed IP in your router to avoid this.
- 2.4 GHz or busy Wi-Fi adds latency and stutter; 5 GHz is much better.

## Files

| File | What it is |
|---|---|
| `server.py` | Signaling server, Python standard library only |
| `static/sender.html` | Mac page: captures and sends |
| `static/viewer.html` | Tablet page: receives and shows full screen |
| `static/denied.html` | Shown when the access key is missing or wrong |
| `build_app.sh` | Builds `ScreenStream.app` |
