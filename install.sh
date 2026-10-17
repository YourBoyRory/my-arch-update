#!/bin/bash

sudo cp ./vertex-update.sh /usr/local/bin/vertex-update
sudo chmod 755 /usr/local/bin/vertex-update
sudo cp ./update_check.py /usr/local/bin/update-check
sudo chmod 755 /usr/local/bin/update-check

mkdir -p ~/.config/systemd/user
mkdir -p ~/.local/share/applications
cp ./update-checker.service  ~/.config/systemd/user/update-checker.service
cp ./update-checker.timer ~/.config/systemd/user/update-checker.timer
systemctl --user daemon-reload
systemctl --user enable --now update-checker.service
systemctl --user enable --now update-checker.timer
systemctl --user list-timers update-checker.timer --no-pager

echo '[Desktop Entry]
Type=Application
Name=Update Check
Comment=Vertex Check for updates
Exec=/usr/local/bin/update-check --show-all
Icon=system-software-update
Terminal=false
Categories=Utility;' > ~/.local/share/applications/my-app.desktop

git submodule update --init
cd update-pamac
git pull
sh ./install.sh
