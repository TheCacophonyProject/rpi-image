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
wget -O - https://repo.saltstack.com/apt/debian/9/armhf/2018.3/SALTSTACK-GPG-KEY.pub | apt-key add -
echo "deb http://repo.saltstack.com/apt/debian/9/armhf/2018.3 stretch main" > /etc/apt/sources.list.d/saltstack.list
apt-get update
apt-get install -y salt-minion
systemctl stop salt-minion

# Install latest Cacophony Project Salt state config
cd /srv
wget https://github.com/TheCacophonyProject/saltops/archive/master.zip
unzip master.zip
mv saltops-master/* .
rm -rf saltops-master master.zip

# Update locally system using Salt
salt-call --local state.apply --state-output=mixed

# Stop services started by Salt
systemctl stop thermal-recorder
systemctl stop thermal-uploader

# General package updates
apt-get update
apt-get upgrade -y
apt-get autoremove -y

# Clean up
rm -rf /srv/*

# TODO: remove self

echo "System updated - shutting down"
/sbin/shutdown -h now
