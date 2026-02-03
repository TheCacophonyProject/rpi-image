#!/bin/bash

sdcard=$1
echo $sdcard

hostname="ir-camera-setting-up"

#check that the directory is correct

# Remove salt minion_id
sudo rm $sdcard/etc/salt/minion_id

# Remove salt pki folder
sudo rm -rf $sdcard/etc/salt/pki

# Remove Device Config
sudo cp config.toml $sdcard/etc/cacophony/config.toml

# Remove recordings
sudo rm -r $sdcard/var/spool/cptv/*

# Remove logs
sudo rm -rf $sdcard/var/log/*

# Remove bash history
cat /dev/null > $sdcard/home/pi/.bash_history && history -c

# Change hostname
echo "$hostname" | sudo tee $sdcard/etc/hostname > /dev/null
sudo sed -i "/^127\.0\.1\.1/ s/.*/127.0.1.1 \t$hostname/" $sdcard/etc/hosts

# Change wifi details
sudo cp wpa_supplicant.conf $sdcard/etc/wpa_supplicant/wpa_supplicant.conf
