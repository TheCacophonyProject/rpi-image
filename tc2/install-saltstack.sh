#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "Please run as root."
    exit 1
fi

# Wait for internet connection to come up
echo "waiting for internet connection..."
for attempt in `seq 10`; do
    ping -q -w 5 -c 1 1.1.1.1 > /dev/null && break
    sleep 1
done
echo "internet connection available"

set -e -x

# Install Salt minion software
# https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/raspbian.html#install-classic-packages-of-salt-on-raspbian-11-bullseye


mkdir /etc/apt/keyrings
sudo curl -fsSL -o /etc/apt/keyrings/salt-archive-keyring.gpg https://repo.saltproject.io/py3/debian/11/armhf/3005/salt-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring.gpg arch=armhf] https://repo.saltproject.io/py3/debian/11/armhf/3005 bullseye main" | sudo tee /etc/apt/sources.list.d/salt.list
apt-get update
apt-get install -y salt-minion
systemctl stop salt-minion
