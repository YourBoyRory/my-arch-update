#!/bin/bash

sudo cp ./vertex-update.sh /usr/local/bin/vertex-update
sudo chmod 755 /usr/local/bin/vertex-update
sudo cp ./update_check.py /usr/local/bin/update-check
sudo chmod 755 /usr/local/bin/update-check

mkdir -p ~/.config/systemd/user
cp ./update-checker.service  ~/.config/systemd/user/update-checker.service
cp ./update-checker.timer ~/.config/systemd/user/update-checker.timer
systemctl --user daemon-reload
systemctl --user enable --now update-checker.service
systemctl --user enable --now update-checker.timer
systemctl --user list-timers update-checker.timer --no-pager

git submodule update --init
cd update-pamac
git pull
sh ./install.sh
