#!/usr/bin/env bash
# Build the Linux version: dist/CheatDock/CheatDock plus dist/CheatDock-linux.tar.gz
# Run from the repo root on Linux:  ./build.sh
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
py=.venv/bin/python
"$py" -m pip install --quiet -r requirements.txt pyinstaller

rm -rf build dist/CheatDock
"$py" -m PyInstaller --noconfirm --onefile --windowed --name CheatDock \
  --add-data "assets/icon-*.png:assets" \
  --distpath dist/CheatDock run_cheatdock.pyw

cp config.yaml dist/CheatDock/
cp -r cheatsheets dist/CheatDock/
cp assets/icon-256.png dist/CheatDock/cheatdock.png
cp linux/install.sh dist/CheatDock/
chmod +x dist/CheatDock/CheatDock dist/CheatDock/install.sh

tar -czf dist/CheatDock-linux.tar.gz -C dist CheatDock
echo "Done: dist/CheatDock/CheatDock and dist/CheatDock-linux.tar.gz"
