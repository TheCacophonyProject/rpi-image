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


mkdir /etc/apt/keyrings
sudo curl -fsSL -o /etc/apt/keyrings/salt-archive-keyring.gpg https://repo.saltproject.io/py3/debian/11/armhf/3005/salt-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring.gpg arch=armhf] https://repo.saltproject.io/py3/debian/11/armhf/3005 bullseye main" | sudo tee /etc/apt/sources.list.d/salt.list

apt-get update
apt-get install -y salt-minion
systemctl stop salt-minion
systemctl disable salt-minion


# Install Salt minion software
wget -O - https://repo.saltstack.com/apt/debian/9/armhf/2018.3/SALTSTACK-GPG-KEY.pub | apt-key add -
echo "deb http://repo.saltstack.com/apt/debian/9/armhf/2018.3 stretch main" > /etc/apt/sources.list.d/saltstack.list
apt-get update
apt-get install -y salt-minion
systemctl stop salt-minion
rm /etc/salt/minion_id