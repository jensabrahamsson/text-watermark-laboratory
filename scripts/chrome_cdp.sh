#!/bin/zsh
# Start (or reuse) your ordinary Google Chrome with CDP on :9222.
# Chrome already running *without* the debug port will ignore the flag — quit it first.

set -euo pipefail
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT=9222

if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null; then
  echo "Chrome CDP already up on :${PORT}"
  curl -s "http://127.0.0.1:${PORT}/json/version"
  exit 0
fi

if pgrep -qx "Google Chrome"; then
  echo "Chrome is already running without the debug port."
  echo "Quit Chrome fully (Cmd+Q) and run this script again."
  exit 1
fi

echo "Starting Chrome with --remote-debugging-port=${PORT} (your usual profile)..."
exec "$CHROME" --remote-debugging-port="${PORT}" --remote-debugging-address=127.0.0.1
