#!/bin/bash
# Install or remove the Wed/Fri/Sun 04:00 Claude resample (launchd).
# Cancel: scripts/install_claude_resample_schedule.sh uninstall
set -euo pipefail
LABEL="se.makeitso.text-watermark-claude-resample"
REPO="/Users/jens/kod/text-watermark-tools"
SRC="$REPO/scripts/claude-resample.plist"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"
UID_N="$(id -u)"

uninstall() {
  launchctl bootout "gui/${UID_N}/${LABEL}" 2>/dev/null || true
  launchctl unload "$DST" 2>/dev/null || true
  rm -f "$DST"
  echo "unloaded $LABEL"
}

install() {
  mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
  cp "$SRC" "$DST"
  launchctl bootout "gui/${UID_N}/${LABEL}" 2>/dev/null || true
  if launchctl bootstrap "gui/${UID_N}" "$DST"; then
    echo "loaded $LABEL (Wednesday, Friday, Sunday at 04:00)"
  else
    launchctl load "$DST"
    echo "loaded $LABEL via launchctl load (Wednesday, Friday, Sunday at 04:00)"
  fi
  echo "cancel: $0 uninstall"
}

case "${1:-install}" in
  uninstall|remove|stop) uninstall ;;
  install|start) install ;;
  *) echo "usage: $0 [install|uninstall]" >&2; exit 2 ;;
esac
