#!/bin/bash

sudo cp ./vertex-update.sh /usr/local/bin/vertex-update
sudo chmod 755 /usr/local/bin/vertex-update

cd update-pamac
git pull
sh ./install.sh
