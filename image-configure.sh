#!/bin/bash

# This script is to configure the SD card on the Raspberry Pi

set -e

host=raspberrypi.local
userHost=pi@$host

echo "Installing saltstack"
scp install-saltstack.sh $userHost:
ssh $userHost "sudo ./install-saltstack.sh"
ssh $userHost "sudo rm ./install-saltstack.sh"

echo "Applying salt state"
wget https://github.com/TheCacophonyProject/saltops/archive/prod.zip
unzip prod.zip
cd saltops-prod/
sed -i '/maybe-reboot/d' salt/top.sls # We don't want to reboot when making the image
ssh $userHost "sudo mkdir -p /etc/cacophony" # Needed for now for cacophony-config to install properly
./state-apply-test.sh $host
cd ..
rm -r ./saltops-prod/
rm prod.zip
ssh $userHost "sudo rm -rf /srv/*"

ssh $userHost "sudo systemctl stop thermal-recorder"
ssh $userHost "sudo systemctl stop thermal-uploader"

ssh $userHost "sudo rm /etc/salt/minion_id"

ssh $userHost "sudo apt-get update "
ssh $userHost "sudo apt-get upgrade -y"
ssh $userHost "sudo apt-get autoremove -y"

#remove salt-name and salt-key
