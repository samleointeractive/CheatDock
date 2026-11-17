#!/usr/bin/env bash
# Adds CheatDock to your app menu (and optionally starts it at login).
# Run it from the unpacked CheatDock folder:  ./install.sh
# Nothing is copied: CheatDock keeps running from this folder, so move the
# folder first if you want it somewhere else, then run this again.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
apps="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
autostart="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
mkdir -p "$apps"

desktop_entry() {
  cat <<EOF
[Desktop Entry]
Type=Application
Name=CheatDock
Comment=Cheat sheets docked to the edge of your screen
Exec="$here/CheatDock"
Icon=$here/cheatdock.png
Terminal=false
Categories=Development;Utility;
StartupWMClass=CheatDock
EOF
}

desktop_entry > "$apps/cheatdock.desktop"
echo "Added CheatDock to the app menu ($apps/cheatdock.desktop)"

read -r -p "Start CheatDock when you log in? [y/N] " answer
if [[ "${answer,,}" == y* ]]; then
  mkdir -p "$autostart"
  desktop_entry > "$autostart/cheatdock.desktop"
  echo "CheatDock will start at login ($autostart/cheatdock.desktop)"
fi

cat <<EOF

Keyboard shortcut: Linux has no standard way for an app to grab a global
hotkey, so add one in your desktop settings that runs:

  "$here/CheatDock" --toggle

GNOME: Settings > Keyboard > View and Customize Shortcuts > Custom Shortcuts
KDE:   System Settings > Shortcuts > Add New > Command or Script
EOF
