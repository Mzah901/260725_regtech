# 2026-10-19 — ScreenStream (Mac → Android tablet screen mirror)

**Date:** 2026-10-19

**Question / hypothesis:** Can a simple, dependency-free tool mirror the Mac
screen to an Android tablet browser over local Wi-Fi with low latency using
WebRTC? Side tool, not regulation research: it does not advance the lab's
domain goals directly; its value is learning (networking, WebRTC, HTTP).

**Sources used:** None (no regulation data). Technical references: the W3C
WebRTC and Screen Capture specs (https://www.w3.org/TR/webrtc/,
https://www.w3.org/TR/screen-capture/).

**Tools and models used:** Python 3 standard library (`http.server`), browser
WebRTC APIs, Playwright + headless Chromium for the automated test. Built with
Claude Code.

**Result:**
- Headless end-to-end test passed: video received (1280×720 fake source),
  jitter buffer ~2 ms, RTT ~1 ms, 0 packets lost, wrong key → 403,
  automatic reconnect after stop/start, Quit stops the server.
- Not yet tested on real hardware. Glass-to-glass latency on a real Mac +
  Android tablet still to be measured.
- Known limits listed in `tools/screen-stream/README.md`.

**What the owner reviewed and approved:** _Pending owner review and a test on
real hardware._
