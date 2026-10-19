#!/bin/bash
# Builds ScreenStream.app: a double-clickable Mac app that starts the server
# and opens the sharing page in your browser.
#
#   cd tools/screen-stream && ./build_app.sh
#   then drag ScreenStream.app into /Applications (optional)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$HERE/ScreenStream.app"

rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$HERE/server.py" "$APP/Contents/Resources/"
cp -R "$HERE/static" "$APP/Contents/Resources/"

# Info.plist: the app's ID card that macOS reads.
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>ScreenStream</string>
  <key>CFBundleDisplayName</key><string>ScreenStream</string>
  <key>CFBundleIdentifier</key><string>local.screenstream</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>ScreenStream</string>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
</dict>
</plist>
PLIST

# The program macOS runs when you double-click the app.
cat > "$APP/Contents/MacOS/ScreenStream" <<'LAUNCHER'
#!/bin/bash
RES="$(cd "$(dirname "$0")/../Resources" && pwd)"
PORT="${SCREENSTREAM_PORT:-8765}"
URL="http://127.0.0.1:$PORT/sender"
LOG="$HOME/Library/Logs/ScreenStream.log"

# Apps opened from Finder get a minimal PATH, so look for Python explicitly.
PY=""
for p in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
  if [ -x "$p" ]; then PY="$p"; break; fi
done
if [ -z "$PY" ]; then
  osascript -e 'display alert "ScreenStream needs Python 3" message "Install it with: xcode-select --install"'
  exit 1
fi

# Start the server only if it isn't already running.
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/healthz"; then
  nohup "$PY" "$RES/server.py" >"$LOG" 2>&1 &
  disown
  for _ in $(seq 1 40); do
    curl -s -o /dev/null "http://127.0.0.1:$PORT/healthz" && break
    sleep 0.25
  done
fi

# Chrome gives the best WebRTC tuning; fall back to the default browser.
open -a "Google Chrome" "$URL" 2>/dev/null || open "$URL"
LAUNCHER
chmod +x "$APP/Contents/MacOS/ScreenStream"

echo "Built $APP"
